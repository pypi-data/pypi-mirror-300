import json

import pytest
import requests
from localstack.testing.aws.util import is_aws_cloud
from localstack.testing.pytest import markers
from localstack.utils.aws.arns import get_partition
from localstack.utils.strings import short_uid
from localstack.utils.sync import retry
from tests.aws.services.apigateway.apigateway_fixtures import api_invoke_url
from tests.aws.services.apigateway.conftest import is_next_gen_api


class TestHttpApiAwsProxySubtypeKinesis:
    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            "$..ApiKeyRequired",
            # Seems like it is returned from Kinesis response in LS
            "$..EncryptionType",
            "$..headers.Server",
            # comes from Kinesis formatting
            "$..headers.Content-Length",
            # TODO: LocalStack Kinesis does not return this header
            "$..headers.x-amz-id-2",
        ],
    )
    @markers.snapshot.skip_snapshot_verify(
        # TODO: note, there are so many parity issues it might be worth skipping all together for legacy
        condition=lambda: not is_next_gen_api(),
        paths=[
            "$..ConnectionType",
            # missing from the response in LS
            "$..headers.Connection",
            "$..headers.apigw-requestid",
            # wrong casing in legacy
            "$..headers.x-amzn-requestid",
            "$..headers.x-amzn-RequestId",
        ],
    )
    def test_apigw_v2_http_kinesis_put_record(
        self,
        create_v2_api,
        kinesis_create_stream,
        aws_client,
        create_iam_role_and_attach_policy,
        snapshot,
        region_name,
    ):
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("SequenceNumber"),
                snapshot.transform.key_value("ShardId"),
                snapshot.transform.key_value("StreamName"),
                snapshot.transform.key_value("IntegrationId"),
                snapshot.transform.key_value("RouteId"),
                snapshot.transform.resource_name(),
                # headers transformers
                snapshot.transform.key_value(
                    "Date", reference_replacement=False, value_replacement="<date>"
                ),
                snapshot.transform.key_value("x-amzn-RequestId"),
                snapshot.transform.key_value("x-amz-id-2"),
                snapshot.transform.key_value("apigw-requestid"),
            ]
        )

        stream_name = f"test-{short_uid()}"
        kinesis_create_stream(StreamName=stream_name, ShardCount=1)

        result = create_v2_api(ProtocolType="HTTP", Name=f"{short_uid()}")
        api_id = result["ApiId"]
        role_arn = create_iam_role_and_attach_policy(
            policy_arn=f"arn:{get_partition(region_name)}:iam::aws:policy/AmazonKinesisFullAccess",
        )
        integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="AWS_PROXY",
            IntegrationSubtype="Kinesis-PutRecord",
            PayloadFormatVersion="1.0",
            RequestParameters={
                "Data": "$request.body.payload",
                "PartitionKey": "$request.body.kinesisKey",
                "StreamName": stream_name,
            },
            CredentialsArn=role_arn,
        )
        snapshot.match("create-kinesis-integration", integration)

        route = aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="NONE",
            RouteKey="POST /",
            Target=f"integrations/{integration['IntegrationId']}",
        )
        snapshot.match("create-kinesis-route", route)
        aws_client.apigatewayv2.create_stage(ApiId=api_id, StageName="$default", AutoDeploy=True)

        endpoint = api_invoke_url(api_id=api_id, path="/")
        payload = json.dumps(
            {
                "payload": "J0hlbGxvLCBXb3JsZCEnCg==",
                "kinesisKey": "p1",
            }
        )

        def _invoke(headers: dict = None) -> dict:
            response = requests.post(
                endpoint,
                data=payload,
                headers=headers or {},
                verify=False,
            )
            assert response.status_code == 200
            return {
                "content": response.json(),
                "headers": dict(response.headers),
            }

        # We are not waiting for the stream to be ready on purpose, so we're testing the error handling at the same time
        # AWS returns 500 Internal Server Error if the integration fails

        result = retry(_invoke, retries=30)
        snapshot.match("kinesis-integration-no-content-type", result)

        result = _invoke(headers={"Content-Type": "application/json"})
        snapshot.match("kinesis-integration-json", result)

    @markers.aws.validated
    @pytest.mark.skipif(
        not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in Legacy"
    )
    @markers.snapshot.skip_snapshot_verify(
        paths=["$..headers.Server"],
    )
    def test_apigw_v2_http_kinesis_put_record_no_stream(
        self,
        create_v2_api,
        kinesis_create_stream,
        aws_client,
        wait_for_stream_ready,
        create_iam_role_and_attach_policy,
        snapshot,
        region_name,
    ):
        snapshot.add_transformers_list(
            [
                # headers transformers
                snapshot.transform.key_value(
                    "Date", reference_replacement=False, value_replacement="<date>"
                ),
                snapshot.transform.key_value("apigw-requestid"),
            ]
        )
        stream_name = f"test-{short_uid()}"
        kinesis_create_stream(StreamName=stream_name, ShardCount=1)

        # We are now waiting for the stream to be ready on purpose, so that the integration fails not because the
        # stream is still getting created
        wait_for_stream_ready(stream_name)

        result = create_v2_api(ProtocolType="HTTP", Name=f"{short_uid()}")
        api_id = result["ApiId"]
        role_arn = create_iam_role_and_attach_policy(
            policy_arn=f"arn:{get_partition(region_name)}:iam::aws:policy/AmazonKinesisFullAccess",
        )
        integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="AWS_PROXY",
            IntegrationSubtype="Kinesis-PutRecord",
            PayloadFormatVersion="1.0",
            RequestParameters={
                "Data": "$request.body.payload",
                "PartitionKey": "$request.body.kinesisKey",
                "StreamName": "$request.body.streamName",
                "ExplicitHashKey": "$request.body.testOptional",
            },
            CredentialsArn=role_arn,
        )

        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="NONE",
            RouteKey="POST /",
            Target=f"integrations/{integration['IntegrationId']}",
        )
        aws_client.apigatewayv2.create_stage(ApiId=api_id, StageName="$default", AutoDeploy=True)

        endpoint = api_invoke_url(api_id=api_id, path="/")

        def _invoke(payload: dict, headers: dict = None, expected_status_code: int = 500) -> dict:
            response = requests.post(
                endpoint,
                data=json.dumps(payload),
                headers=headers or {},
                verify=False,
            )
            assert response.status_code == expected_status_code
            return {
                "content": response.json(),
                "headers": dict(response.headers),
            }

        # missing required parameter (StreamName)
        payload_missing_required = {
            "payload": "J0hlbGxvLCBXb3JsZCEnCg==",
            "kinesisKey": "p1",
        }

        result = retry(
            _invoke, retries=30, payload=payload_missing_required, expected_status_code=400
        )
        snapshot.match("kinesis-integration-missing-required", result)

        # missing optional parameter (StreamName)
        payload_missing_optional = {
            "payload": "J0hlbGxvLCBXb3JsZCEnCg==",
            "kinesisKey": "p1",
            "streamName": stream_name,
        }

        result = _invoke(payload=payload_missing_optional, expected_status_code=400)
        snapshot.match("kinesis-integration-missing-optional", result)

        # empty required parameter (StreamName)
        payload_bad_name = {
            "payload": "J0hlbGxvLCBXb3JsZCEnCg==",
            "kinesisKey": "p1",
            "streamName": "",
            "testOptional": "123",
        }

        result = _invoke(payload=payload_bad_name, expected_status_code=400)
        snapshot.match("kinesis-integration-empty-required", result)

        # empty optional parameter
        payload_bad_name = {
            "payload": "J0hlbGxvLCBXb3JsZCEnCg==",
            "kinesisKey": "p1",
            "streamName": "badname",
            "testOptional": "",
        }

        result = _invoke(payload=payload_bad_name, expected_status_code=400)
        snapshot.match("kinesis-integration-empty-optional", result)

        # bad required parameter (StreamName)
        payload_bad_name = {
            "payload": "J0hlbGxvLCBXb3JsZCEnCg==",
            "kinesisKey": "p1",
            "streamName": "doesntexist",
            "testOptional": "123",
        }

        result = _invoke(payload=payload_bad_name, expected_status_code=500)
        snapshot.match("kinesis-integration-bad-stream-name", result)
