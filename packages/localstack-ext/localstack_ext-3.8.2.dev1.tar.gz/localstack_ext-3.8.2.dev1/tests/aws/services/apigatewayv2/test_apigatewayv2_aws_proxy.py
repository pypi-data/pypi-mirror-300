import base64
import gzip
import json
import os
from typing import BinaryIO
from urllib.parse import urlencode

import pytest
import requests
from localstack.aws.api.lambda_ import Runtime
from localstack.testing.aws.util import is_aws_cloud
from localstack.testing.pytest import markers
from localstack.utils.strings import short_uid, to_str
from localstack.utils.sync import retry
from tests.aws.services.apigateway.apigateway_fixtures import api_invoke_url
from tests.aws.services.apigateway.conftest import (
    LAMBDA_BASE64_RESPONSE,
    LAMBDA_ECHO,
    LAMBDA_ECHO_EVENT,
    LAMBDA_GZIP_RESPONSE,
    LAMBDA_RESPONSE_FROM_BODY,
    is_next_gen_api,
)


def invoke(
    path: str,
    api_id: str,
    method: str = "GET",
    body: str | bytes | BinaryIO | dict = None,
    _json: dict = None,
    headers: dict[str, str] = None,
    params: dict[str, list[str] | str] = None,
    cookies: dict[str, str] = None,
    stage_name: str = None,
    stream: bool = False,
    expected_status_code: int = 200,
) -> requests.Response:
    if stage_name:
        _endpoint = api_invoke_url(api_id=api_id, path=path, stage=stage_name)
    else:
        _endpoint = api_invoke_url(api_id=api_id, path=path)

    kwargs = {}
    if body:
        kwargs["data"] = body
    if params:
        kwargs["params"] = params
    if cookies:
        kwargs["cookies"] = cookies
    if _json is not None:
        kwargs["json"] = _json
    if stream is not None:
        kwargs["stream"] = stream

    req_headers = {"User-Agent": "python/test"}
    if headers:
        req_headers.update(headers)

    _response = requests.request(
        method=method,
        url=_endpoint,
        headers=req_headers,
        verify=False,
        **kwargs,
    )
    assert _response.status_code == expected_status_code
    return _response


class TestHttpApiAwsProxyIntegration:
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            "$..ApiKeyRequired",
        ],
    )
    @markers.snapshot.skip_snapshot_verify(
        # TODO: note, there are so many parity issues it might be worth skipping all together for legacy
        condition=lambda: not is_next_gen_api(),
        paths=[
            "$..ConnectionType",
            "$..ApiKeySelectionExpression",
            "$..CreatedDate",
            "$..DisableExecuteApiEndpoint",
            "$..RouteSelectionExpression",
            "$..body",
            "$..Content-Length",
            "$..content-length",
            "$..Connection",
            "$..connection",
            "$..user-agent",
            "$..User-Agent",
            "$..Host",
            "$..host",
            "$..Cookie",
            "$..cookie",
            "$..multiValueQueryStringParameters",
            "$..queryStringParameters",
            "$..pathParameters",
            "$..requestContext.authorizer",
            "$..requestContext.deploymentId",
            "$..requestContext.domainName",
            "$..requestContext.extendedRequestId",
            "$..requestContext.eventType",
            "$..requestContext.identity.accessKey",
            "$..requestContext.identity.accountId",
            "$..requestContext.identity.caller",
            "$..requestContext.identity.cognitoAmr",
            "$..requestContext.identity.cognitoAuthenticationProvider",
            "$..requestContext.identity.cognitoAuthenticationType",
            "$..requestContext.identity.cognitoIdentityId",
            "$..requestContext.identity.cognitoIdentityPoolId",
            "$..requestContext.identity.principalOrgId",
            "$..requestContext.identity.user",
            "$..requestContext.identity.userArn",
            "$..requestContext.messageId",
            "$..requestContext.requestId",
            "$..requestContext.resourceId",
            "$..requestContext.resourcePath",
            "$..requestContext.routeKey",
            "$..requestContext.version",
            "$..requestContext.http.path",
            "$..resource",
            "$..stageVariables",
            "$..X-Amzn-Trace-Id",
            "$..x-amzn-trace-id",
            "$..X-Forwarded-For",
            "$..x-forwarded-for",
            "$..X-Forwarded-Port",
            "$..x-forwarded-port",
            "$..X-Forwarded-Proto",
            "$..x-forwarded-proto",
            "$..x-localstack-edge",
            "$.invoke-api-test-path-basic-prepended-and-stage.requestContext.path",
            "$.invoke-api-test-query-string.path",
            "$.invoke-api-test-headers-casing.headers.CaSeD-HEADER",
            "$.invoke-api-test-headers-casing.headers.cased-header",
            "$.invoke-api-test-body.isBase64Encoded",
            "$..rawQueryString",
            "$.invoke-api-test-path-basic-prepended-and-stage.rawPath",
            "$..routeKey",
        ],
    )
    @markers.aws.validated
    @pytest.mark.parametrize("payload_format", ["1.0", "2.0"])
    def test_lambda_payload_format(
        self,
        create_v2_api,
        create_lambda_function,
        add_permission_for_integration_lambda,
        payload_format,
        snapshot,
        aws_client,
        add_aws_proxy_snapshot_transformers,
    ):
        snapshot.add_transformer(snapshot.transform.key_value("ApiEndpoint"), priority=-2)
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("ApiId"),
                snapshot.transform.key_value("IntegrationId"),
                snapshot.transform.key_value("RouteId"),
            ]
        )
        lambda_name = f"int-{short_uid()}"
        result = create_lambda_function(
            handler_file=LAMBDA_ECHO_EVENT, func_name=lambda_name, runtime=Runtime.nodejs20_x
        )
        lambda_arn = result["CreateFunctionResponse"]["FunctionArn"]

        result = create_v2_api(ProtocolType="HTTP", Name="test-aws-proxy-payload-format")
        snapshot.match("create-api", result)
        api_id = result["ApiId"]

        add_permission_for_integration_lambda(api_id, lambda_arn)

        create_integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="AWS_PROXY",
            PayloadFormatVersion=payload_format,
            IntegrationMethod="ANY",
            IntegrationUri=lambda_arn,
        )
        snapshot.match("create-integration", create_integration)
        integration_id = create_integration["IntegrationId"]

        create_route = aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="GET /{proxy+}",
            Target=f"integrations/{integration_id}",
            AuthorizationType="NONE",
        )
        snapshot.match("create-route", create_route)

        create_default_route = aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="$default",
            Target=f"integrations/{integration_id}",
            AuthorizationType="NONE",
        )
        snapshot.match("create-default-route", create_default_route)

        for stage in ("$default", "dev"):
            aws_client.apigatewayv2.create_stage(
                ApiId=api_id,
                StageName=stage,
                AutoDeploy=True,
            )

        response = retry(invoke, sleep=1, retries=10, path="test-path", api_id=api_id)
        snapshot.match("invoke-api-test-path-basic", response.json())

        response = invoke(path="///test-path-prepended", api_id=api_id)
        snapshot.match("invoke-api-test-path-basic-prepended", response.json())

        response = retry(
            invoke,
            sleep=1,
            retries=10,
            path="///test-path-prepended",
            stage_name="dev",
            api_id=api_id,
        )
        snapshot.match("invoke-api-test-path-basic-prepended-and-stage", response.json())

        response = invoke(
            path="/test", headers={"test-header": "value", "CaSeD-HEADER": "value2"}, api_id=api_id
        )
        snapshot.match("invoke-api-test-headers-casing", response.json())

        response = invoke(
            path="/test",
            api_id=api_id,
            params={
                "test-qs": "value",
                "test-multi": ["value2", "value3"],
                "test-encoded": "my?qs/value",
            },
        )
        snapshot.match("invoke-api-test-query-string", response.json())

        response = invoke(path="/test", body=b"my test body", api_id=api_id)
        snapshot.match("invoke-api-test-body", response.json())

        response = invoke(path="/test", cookies={"test": "value"}, api_id=api_id)
        snapshot.match("invoke-api-test-cookies", response.json())

        response = invoke(path="/default", method="POST", api_id=api_id)
        snapshot.match("invoke-api-default-route", response.json())

    @markers.aws.validated
    @pytest.mark.skipif(
        condition=not is_next_gen_api() and not is_aws_cloud(),
        reason="Not properly implemented in current implementation, legacy is returning the lambda error directly",
    )
    @markers.snapshot.skip_snapshot_verify(
        # returned by LocalStack by default
        paths=["$..headers.Server"],
    )
    def test_aws_proxy_lambda_runtime_exception(
        self,
        create_v2_api,
        create_lambda_function,
        aws_client,
        add_permission_for_integration_lambda,
        snapshot,
    ):
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("Apigw-Requestid"),
                snapshot.transform.key_value(
                    "Date", reference_replacement=False, value_replacement="<date>"
                ),
            ]
        )
        lambda_name = f"response-format-{short_uid()}"
        # we on purpose set the runtime to be node.js but the function is defined in Python
        result = create_lambda_function(
            handler_file=LAMBDA_RESPONSE_FROM_BODY,
            func_name=lambda_name,
            runtime=Runtime.nodejs20_x,
        )
        lambda_arn = result["CreateFunctionResponse"]["FunctionArn"]

        result = create_v2_api(ProtocolType="HTTP", Name="test-aws-proxy-runtime-exc")
        api_id = result["ApiId"]

        add_permission_for_integration_lambda(api_id, lambda_arn)

        create_integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="AWS_PROXY",
            PayloadFormatVersion="1.0",
            IntegrationMethod="ANY",
            IntegrationUri=lambda_arn,
        )
        integration_id = create_integration["IntegrationId"]

        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="ANY /{proxy+}",
            Target=f"integrations/{integration_id}",
            AuthorizationType="NONE",
        )
        aws_client.apigatewayv2.create_stage(
            ApiId=api_id,
            StageName="$default",
            AutoDeploy=True,
        )

        response = retry(
            invoke, sleep=1, retries=10, path="test-path", api_id=api_id, expected_status_code=500
        )
        snapshot.match(
            "invoke-api-runtime-exc",
            {"content": response.json(), "headers": dict(response.headers)},
        )

    @pytest.mark.skipif(
        condition=not is_next_gen_api() and not is_aws_cloud(),
        reason="Not properly implemented in current implementation",
    )
    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            # returned by LocalStack by default
            "$..headers.Server",
            # TODO: fix those 2 headers as we did in REST APIs
            "$..headers.Connection",
            "$..headers.Content-Type",
        ]
    )
    def test_aws_proxy_response_payload_format_validation_v1(
        self,
        create_v2_api,
        create_lambda_function,
        aws_client,
        add_permission_for_integration_lambda,
        snapshot,
    ):
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("Apigw-Requestid"),
                snapshot.transform.key_value(
                    "Date", reference_replacement=False, value_replacement="<date>"
                ),
            ]
        )
        lambda_name = f"response-format-{short_uid()}"
        result = create_lambda_function(
            handler_file=LAMBDA_RESPONSE_FROM_BODY,
            func_name=lambda_name,
            runtime=Runtime.python3_12,
        )
        lambda_arn = result["CreateFunctionResponse"]["FunctionArn"]

        result = create_v2_api(ProtocolType="HTTP", Name="test-aws-proxy-response-format-v1")
        api_id = result["ApiId"]

        add_permission_for_integration_lambda(api_id, lambda_arn)

        create_integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="AWS_PROXY",
            PayloadFormatVersion="1.0",
            IntegrationMethod="ANY",
            IntegrationUri=lambda_arn,
        )
        integration_id = create_integration["IntegrationId"]

        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="ANY /{proxy+}",
            Target=f"integrations/{integration_id}",
            AuthorizationType="NONE",
        )
        aws_client.apigatewayv2.create_stage(
            ApiId=api_id,
            StageName="$default",
            AutoDeploy=True,
        )

        def _invoke(
            body: dict | str, expected_status_code: int = 200, return_headers: bool = False
        ) -> dict:
            _resp = invoke(
                path="test", api_id=api_id, _json=body, expected_status_code=expected_status_code
            )
            try:
                content = _resp.json()
            except json.JSONDecodeError:
                content = _resp.content.decode()
            dict_resp = {"content": content}
            if return_headers:
                dict_resp["headers"] = dict(_resp.headers)

            return dict_resp

        response = retry(_invoke, sleep=1, retries=10, body={"statusCode": 200})
        snapshot.match("invoke-api-no-body", response)

        response = _invoke(
            body={"statusCode": 200, "headers": {"test-header": "value", "header-bool": True}},
            return_headers=True,
        )
        snapshot.match("invoke-api-with-headers", response)

        # seems like in HTTP APIs, there is no validation of the body, it is just ignored unlike REST APIs
        response = _invoke(
            body={"statusCode": 200, "wrongValue": "value"}, expected_status_code=200
        )
        snapshot.match("invoke-api-wrong-format", response)

        # APIGW v2 basically only fails if the statusCode is not provided
        response = _invoke(body={}, expected_status_code=500)
        snapshot.match("invoke-api-empty-response", response)

        response = _invoke(
            body={
                "statusCode": 200,
                "body": base64.b64encode(b"test-data").decode(),
                "isBase64Encoded": True,
            }
        )
        snapshot.match("invoke-api-b64-encoded-true", response)

        response = _invoke(
            body={"statusCode": 200, "body": base64.b64encode(b"test-data").decode()}
        )
        snapshot.match("invoke-api-b64-encoded-false", response)

        response = _invoke(
            body={"statusCode": 200, "multiValueHeaders": {"test-multi": ["value1", "value2"]}},
            return_headers=True,
        )
        snapshot.match("invoke-api-multi-headers-valid", response)

        response = _invoke(
            body={
                "statusCode": 200,
                "multiValueHeaders": {"test-multi": ["value-multi"]},
                "headers": {"test-multi": "value-solo"},
            },
            return_headers=True,
        )
        snapshot.match("invoke-api-multi-headers-overwrite", response)

        response = _invoke(
            body={"statusCode": 200, "multiValueHeaders": {"test-multi-invalid": "value1"}},
            expected_status_code=500,
        )
        snapshot.match("invoke-api-multi-headers-invalid", response)

        response = _invoke(body={"statusCode": "test"}, expected_status_code=500)
        snapshot.match("invoke-api-invalid-status-code", response)

        response = _invoke(body={"statusCode": "201"}, expected_status_code=201)
        snapshot.match("invoke-api-status-code-str", response)

        response = _invoke(body="justAString", expected_status_code=500)
        snapshot.match("invoke-api-just-string", response)

        # APIGW v2 basically only fails if the statusCode is not provided
        response = _invoke(body={"headers": {"test-header": "value"}}, expected_status_code=500)
        snapshot.match("invoke-api-only-headers", response)

    @pytest.mark.skipif(
        condition=not is_next_gen_api() and not is_aws_cloud(),
        reason="Not properly implemented in current implementation",
    )
    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            # returned by LocalStack by default
            "$..headers.Server",
            # TODO: fix those 2 headers as we did in REST APIs
            "$..headers.Connection",
            "$..headers.Content-Type",
        ]
    )
    def test_aws_proxy_response_payload_format_validation_v2(
        self,
        create_v2_api,
        create_lambda_function,
        aws_client,
        add_permission_for_integration_lambda,
        snapshot,
    ):
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("Apigw-Requestid"),
                snapshot.transform.key_value(
                    "Date", reference_replacement=False, value_replacement="<date>"
                ),
            ]
        )
        lambda_name = f"response-format-{short_uid()}"
        result = create_lambda_function(
            handler_file=LAMBDA_RESPONSE_FROM_BODY,
            func_name=lambda_name,
            runtime=Runtime.python3_12,
        )
        lambda_arn = result["CreateFunctionResponse"]["FunctionArn"]

        result = create_v2_api(ProtocolType="HTTP", Name="test-aws-proxy-response-format-v1")
        api_id = result["ApiId"]

        add_permission_for_integration_lambda(api_id, lambda_arn)

        create_integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="AWS_PROXY",
            PayloadFormatVersion="2.0",
            IntegrationMethod="ANY",
            IntegrationUri=lambda_arn,
        )
        integration_id = create_integration["IntegrationId"]

        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="ANY /{proxy+}",
            Target=f"integrations/{integration_id}",
            AuthorizationType="NONE",
        )
        aws_client.apigatewayv2.create_stage(
            ApiId=api_id,
            StageName="$default",
            AutoDeploy=True,
        )

        def _invoke(body: dict | str, expected_status_code: int = 200) -> dict:
            _resp = invoke(
                path="test", api_id=api_id, _json=body, expected_status_code=expected_status_code
            )
            try:
                content = _resp.json()
            except json.JSONDecodeError:
                content = _resp.content.decode()
            return {
                "content": content,
                "headers": dict(_resp.headers),
            }

        response = retry(_invoke, sleep=1, retries=10, body={"statusCode": 200})
        snapshot.match("invoke-api-no-body", response)

        response = _invoke(
            body={"statusCode": 200, "headers": {"test-header": "value", "header-bool": True}}
        )
        snapshot.match("invoke-api-with-headers", response)

        # seems like in HTTP APIs, there is no validation of the body, it is just ignored unlike REST APIs
        response = _invoke(
            body={"statusCode": 200, "wrongValue": "value"}, expected_status_code=200
        )
        snapshot.match("invoke-api-wrong-format", response)

        response = _invoke(body={}, expected_status_code=200)
        snapshot.match("invoke-api-empty-response", response)

        response = _invoke(
            body={
                "statusCode": 200,
                "body": base64.b64encode(b"test-data").decode(),
                "isBase64Encoded": True,
            }
        )
        snapshot.match("invoke-api-b64-encoded-true", response)

        response = _invoke(
            body={"statusCode": 200, "body": base64.b64encode(b"test-data").decode()}
        )
        snapshot.match("invoke-api-b64-encoded-false", response)

        response = _invoke(
            body={
                "statusCode": 200,
                "cookies": ["test-cookie=value", "test-cookie2=value1", "test-cookie3=value2"],
            },
        )
        snapshot.match("invoke-api-cookies", response)

        response = _invoke(
            body={"statusCode": 200, "cookies": {"test-cookies-invalid": "value1"}},
            expected_status_code=500,
        )
        snapshot.match("invoke-api-cookies-invalid", response)
        # TODO: once we remove the snapshot skip due to Content-Type never-empty error, we can remove this assertion
        assert response["headers"]["Content-Type"] == "application/json"

        response = _invoke(body={"statusCode": "test"}, expected_status_code=500)
        snapshot.match("invoke-api-invalid-status-code", response)

        response = _invoke(body={"statusCode": "201"}, expected_status_code=201)
        snapshot.match("invoke-api-status-code-str", response)

        response = _invoke(body="justAString")
        snapshot.match("invoke-api-just-string", response)

        response = _invoke(body={"headers": {"test-header": "value"}})
        snapshot.match("invoke-api-only-headers", response)

        response = _invoke(body={"random": {"json-body": "value"}})
        snapshot.match("invoke-api-json-body", response)

        # seems like AWS is doing matching on what lambda would return if it failed...
        response = _invoke(
            body={"errorMessage": "test fake error message"}, expected_status_code=500
        )
        snapshot.match("invoke-api-error-message", response)

        response = invoke(path="test", api_id=api_id, _json="null", expected_status_code=200)
        assert response.content == b"null"
        snap_response = {
            "content": response.json(),
            "headers": dict(response.headers),
        }
        snapshot.match("invoke-api-fake-null", snap_response)

        response = _invoke(body="", expected_status_code=200)
        snapshot.match("invoke-api-no-response", response)

        response = _invoke(body="errorMessage", expected_status_code=200)
        snapshot.match("invoke-api-error-message-in-str", response)

    @markers.aws.validated
    def test_aws_proxy_return_gzip_response(
        self,
        create_lambda_function,
        aws_client,
        create_v2_api,
        add_permission_for_integration_lambda,
    ):
        lambda_name = f"response-gzip-{short_uid()}"
        result = create_lambda_function(
            handler_file=LAMBDA_GZIP_RESPONSE,
            func_name=lambda_name,
            runtime=Runtime.python3_12,
        )
        lambda_arn = result["CreateFunctionResponse"]["FunctionArn"]

        result = create_v2_api(
            ProtocolType="HTTP",
            Name="test-aws-proxy-gzip",
            Target=lambda_arn,
        )
        api_id = result["ApiId"]

        add_permission_for_integration_lambda(api_id, lambda_arn)

        data = {"content": "test 123"}
        response = retry(
            invoke,
            sleep=1,
            retries=10,
            path="/test/resource1",
            method="POST",
            api_id=api_id,
            _json=data,
        )
        assert response.ok
        assert json.loads(to_str(response.content)) == data

        data_gzip = {
            "content": "test 123",
            # passing gzip = True will make the lambda return a gzipped response
            "gzip": True,
        }
        response = invoke(
            path="/test/resource1",
            method="POST",
            api_id=api_id,
            _json=data_gzip,
            headers={"Accept-Encoding": "gzip"},
            # this allows us to directly read the returning stream, and manually assert that the request was gzip
            # encoded
            stream=True,
        )

        assert response.ok
        content = response.raw.read()
        content = gzip.decompress(content)
        assert json.loads(to_str(content)) == data_gzip

    @markers.aws.validated
    def test_lambda_handling_binary_data(
        self,
        create_v2_api,
        create_lambda_function,
        add_permission_for_integration_lambda,
        aws_client,
    ):
        lambda_name = f"response-b64-data-{short_uid()}"
        result = create_lambda_function(
            handler_file=LAMBDA_BASE64_RESPONSE,
            func_name=lambda_name,
            runtime=Runtime.python3_12,
        )
        lambda_arn = result["CreateFunctionResponse"]["FunctionArn"]

        result = create_v2_api(
            ProtocolType="HTTP",
            Name="test-aws-proxy-b64",
            Target=lambda_arn,
        )
        api_id = result["ApiId"]

        add_permission_for_integration_lambda(api_id, lambda_arn)

        image_file = os.path.join(os.path.dirname(__file__), "resources", "nyan-cat.jpg")
        image_data_read = open(image_file, "rb").read()

        response = retry(
            invoke,
            sleep=1,
            retries=10,
            path="/test/resource1",
            method="POST",
            api_id=api_id,
            body=image_data_read,
            headers={"response-status-code": "200"},
        )
        assert response.status_code == 200
        assert response.content == image_data_read

        response_404 = invoke(
            path="/test/resource1",
            method="POST",
            api_id=api_id,
            body=open(image_file, "rb"),
            headers={"response-status-code": "404"},
            expected_status_code=404,
        )
        assert response_404.status_code == 404
        # assert that even with a 404 code, it still returns the data
        assert response_404.content == image_data_read

    @markers.aws.validated
    def test_lambda_handling_form_urlencoded_data(
        self,
        create_v2_api,
        create_lambda_function,
        add_permission_for_integration_lambda,
        aws_client,
    ):
        # create Lambda
        lambda_name = f"echo-encoding-{short_uid()}"
        lambda_fn = LAMBDA_ECHO % 'event.headers["resp-is-encoded"] == "true"'
        lambda_arn = create_lambda_function(
            handler_file=lambda_fn, func_name=lambda_name, runtime=Runtime.nodejs20_x
        )["CreateFunctionResponse"]["FunctionArn"]

        # create API
        result = create_v2_api(Name="test-form-urlencoded", ProtocolType="HTTP", Target=lambda_arn)
        api_id = result["ApiId"]
        add_permission_for_integration_lambda(api_id, lambda_arn)

        url_parameters = {"param1": "value1", "param2": "value2"}
        response_encoded = retry(
            invoke,
            sleep=1,
            retries=10,
            path="/test/resource1",
            method="POST",
            api_id=api_id,
            body=url_parameters,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "resp-is-encoded": "true",
            },
        )
        assert response_encoded.ok
        assert to_str(response_encoded.content) == urlencode(url_parameters)

        response_non_encoded = invoke(
            path="/test/resource1",
            method="POST",
            api_id=api_id,
            body=url_parameters,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "resp-is-encoded": "false",
            },
        )
        assert response_non_encoded.ok
        assert to_str(response_non_encoded.content) == to_str(
            base64.b64encode(b"param1=value1&param2=value2")
        )

    @markers.aws.validated
    @pytest.mark.skipif(
        condition=not is_next_gen_api() and not is_aws_cloud(),
        reason="Not properly implemented in current implementation, legacy is returning the lambda error directly",
    )
    def test_lambda_input_base_64_detection(
        self,
        create_v2_api,
        create_lambda_function,
        add_permission_for_integration_lambda,
        snapshot,
        aws_client,
        add_aws_proxy_snapshot_transformers,
    ):
        lambda_name = f"int-{short_uid()}"
        result = create_lambda_function(
            handler_file=LAMBDA_ECHO_EVENT, func_name=lambda_name, runtime=Runtime.nodejs20_x
        )
        lambda_arn = result["CreateFunctionResponse"]["FunctionArn"]

        result = create_v2_api(
            ProtocolType="HTTP", Name="test-aws-proxy-b64-input-format", Target=lambda_arn
        )
        api_id = result["ApiId"]
        add_permission_for_integration_lambda(api_id, lambda_arn)

        def _invoke(body: str | bytes, content_type: str) -> dict:
            resp = invoke(
                path="/test", body=body, api_id=api_id, headers={"Content-Type": content_type}
            )
            return {"body": resp.json()["body"]}

        response = retry(_invoke, sleep=1, retries=10, body="Hello", content_type="text/html")
        snapshot.match("invoke-api-test-body-text-html", response)

        response = _invoke(body=b"my test body", content_type="application/test")
        snapshot.match("invoke-api-application-test", response)

        response = _invoke(body=b"my test body", content_type="application/json")
        snapshot.match("invoke-api-application-json", response)

        response = _invoke(body=b"my test body", content_type="text/test")
        snapshot.match("invoke-api-text-test", response)

        response = _invoke(body=b"my test body", content_type="text/plain")
        snapshot.match("invoke-api-text-plain", response)

        response = _invoke(body=b"my test body", content_type="application/vnd.ms-excel")
        snapshot.match("invoke-api-application-excel", response)

        response = _invoke(body=b"my test body", content_type="text/javascript")
        snapshot.match("invoke-api-text-javascript", response)

        if is_aws_cloud():
            # TODO: LocalStack does not handle invalid x-www-form-urlencoded request, it sets the data to b"" instead
            #  of the invalid data, due to `restore_payload`
            response = _invoke(
                body=b"my test body", content_type="application/x-www-form-urlencoded"
            )
            snapshot.match("invoke-api-application-x-www-form-urlencoded", response)

            # TODO: it also doesn't manage multipart data for the same reasons
            response = _invoke(
                body=b"my test body",
                content_type="multipart/form-data; boundary=------9051914041544843365972754266",
            )
            snapshot.match("invoke-api-multipart-form-data", response)

        response = _invoke(body=b"my test body", content_type="image/svg+xml")
        snapshot.match("invoke-api-image-svg-xml", response)

        response = _invoke(body=b"my test body", content_type="application/xml")
        snapshot.match("invoke-api-application-xml", response)

        response = _invoke(body=b"my test body", content_type="text/binary")
        snapshot.match("invoke-api-text-binary", response)

        response = _invoke(
            body=b"\xabW\xdc\x17\xe4q~\xec\x01\x05m\xd0\xdd\x80\t", content_type="text/test"
        )
        snapshot.match("invoke-api-text-bad-text", response)
