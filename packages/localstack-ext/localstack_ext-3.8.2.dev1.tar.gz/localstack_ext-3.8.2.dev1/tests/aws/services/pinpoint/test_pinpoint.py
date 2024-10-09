import logging

import pytest
from botocore.config import Config
from botocore.exceptions import ClientError
from localstack.pro.core.aws.api.pinpoint import CreateApplicationRequest, CreateAppResponse
from localstack.testing.pytest import markers
from localstack.utils.strings import short_uid

LOG = logging.getLogger(__name__)


@pytest.fixture
def pinpoint_create_app(aws_client):
    apps = []

    def _create_app(create_application_request: CreateApplicationRequest) -> CreateAppResponse:
        create_application_request.setdefault("Name", f"PinpointTest-{short_uid()}")

        create_app = aws_client.pinpoint.create_app(
            CreateApplicationRequest=create_application_request,
        )
        apps.append(create_app["ApplicationResponse"]["Id"])

        return create_app

    yield _create_app

    for app_id in apps:
        try:
            aws_client.pinpoint.delete_app(ApplicationId=app_id)
        except aws_client.pinpoint.exceptions.NotFoundException:
            pass
        except aws_client.pinpoint.exceptions.ClientError as e:
            LOG.warning("Error while cleaning up Pinpoint App %s - %s", app_id, e)


class TestPinpoint:
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            # TODO: moto does not return the tags for those operations
            "$.get_app_response.ApplicationResponse.tags",
            "$.delete_app_response.ApplicationResponse.tags",
        ]
    )
    @markers.aws.validated
    def test_pinpoint_app_operations(self, aws_client, pinpoint_create_app, snapshot):
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("Id"),
                snapshot.transform.key_value("Name"),
            ]
        )
        application_name = f"ExampleCorp-{short_uid()}"

        # Create Pinpoint App
        create_app_response = pinpoint_create_app(
            {"Name": application_name, "tags": {"Stack": "Test"}}
        )
        snapshot.match("create_app_response", create_app_response)

        app_id = create_app_response["ApplicationResponse"]["Id"]

        # Get details of the created Pinpoint App
        get_app_response = aws_client.pinpoint.get_app(ApplicationId=app_id)
        snapshot.match("get_app_response", get_app_response)

        # delete the created Pinpoint App
        delete_app_response = aws_client.pinpoint.delete_app(ApplicationId=app_id)
        snapshot.match("delete_app_response", delete_app_response)

    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        # TODO: moto does not add the RequestId to the exception body
        paths=["$..RequestID"],
    )
    def test_pinpoint_app_operations_on_non_existent_app(
        self, aws_client, pinpoint_create_app, snapshot
    ):
        snapshot.add_transformer(snapshot.transform.key_value("RequestID"))

        with pytest.raises(ClientError) as e:
            aws_client.pinpoint.get_app(ApplicationId="random-app")
        snapshot.match("get-non-existent-app", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.pinpoint.delete_app(ApplicationId="random-app")
        snapshot.match("delete-non-existent-app", e.value.response)


class TestPinpointSMSChannel:
    @pytest.fixture(autouse=True)
    def create_app_transformer(self, snapshot):
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("ApplicationId"),
                snapshot.transform.key_value("Name"),
            ]
        )

    @markers.aws.validated
    def test_pinpoint_sms_channel_lifecycle(self, aws_client, pinpoint_create_app, snapshot):
        application_name = f"TestSMSChannel-{short_uid()}"
        # Create Pinpoint App
        create_app_response = pinpoint_create_app({"Name": application_name})
        snapshot.match("create-app", create_app_response)

        app_id = create_app_response["ApplicationResponse"]["Id"]

        # try getting the SMSChannel before enabling it or interacting with it at all
        with pytest.raises(ClientError) as e:
            aws_client.pinpoint.get_sms_channel(ApplicationId=app_id)
        snapshot.match("get-sms-channel-before-update", e.value.response)

        update_sms_channel = aws_client.pinpoint.update_sms_channel(
            ApplicationId=app_id,
            SMSChannelRequest={
                "Enabled": True,
                "SenderId": "",
                "ShortCode": "",
            },
        )
        snapshot.match("update-sms-channel", update_sms_channel)

        get_sms_channel = aws_client.pinpoint.get_sms_channel(
            ApplicationId=app_id,
        )
        snapshot.match("get-sms-channel-after-update", get_sms_channel)

        delete_sms_channel = aws_client.pinpoint.delete_sms_channel(ApplicationId=app_id)
        snapshot.match("delete-sms-channel", delete_sms_channel)

        with pytest.raises(ClientError) as e:
            aws_client.pinpoint.get_sms_channel(ApplicationId=app_id)
        snapshot.match("get-sms-channel-after-delete", e.value.response)

        update_sms_channel = aws_client.pinpoint.update_sms_channel(
            ApplicationId=app_id,
            SMSChannelRequest={
                "Enabled": False,
                "SenderId": "test-id",
                "ShortCode": "77766",
            },
        )
        snapshot.match("update-sms-channel-2", update_sms_channel)

        get_sms_channel = aws_client.pinpoint.get_sms_channel(
            ApplicationId=app_id,
        )
        snapshot.match("get-sms-channel-after-update-2", get_sms_channel)

    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            # AWS returns location information that we don't (Line x Column y)
            "$..Error.Message",
            "$..Message",
        ]
    )
    def test_pinpoint_update_sms_channel_validation(
        self, aws_client_factory, pinpoint_create_app, snapshot, region_name
    ):
        application_name = f"TestSMSChannel-{short_uid()}"
        # Create Pinpoint App
        create_app_response = pinpoint_create_app({"Name": application_name})
        snapshot.match("create-app", create_app_response)

        app_id = create_app_response["ApplicationResponse"]["Id"]

        pinpoint_client = aws_client_factory(
            region_name=region_name, config=Config(parameter_validation=False)
        ).pinpoint

        update_str_value = pinpoint_client.update_sms_channel(
            ApplicationId=app_id,
            SMSChannelRequest={
                "ShortCode": "test124",
            },
        )
        snapshot.match("update-sms-channel-no-enabled-first", update_str_value)

        update_str_value = pinpoint_client.update_sms_channel(
            ApplicationId=app_id,
            SMSChannelRequest={
                "Enabled": "true",
            },
        )
        snapshot.match("update-sms-channel-error-enabled-str", update_str_value)

        with pytest.raises(ClientError) as e:
            pinpoint_client.update_sms_channel(
                ApplicationId=app_id,
                SMSChannelRequest={
                    "Enabled": "random-value",
                },
            )
        snapshot.match("update-sms-channel-error-enabled-no-bool", e.value.response)
        # AWS adds text position to the error (Line 1 Column 12), so we have to manually match the error
        e.match(
            'Cannot deserialize value of type `Boolean` from String "random-value": only "true" or "false" recognized'
        )

        # botocore raises?? test
        no_request = pinpoint_client.update_sms_channel(
            ApplicationId=app_id,
        )
        snapshot.match("update-sms-channel-no-request", no_request)

        # A short code typically contains between three and seven digits, depending on the country that it's based in.
        # with pytest.raises(ClientError) as e:
        bad_short_code = pinpoint_client.update_sms_channel(
            ApplicationId=app_id,
            SMSChannelRequest={
                "Enabled": False,
                "ShortCode": "abcdrefdzndzdazid",
            },
        )
        snapshot.match("update-sms-channel-bad-shortcode", bad_short_code)

        # The sender ID must be 1-11 alphanumeric characters including letters (A-Z), numbers (0-9), or hyphens (-).
        # The sender ID must begin with a letter.
        bad_sender_id = pinpoint_client.update_sms_channel(
            ApplicationId=app_id,
            SMSChannelRequest={"SenderId": "--abdcd/"},
        )
        snapshot.match("update-sms-channel-error-sender-id", bad_sender_id)

    @markers.aws.validated
    def test_pinpoint_sms_channel_non_existent_app(self, aws_client, pinpoint_create_app, snapshot):
        with pytest.raises(ClientError) as e:
            aws_client.pinpoint.update_sms_channel(
                ApplicationId="bad-app-id",
                SMSChannelRequest={"Enabled": True},
            )
        snapshot.match("update-sms-channel-bad-app-id", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.pinpoint.get_sms_channel(
                ApplicationId="bad-app-id",
            )
        snapshot.match("get-sms-channel-bad-app-id", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.pinpoint.delete_sms_channel(
                ApplicationId="bad-app-id",
            )
        snapshot.match("delete-sms-channel-bad-app-id", e.value.response)

    @markers.aws.validated
    def test_pinpoint_sms_channel_multiple_delete(self, aws_client, pinpoint_create_app, snapshot):
        application_name = f"TestSMSChannel-{short_uid()}"
        # Create Pinpoint App
        create_app_response = pinpoint_create_app({"Name": application_name})
        app_id = create_app_response["ApplicationResponse"]["Id"]

        delete_sms_channel = aws_client.pinpoint.delete_sms_channel(
            ApplicationId=app_id,
        )
        snapshot.match("delete-sms-channel", delete_sms_channel)

        delete_sms_channel_2 = aws_client.pinpoint.delete_sms_channel(
            ApplicationId=app_id,
        )
        snapshot.match("delete-sms-channel-2", delete_sms_channel_2)

    @markers.aws.validated
    def test_pinpoint_sms_channel_versions(self, aws_client, pinpoint_create_app, snapshot):
        application_name = f"TestSMSChannel-{short_uid()}"
        # Create Pinpoint App
        create_app_response = pinpoint_create_app({"Name": application_name})
        snapshot.match("create-app", create_app_response)

        app_id = create_app_response["ApplicationResponse"]["Id"]

        update_sms_channel = aws_client.pinpoint.update_sms_channel(
            ApplicationId=app_id,
            SMSChannelRequest={
                "Enabled": True,
                "SenderId": "",
                "ShortCode": "",
            },
        )
        snapshot.match("update-sms-channel", update_sms_channel)

        update_sms_channel = aws_client.pinpoint.update_sms_channel(
            ApplicationId=app_id,
            SMSChannelRequest={
                "Enabled": True,
                "SenderId": "test-id",
                "ShortCode": "",
            },
        )
        snapshot.match("update-sms-channel-2", update_sms_channel)

        update_sms_channel = aws_client.pinpoint.update_sms_channel(
            ApplicationId=app_id,
            SMSChannelRequest={
                "Enabled": True,
                "SenderId": "test-id",
                "ShortCode": "666777",
            },
        )
        snapshot.match("update-sms-channel-3", update_sms_channel)

        delete_sms_channel = aws_client.pinpoint.delete_sms_channel(
            ApplicationId=app_id,
        )
        snapshot.match("delete-sms-channel", delete_sms_channel)

        # the version counter goes back to 1 after deletion
        update_sms_channel = aws_client.pinpoint.update_sms_channel(
            ApplicationId=app_id,
            SMSChannelRequest={
                "Enabled": True,
                "SenderId": "",
                "ShortCode": "",
            },
        )
        snapshot.match("recreate-sms-channel", update_sms_channel)
