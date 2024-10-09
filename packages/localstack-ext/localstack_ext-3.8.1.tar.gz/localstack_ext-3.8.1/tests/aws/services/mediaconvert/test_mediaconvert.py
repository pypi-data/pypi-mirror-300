import json
import time
from pathlib import Path

import pytest
from botocore.exceptions import ClientError
from localstack.config import external_service_url
from localstack.pro.core.aws.api.mediaconvert import CreateQueueResponse
from localstack.testing.aws.util import is_aws_cloud
from localstack.testing.pytest import markers
from localstack.utils.strings import short_uid
from localstack.utils.sync import retry


@pytest.fixture(scope="session")
def load_asset():
    template_root = Path(__file__).parent / "assets"

    def load_template_from_disk(stub: str, mode: str = "rt") -> str:
        with (template_root / stub).open(mode) as infile:
            return infile.read()

    return load_template_from_disk


@pytest.fixture(scope="session")
def load_json_asset(load_asset):
    def load(stub: str) -> dict:
        return json.loads(load_asset(f"{stub}.json"))

    return load


@pytest.fixture
def mediaconvert_client(aws_client, aws_client_factory, region_name):
    endpoint_url = f"https://mediaconvert.{region_name}.amazonaws.com"
    if not is_aws_cloud():
        endpoint_url = external_service_url(subdomains=f"mediaconvert.{region_name}")
    return aws_client_factory(endpoint_url=endpoint_url).mediaconvert


@pytest.fixture
def create_queue(mediaconvert_client):
    queue_names = []

    def _create_queue(
        queue_name: str | None = None, description: str | None = None, **kwargs
    ) -> CreateQueueResponse:
        queue_name = queue_name or kwargs.pop("Name", None) or f"queue-{short_uid()}"
        description = description or kwargs.pop("Description", None) or "Test queue"
        create_queue_result = mediaconvert_client.create_queue(
            Name=queue_name, Description=description, **kwargs
        )
        queue_names.append(queue_name)
        return create_queue_result

    yield _create_queue

    sleep = 1.0
    retries = 3
    if is_aws_cloud():
        sleep = 6.0
        retries = 10

    for queue_name in queue_names:

        def delete_queue():
            mediaconvert_client.delete_queue(Name=queue_name)

        retry(delete_queue, sleep=sleep, retries=retries)


@pytest.fixture
def create_job(mediaconvert_client, account_id, load_json_asset):
    def _create_job(
        payload: dict | None = None, role_arn: str | None = None, queue_name: str | None = None
    ):
        role_arn = (
            role_arn or f"arn:aws:iam::{account_id}:role/service-role/MediaConvert_Default_Role"
        )

        queue_name = queue_name or "Default"
        payload = payload or load_json_asset("minimal-static")
        job_json = {**payload, "Role": role_arn, "Queue": queue_name}

        return mediaconvert_client.create_job(**job_json)

    return _create_job


@pytest.fixture
def create_message_capture_queue_url(aws_client, sqs_queue):
    rule_name = f"rule-{short_uid()}"
    target_id = f"target-{short_uid()}"
    events_client = aws_client.events

    sqs_client = aws_client.sqs

    status_queue_arn = sqs_client.get_queue_attributes(
        QueueUrl=sqs_queue, AttributeNames=["QueueArn"]
    )["Attributes"]["QueueArn"]

    def create(queue_arn: str | None = None):
        pattern = {
            "source": ["aws.mediaconvert"],
            "detail-type": ["MediaConvert Job State Change"],
            "detail": {
                # Terminal states
                "status": ["COMPLETE", "ERROR"],
            },
        }

        if queue_arn:
            pattern["detail"]["queue"] = [queue_arn]

        rule_arn = events_client.put_rule(
            Name=rule_name,
            EventPattern=json.dumps(pattern),
        )["RuleArn"]
        events_client.put_targets(
            Rule=rule_name, Targets=[{"Id": target_id, "Arn": status_queue_arn}]
        )

        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "",
                    "Effect": "Allow",
                    "Principal": {"Service": "events.amazonaws.com"},
                    "Action": "SQS:SendMessage",
                    "Resource": status_queue_arn,
                    "Condition": {"ArnEquals": {"aws:SourceArn": rule_arn}},
                }
            ],
        }
        sqs_client.set_queue_attributes(
            QueueUrl=sqs_queue, Attributes={"Policy": json.dumps(policy)}
        )

        return sqs_queue

    yield create

    events_client.remove_targets(Rule=rule_name, Ids=[target_id])
    events_client.delete_rule(Name=rule_name)


class TestQueuesCrud:
    @markers.aws.validated
    def test_create_queue(self, mediaconvert_client, snapshot, cleanups):
        queue_name = f"queue-{short_uid()}"
        snapshot.add_transformer(snapshot.transform.regex(queue_name, "<queue-name>"))

        description = "Test queue"
        create_result = mediaconvert_client.create_queue(Name=queue_name, Description=description)
        cleanups.append(lambda: mediaconvert_client.delete_queue(Name=queue_name))

        snapshot.match("create-queue", create_result["Queue"])

    @markers.aws.validated
    def test_delete_default_queue(self, mediaconvert_client, snapshot):
        with pytest.raises(ClientError) as exc_info:
            mediaconvert_client.delete_queue(Name="Default")

        snapshot.match("delete-default-queue", exc_info.value.response)

    @markers.aws.validated
    def test_list_queues(self, mediaconvert_client, create_queue):
        queue_name = create_queue()["Queue"]["Name"]

        list_queues_result = mediaconvert_client.list_queues()["Queues"]

        queue_names = [queue["Name"] for queue in list_queues_result]

        assert queue_name in queue_names
        assert "Default" in queue_names


class TestJobsCrud:
    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            "$..ClientRequestToken",
        ]
    )
    @pytest.mark.wip
    def test_create_job(
        self,
        load_json_asset,
        mediaconvert_client,
        account_id,
        create_queue,
        snapshot,
    ):
        queue_name = create_queue()["Queue"]["Name"]
        snapshot.add_transformer(snapshot.transform.regex(queue_name, "<queue-name>"))

        role_arn = f"arn:aws:iam::{account_id}:role/service-role/MediaConvert_Default_Role"
        template_base = load_json_asset("minimal-static")
        job_json = {**template_base, "Role": role_arn, "Queue": queue_name}

        create_job_result = mediaconvert_client.create_job(**job_json)

        snapshot.add_transformer(snapshot.transform.key_value("Id", reference_replacement=True))
        snapshot.match("create-job", create_job_result["Job"])

    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            "$..ClientRequestToken",
            "$..UserMetadata",
        ]
    )
    def test_list_jobs(self, mediaconvert_client, create_queue, create_job, snapshot):
        create_queue_result = create_queue()
        queue_name = create_queue_result["Queue"]["Name"]
        snapshot.add_transformer(snapshot.transform.regex(queue_name, "<queue-name>"))
        snapshot.add_transformer(snapshot.transform.key_value("Id", reference_replacement=True))

        create_job(queue_name=queue_name)

        list_jobs_result = mediaconvert_client.list_jobs(Queue=queue_name)

        snapshot.match("list-jobs", list_jobs_result["Jobs"])


class TestTranscode:
    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            "$..ClientRequestToken",
            # TODO: we should implement this
            "$..OutputGroupDetails",
            "$..Timing.FinishTime",
            "$..Timing.StartTime",
            "$..UserMetadata",
            "$..Warnings",
            # complete event payload
            "$..Body.detail.blackVideoDetected",
            # TODO: we should implement this
            "$..Body.detail.outputGroupDetails",
            "$..Body.detail.paddingInserted",
            "$..Body.detail.timestamp",
            "$..Body.detail.userMetadata",
            "$..Body.detail.warnings",
        ]
    )
    @pytest.mark.wip
    def test_run_transcode_events(
        self,
        snapshot,
        create_queue,
        aws_client,
        mediaconvert_client,
        s3_create_bucket,
        load_json_asset,
        create_role_with_policy,
        create_message_capture_queue_url,
    ):
        """
        Test that runs a transcode job and subscribes to EventBridge events to indicate job completion.
        """
        snapshot.add_transformer(snapshot.transform.key_value("Arn"))
        snapshot.add_transformer(snapshot.transform.key_value("Id"))
        snapshot.add_transformer(snapshot.transform.key_value("Role"))
        snapshot.add_transformer(snapshot.transform.key_value("ReceiptHandle"))
        snapshot.add_transformer(snapshot.transform.key_value("MD5OfBody"))
        snapshot.add_transformer(
            snapshot.transform.key_value("averageBitrate", reference_replacement=False)
        )

        _, role_arn = create_role_with_policy(
            effect="Allow",
            actions=[
                "s3:Put*",
                "s3:List*",
                "s3:Get*",
            ],
            assume_policy_doc=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "mediaconvert.amazonaws.com"},
                            "Action": "sts:AssumeRole",
                        }
                    ],
                }
            ),
        )

        if is_aws_cloud():
            # IAM policies may not be available immediately, so set this up before creating
            # other resources to maximize the chance that we create the object in time
            time.sleep(30)

        job_template = load_json_asset("basic")
        source_bucket_name = f"mediaconvert-source-{short_uid()}"
        dest_bucket_name = f"mediaconvert-dest-{short_uid()}"
        snapshot.add_transformer(snapshot.transform.regex(source_bucket_name, "<source-bucket>"))
        snapshot.add_transformer(snapshot.transform.regex(dest_bucket_name, "<dest-bucket>"))

        source_bucket = s3_create_bucket(Bucket=source_bucket_name)
        dest_bucket = s3_create_bucket(Bucket=dest_bucket_name)

        aws_client.s3.upload_file(
            Filename=Path(__file__).parent.joinpath("assets", "input.mp4"),
            Key="input.mp4",
            Bucket=source_bucket,
        )

        create_queue_result = create_queue()
        snapshot.add_transformer(
            snapshot.transform.regex(create_queue_result["Queue"]["Name"], "<queue-name>")
        )
        queue_arn = create_queue_result["Queue"]["Arn"]

        message_capture_queue_url = create_message_capture_queue_url(queue_arn=queue_arn)

        # update template values
        job_template["Queue"] = queue_arn
        job_template["Role"] = role_arn
        job_template["Settings"]["Inputs"][0]["FileInput"] = f"s3://{source_bucket}/input.mp4"
        job_template["Settings"]["OutputGroups"][0]["OutputGroupSettings"]["HlsGroupSettings"][
            "Destination"
        ] = f"s3://{dest_bucket}/out/"
        # check all placeholders have been replaced
        assert "{{" not in job_template and "}}" not in job_template

        res = mediaconvert_client.create_job(**job_template)
        snapshot.match("create-job", res["Job"])
        job_id = res["Job"]["Id"]

        def receive_messages() -> list:
            messages_res = aws_client.sqs.receive_message(QueueUrl=message_capture_queue_url)
            messages = messages_res["Messages"]
            assert len(messages) > 0
            return messages

        messages = retry(receive_messages, retries=30, sleep=2)
        # the complete message
        assert len(messages) == 1
        snapshot.match("complete-message", messages[0])

        get_job_res = mediaconvert_client.get_job(Id=job_id)
        snapshot.match("completed-job", get_job_res["Job"])

    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            "$..ClientRequestToken",
            "$..UserMetadata",
            # TODO: we should implement this
            "$..Job.OutputGroupDetails",
            "$..Job.Timing.FinishTime",
            "$..Job.Timing.StartTime",
            "$..Job.Warnings",
        ]
    )
    def test_run_transcode_polling(
        self,
        snapshot,
        create_queue,
        aws_client,
        mediaconvert_client,
        s3_create_bucket,
        load_json_asset,
        create_role_with_policy,
    ):
        """
        Test that runs a transcode job and polls for job completion using `GetJob`
        """
        snapshot.add_transformer(snapshot.transform.key_value("Arn"))
        snapshot.add_transformer(snapshot.transform.key_value("Id"))
        snapshot.add_transformer(snapshot.transform.key_value("Role"))
        snapshot.add_transformer(snapshot.transform.key_value("ReceiptHandle"))
        snapshot.add_transformer(snapshot.transform.key_value("MD5OfBody"))
        snapshot.add_transformer(
            snapshot.transform.key_value("averageBitrate", reference_replacement=False)
        )

        _, role_arn = create_role_with_policy(
            effect="Allow",
            actions=[
                "s3:Put*",
                "s3:List*",
                "s3:Get*",
            ],
            assume_policy_doc=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "mediaconvert.amazonaws.com"},
                            "Action": "sts:AssumeRole",
                        }
                    ],
                }
            ),
        )

        if is_aws_cloud():
            # IAM policies may not be available immediately, so set this up before creating
            # other resources to maximize the chance that we create the object in time
            time.sleep(30)

        job_template = load_json_asset("basic")
        source_bucket_name = f"mediaconvert-source-{short_uid()}"
        dest_bucket_name = f"mediaconvert-dest-{short_uid()}"
        snapshot.add_transformer(snapshot.transform.regex(source_bucket_name, "<source-bucket>"))
        snapshot.add_transformer(snapshot.transform.regex(dest_bucket_name, "<dest-bucket>"))

        source_bucket = s3_create_bucket(Bucket=source_bucket_name)
        dest_bucket = s3_create_bucket(Bucket=dest_bucket_name)

        aws_client.s3.upload_file(
            Filename=Path(__file__).parent.joinpath("assets", "input.mp4"),
            Key="input.mp4",
            Bucket=source_bucket,
        )

        create_queue_result = create_queue()
        snapshot.add_transformer(
            snapshot.transform.regex(create_queue_result["Queue"]["Name"], "<queue-name>")
        )
        queue_arn = create_queue_result["Queue"]["Arn"]

        # update template values
        job_template["Queue"] = queue_arn
        job_template["Role"] = role_arn
        job_template["Settings"]["Inputs"][0]["FileInput"] = f"s3://{source_bucket}/input.mp4"
        job_template["Settings"]["OutputGroups"][0]["OutputGroupSettings"]["HlsGroupSettings"][
            "Destination"
        ] = f"s3://{dest_bucket}/out/"
        # check all placeholders have been replaced
        assert "{{" not in job_template and "}}" not in job_template

        res = mediaconvert_client.create_job(**job_template)
        snapshot.match("create-job", res["Job"])
        job_id = res["Job"]["Id"]

        def poll_for_job_completion():
            get_job_res = mediaconvert_client.get_job(Id=job_id)
            assert get_job_res["Job"]["Status"] == "COMPLETE"
            return get_job_res

        complete_job_res = retry(poll_for_job_completion, retries=30, sleep=2)
        snapshot.match("completed-job", complete_job_res)
