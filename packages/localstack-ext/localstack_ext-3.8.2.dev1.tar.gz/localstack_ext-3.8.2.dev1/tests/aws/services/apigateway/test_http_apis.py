import json
import os
from typing import List

import pytest
import requests
from localstack import config
from localstack.aws.api.lambda_ import Runtime
from localstack.http.request import get_full_raw_path
from localstack.pro.core.services.cognito_idp.cognito_utils import (
    get_auth_token_via_login_form,
)
from localstack.services.apigateway.helpers import host_based_url
from localstack.testing.aws.util import is_aws_cloud
from localstack.testing.pytest import markers
from localstack.utils import testutil
from localstack.utils.aws import arns
from localstack.utils.collections import remove_attributes
from localstack.utils.files import load_file
from localstack.utils.strings import short_uid, to_str
from localstack.utils.sync import retry
from pytest_httpserver import HTTPServer
from requests import Response
from werkzeug import Request
from werkzeug import Response as WerkzeugResponse

from tests.aws.services.apigateway.apigateway_fixtures import (
    api_invoke_url,
)
from tests.aws.services.apigateway.conftest import (
    LAMBDA_ECHO_EVENT,
    LAMBDA_JS,
    LAMBDA_REQUEST_AUTH,
    is_next_gen_api,
)

API_SPEC_FILE = os.path.join(os.path.dirname(__file__), "../../templates", "openapi.spec.json")
THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))


def assert_lambda_authorizer_event_payload_v1(
    result: Response, scopes: List[str] = None, token_type: str = None
):
    body = json.loads(result.text)
    request_context = body.get("requestContext")
    authorizer_obj = request_context.get("authorizer")
    assert "claims" in authorizer_obj
    if token_type:
        assert authorizer_obj["claims"]["token_use"] == token_type
    assert "scopes" in authorizer_obj
    if scopes:
        assert any(scope in authorizer_obj["scopes"] for scope in scopes)
    else:
        assert authorizer_obj["scopes"] == scopes


def assert_lambda_authorizer_event_payload_v2(
    result: Response, scopes: List[str] = None, token_type: str = None
):
    body = json.loads(result.text)
    request_context = body.get("requestContext")
    authorizer_obj = request_context.get("authorizer")
    jwt_claims = authorizer_obj.get("jwt")
    assert "claims" in jwt_claims
    if token_type:
        assert jwt_claims["claims"]["token_use"] == token_type
    assert "scopes" in jwt_claims
    if scopes:
        assert any(scope in jwt_claims["scopes"] for scope in scopes)
    else:
        assert jwt_claims["scopes"] == scopes


def create_deployment(apigatewayv2_client, api_id, stage_name=None):
    stage_name = stage_name or "test-stage"
    deployment_id = apigatewayv2_client.create_deployment(ApiId=api_id)["DeploymentId"]
    apigatewayv2_client.create_stage(ApiId=api_id, StageName=stage_name, DeploymentId=deployment_id)

    def _deployment_ready():
        result = apigatewayv2_client.get_deployment(ApiId=api_id, DeploymentId=deployment_id)
        assert result["DeploymentStatus"] == "DEPLOYED"

    retry(_deployment_ready, sleep=1, retries=10)
    return deployment_id


class TestHttpApis:
    """Tests for API GW v2 HTTP APIs."""

    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            "$..Connection",
            "$..Content-Type",
            "$..X-Amzn-Trace-Id",
            "$..X-Localstack-Edge",
            "$..X-Localstack-Tgt-Api",
        ]
    )
    def test_import_and_invoke_http_api(
        self, aws_client, echo_http_server_post, import_apigw_v2, snapshot
    ):
        snapshot.add_transformer(
            snapshot.transform.key_value("Forwarded", "forwarded", reference_replacement=False)
        )
        snapshot.add_transformer(snapshot.transform.key_value("Host", "host"))
        snapshot.add_transformer(
            snapshot.transform.key_value("User-Agent", "<user-agent>", reference_replacement=False)
        )
        snapshot.add_transformer(snapshot.transform.key_value("Header1", "request-id"))
        api_spec = load_file(API_SPEC_FILE)

        result = import_apigw_v2(api_spec)
        api_id = result["ApiId"]
        # TODO: add tests for additional integrations like Lambda, etc
        params = {
            "append:header.header1": "$context.requestId",
            "append:header.header2": "test",
        }
        result = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            IntegrationUri=echo_http_server_post,
            RequestParameters=params,
            PayloadFormatVersion="1.0",
            IntegrationMethod="POST",
        )
        int_id = result["IntegrationId"]

        http_integrations = aws_client.apigatewayv2.get_integrations(ApiId=api_id)["Items"]
        assert len(http_integrations) == 4
        assert (
            len(list(filter(lambda x: (x["IntegrationType"] == "HTTP_PROXY"), http_integrations)))
            == 3
        )

        result = aws_client.apigatewayv2.get_routes(ApiId=api_id)["Items"]
        for route in result:
            aws_client.apigatewayv2.update_route(
                ApiId=api_id, RouteId=route["RouteId"], Target=f"integrations/{int_id}"
            )

        aws_client.apigatewayv2.create_stage(ApiId=api_id, StageName="$default", AutoDeploy=True)

        def invoke_api():
            endpoint = api_invoke_url(api_id=api_id, stage="$default", path="/pets")
            result = requests.get(endpoint)
            assert result.ok
            response = json.loads(to_str(result.content))
            return response.get("headers")

        headers = retry(invoke_api, retries=10, sleep=1)
        snapshot.match("http-proxy-request-header-parameters", headers)

    @markers.aws.unknown
    def test_v2_dynamic_proxy_paths(self, create_v2_api, tmp_http_server, aws_client):
        test_port, invocations = tmp_http_server

        # create API
        api_name = f"api-{short_uid()}"
        result = create_v2_api(Name=api_name, ProtocolType="HTTP")
        api_id = result["ApiId"]

        # create integration
        result = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            IntegrationUri="http://localhost:%s/{proxy}" % test_port,
            PayloadFormatVersion="1.0",
            IntegrationMethod="ANY",
        )
        int_id = result["IntegrationId"]

        # create routes
        aws_client.apigatewayv2.create_route(
            ApiId=api_id, RouteKey="GET /{proxy+}", Target=f"integrations/{int_id}"
        )
        aws_client.apigatewayv2.create_route(
            ApiId=api_id, RouteKey="POST /my/param/{proxy}/1", Target=f"integrations/{int_id}"
        )

        aws_client.apigatewayv2.create_stage(ApiId=api_id, StageName="$default", AutoDeploy=True)
        # create custom stage (in addition to $default stage)
        stage_name = "stage1"
        aws_client.apigatewayv2.create_stage(ApiId=api_id, StageName=stage_name, AutoDeploy=True)

        # invoke with path using custom stage
        url = host_based_url(api_id, path="/my/test/1?p1", stage_name=stage_name)
        assert stage_name in url
        result = requests.get(url)
        assert result.status_code == 200
        # invoke with alternative path, using default stage
        url = host_based_url(api_id, path="/my/test/2?p2=2")
        result = requests.get(url)
        assert result.status_code == 200
        # invoke with alternative path, using single "{proxy}" path param
        url = host_based_url(api_id, path="/my/param/test6427/1?p3=3")
        result = requests.post(url)
        assert result.status_code == 200
        # invoke with a non-matching path, should return 404/error response
        url = host_based_url(api_id, path="/foobar")
        result = requests.post(url)
        assert result.status_code == 404

        # assert that invocations with correct paths have been received
        paths = [get_full_raw_path(inv) for inv in invocations]
        assert paths == ["/my/test/1?p1=", "/my/test/2?p2=2", "/test6427?p3=3"]

    @markers.aws.unknown
    def test_v2_status_code_mappings(self, create_v2_api, httpserver: HTTPServer, aws_client):
        def _handler(_request: Request) -> WerkzeugResponse:
            response_data = _request.get_data(as_text=True)
            if "large" in _request.path:
                response_data = response_data + "test123 test456 test789" * 100000
            response_content = {
                "method": _request.method,
                "path": _request.path,
                "data": response_data,
                "headers": dict(_request.headers),
            }
            status_code = int(_request.path.split("/")[-1])
            return WerkzeugResponse(
                json.dumps(response_content), mimetype="application/json", status=status_code
            )

        httpserver.expect_request("").respond_with_handler(_handler)
        uri = httpserver.url_for("/{proxy}")

        # create API
        api_name = f"api-{short_uid()}"
        result = create_v2_api(Name=api_name, ProtocolType="HTTP")
        api_id = result["ApiId"]

        # create integration
        result = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            IntegrationUri=uri,
            ResponseParameters={"201": {"overwrite:statuscode": "202"}},
            PayloadFormatVersion="1.0",
            IntegrationMethod="ANY",
        )
        int_id = result["IntegrationId"]

        # create routes
        aws_client.apigatewayv2.create_route(
            ApiId=api_id, RouteKey="GET /{proxy+}", Target=f"integrations/{int_id}"
        )
        aws_client.apigatewayv2.create_stage(ApiId=api_id, StageName="$default", AutoDeploy=True)

        # invoke with different expected status codes
        for code in [200, 201, 400, 403]:
            for payload in ["normal", "large"]:
                url = host_based_url(api_id, path=f"/test/{payload}/{code}")
                result = requests.get(url)
                expected = code + 1 if code % 100 == 1 else code
                assert result.status_code == expected

    # TODO remove when migrating to Next Gen
    @markers.aws.unknown
    @pytest.mark.skipif(
        is_aws_cloud() or is_next_gen_api(),
        reason="This test is making wrong assumption that you can create a request authorizer without payload format",
    )
    def test_lambda_authorizer_with_no_payload_format_version(
        self,
        create_v2_api,
        create_lambda_function,
        aws_client,
        region_name,
    ):
        # creates HTTP API
        result = create_v2_api(ProtocolType="HTTP", Name=f"{short_uid()}")
        api_id = result["ApiId"]

        # creates the lambda authorizer
        lambda_name = f"auth-{short_uid()}"
        lambda_code = LAMBDA_REQUEST_AUTH % "2.0"
        zip_file = testutil.create_lambda_archive(lambda_code, get_content=True)
        lambda_arn = create_lambda_function(func_name=lambda_name, zip_file=zip_file)[
            "CreateFunctionResponse"
        ]["FunctionArn"]
        auth_url = arns.apigateway_invocations_arn(lambda_arn, region_name)

        authorizer_id = aws_client.apigatewayv2.create_authorizer(
            Name="lambda-authorizer",
            ApiId=api_id,
            AuthorizerUri=auth_url,
            AuthorizerType="REQUEST",
            IdentitySource=["$request.header.x-user"],
            EnableSimpleResponses=True,
        )["AuthorizerId"]

        # creates the lambda integration
        lambda_name = f"int-{short_uid()}"
        lambda_arn = create_lambda_function(
            handler_file=LAMBDA_JS % "nice", func_name=lambda_name, runtime=Runtime.nodejs20_x
        )["CreateFunctionResponse"]["FunctionArn"]

        integration_id = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="AWS_PROXY",
            PayloadFormatVersion="2.0",
            IntegrationMethod="ANY",
            IntegrationUri=lambda_arn,
        )["IntegrationId"]

        # creates the /example/{proxy+} route
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="CUSTOM",
            AuthorizerId=authorizer_id,
            RouteKey="POST /example/{proxy+}",
            Target=f"integrations/{integration_id}",
        )

        # assert responses
        endpoint = api_invoke_url(api_id=api_id, stage="$default", path="/example/test")

        result = requests.post(endpoint, headers={"X-User": "invalid-user"}, verify=False)
        assert result.status_code == 403

        # tests for valid authorization
        result = requests.request("POST", endpoint, headers={"X-User": "user"}, verify=False)
        assert result.status_code == 200
        assert to_str(result.content) == "I am a nice API!"

        # tests for missing headers
        result = requests.request("POST", endpoint, headers={}, verify=False)
        assert result.status_code == 401
        assert to_str(result.content) == '{"message": "Unauthorized"}'

    @markers.aws.validated
    @pytest.mark.parametrize("payload_format", ["1.0", "2.0"])
    def test_lambda_events_with_authorizer(
        self,
        create_v2_api,
        create_lambda_function,
        add_permission_for_integration_lambda,
        payload_format,
        snapshot,
        aws_client,
        region_name,
    ):
        result = create_v2_api(ProtocolType="HTTP", Name=f"{short_uid()}")
        api_id = result["ApiId"]

        lambda_name = f"auth-{short_uid()}"
        lambda_code = LAMBDA_REQUEST_AUTH % payload_format
        zip_file = testutil.create_lambda_archive(lambda_code, get_content=True)
        result = create_lambda_function(func_name=lambda_name, zip_file=zip_file)
        lambda_arn = result["CreateFunctionResponse"]["FunctionArn"]
        auth_url = arns.apigateway_invocations_arn(lambda_arn, region_name)
        add_permission_for_integration_lambda(api_id, lambda_arn)

        kwargs = {} if payload_format == "1.0" else {"EnableSimpleResponses": True}
        authorizer_id = aws_client.apigatewayv2.create_authorizer(
            ApiId=api_id,
            AuthorizerType="REQUEST",
            AuthorizerUri=auth_url,
            AuthorizerPayloadFormatVersion=payload_format,
            Name=f"lambda-auth-{short_uid()}",
            IdentitySource=["$request.header.X-User"],
            **kwargs,
        )["AuthorizerId"]

        lambda_name = f"int-{short_uid()}"
        result = create_lambda_function(
            handler_file=LAMBDA_ECHO_EVENT, func_name=lambda_name, runtime=Runtime.nodejs20_x
        )
        lambda_arn = result["CreateFunctionResponse"]["FunctionArn"]
        add_permission_for_integration_lambda(api_id, lambda_arn)

        path = "/example/test"
        integration_id = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="AWS_PROXY",
            PayloadFormatVersion=payload_format,
            IntegrationMethod="ANY",
            IntegrationUri=lambda_arn,
        )["IntegrationId"]
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="CUSTOM",
            AuthorizerId=authorizer_id,
            RouteKey=f"POST {path}",
            Target=f"integrations/{integration_id}",
        )

        # create deployment
        stage_name = "test-stage"
        create_deployment(aws_client.apigatewayv2, api_id, stage_name=stage_name)

        endpoint = api_invoke_url(api_id=api_id, stage=stage_name, path=path)

        result = requests.post(endpoint, headers={"X-User": "user"}, verify=False)
        request_context = json.loads(result.content).get("requestContext", {})

        assert result.status_code == 200
        auth_req_context = request_context.get("authorizer")
        snapshot.match("auth-request-ctx", auth_req_context)

    @markers.aws.validated
    def test_cors_preflight_requests(
        self,
        create_v2_api,
        create_lambda_function,
        add_permission_for_integration_lambda,
        aws_client,
    ):
        # TODO: remove in favor of CORS tests
        result = create_v2_api(
            ProtocolType="HTTP",
            Name=f"{short_uid()}",
            CorsConfiguration={
                "AllowCredentials": False,
                "AllowHeaders": [
                    "content-type",
                ],
                "AllowMethods": [
                    "GET",
                    "POST",
                    "PUT",
                    "PATCH",
                    "DELETE",
                    "OPTIONS",
                ],
                "AllowOrigins": ["http://localhost:4566", "https://lwn.net"],
                "MaxAge": 0,
            },
        )
        api_id = result["ApiId"]
        endpoint = result["ApiEndpoint"]

        func_name = f"func_{short_uid()}"
        zip_file = testutil.create_lambda_archive(
            LAMBDA_ECHO_EVENT, get_content=True, runtime=Runtime.nodejs20_x
        )
        create_lambda_function(func_name=func_name, zip_file=zip_file, runtime=Runtime.nodejs20_x)
        lambda_arn = aws_client.lambda_.get_function(FunctionName=func_name)["Configuration"][
            "FunctionArn"
        ]
        add_permission_for_integration_lambda(api_id, lambda_arn)

        integration_id = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="AWS_PROXY",
            PayloadFormatVersion="2.0",
            IntegrationMethod="ANY",
            IntegrationUri=lambda_arn,
        )["IntegrationId"]
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="NONE",
            RouteKey="POST /test",
            Target=f"integrations/{integration_id}",
        )

        aws_client.apigatewayv2.create_stage(ApiId=api_id, StageName="$default", AutoDeploy=True)

        endpoint = api_invoke_url(api_id=api_id, path="/test")

        # CORS Regular Request
        def validate_regular_request():
            response = requests.post(endpoint, headers={"Origin": "https://lwn.net"})
            assert response.status_code == 200
            assert "https://lwn.net" in response.headers["Access-Control-Allow-Origin"]

        retry(validate_regular_request, retries=5, sleep=1)

        # CORS Preflight Request
        def validate_preflight_request():
            preflight_response = requests.options(
                endpoint,
                headers={
                    "Origin": "https://lwn.net",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type",
                },
            )
            assert preflight_response.status_code == 204
            assert "https://lwn.net" in preflight_response.headers["Access-Control-Allow-Origin"]
            assert all(
                r in ["HEAD", "GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
                for r in preflight_response.headers["Access-Control-Allow-Methods"].split(",")
            )
            assert "content-type" in preflight_response.headers["Access-Control-Allow-Headers"]

        retry(validate_preflight_request, retries=5, sleep=1)

    # TODO:
    # - HTTP_PROXY snapshot tests implemented on https://github.com/localstack/localstack-ext/pull/1491
    @markers.aws.unknown
    @pytest.mark.skipif(
        is_next_gen_api(),
        reason="Not properly implemented nor validated, can be removed when switching to NextGen",
    )
    def test_apigw_v2_http_jwt_authorizer(
        self,
        create_v2_api,
        create_user_pool_client,
        httpserver: HTTPServer,
        aws_client,
        region_name,
        trigger_lambda_pre_token,
    ):
        scopes = ["openid", "email"]
        user_pool_result = create_user_pool_client(
            pool_kwargs={
                "UserPoolAddOns": {"AdvancedSecurityMode": "ENFORCED"},
                "LambdaConfig": {
                    "PreTokenGenerationConfig": {
                        "LambdaArn": trigger_lambda_pre_token,
                        "LambdaVersion": "V2_0",
                    }
                },
            },
            client_kwargs={
                "AllowedOAuthScopes": scopes,
                "AllowedOAuthFlows": ["code", "implicit"],
                "CallbackURLs": ["https://example.com"],
                "ExplicitAuthFlows": ["USER_PASSWORD_AUTH"],
                "SupportedIdentityProviders": ["COGNITO"],
                "AllowedOAuthFlowsUserPoolClient": True,
            },
        )
        cognito_client_id = user_pool_result.pool_client["ClientId"]
        cognito_pool_id = user_pool_result.user_pool["Id"]
        domain_name = f"ls-{short_uid()}"
        aws_client.cognito_idp.create_user_pool_domain(
            Domain=domain_name, UserPoolId=cognito_pool_id
        )
        user_pool_result.user_pool["Domain"] = domain_name

        # create resource server and custom Cognito scopes
        aws_client.cognito_idp.create_resource_server(
            UserPoolId=cognito_pool_id,
            Identifier="http://example.com",
            Name="ressrv1",
            Scopes=[{"ScopeName": "scope1", "ScopeDescription": "test scope 1"}],
        )
        kwargs = remove_attributes(
            dict(user_pool_result.pool_client), ["CreationDate", "LastModifiedDate"]
        )
        custom_scopes = ["http://example.com/scope1"]
        kwargs["AllowedOAuthScopes"] = scopes + custom_scopes
        aws_client.cognito_idp.update_user_pool_client(**kwargs)

        # create http api
        result = create_v2_api(ProtocolType="HTTP", Name=f"{short_uid()}")
        api_id = result["ApiId"]

        issuer_domain = config.external_service_url()
        if is_aws_cloud():
            issuer_domain = (
                f"https://cognito-idp.{aws_client.cognito_idp.meta.region_name}.amazonaws.com"
            )

        authorizer_id = aws_client.apigatewayv2.create_authorizer(
            Name="jwt-authorizer",
            ApiId=api_id,
            AuthorizerType="JWT",
            JwtConfiguration={
                "Audience": [cognito_client_id],
                "Issuer": f"{issuer_domain}/{cognito_pool_id}",
            },
            IdentitySource=["$request.header.Authorization"],
        )["AuthorizerId"]
        if is_aws_cloud():
            uri = "https://httpbin.org/anything"
        else:

            def _handler(_request: Request) -> WerkzeugResponse:
                response_content = {
                    "method": _request.method,
                    "path": _request.path,
                    "query": _request.query_string.decode("utf-8"),
                    "data": _request.get_data(as_text=True),
                    "headers": dict(_request.headers),
                }
                return WerkzeugResponse(
                    json.dumps(response_content), mimetype="application/json", status=200
                )

            httpserver.expect_request("").respond_with_handler(_handler)
            uri = httpserver.url_for("/")

        result = aws_client.apigatewayv2.create_integration(
            ApiId=result["ApiId"],
            IntegrationType="HTTP_PROXY",
            IntegrationMethod="ANY",
            PayloadFormatVersion="1.0",  # HTTP_PROXY only supports 1.0
            RequestParameters={
                "append:header.UseToken": "$context.authorizer.claims.token_use",
                "append:header.Scope": "$context.authorizer.claims.scope",
                "append:header.Username": "$context.authorizer.jwt.claims.username",
                "append:header.Sub": "$context.authorizer.claims.sub",
                "append:header.ApiId": "$context.apiId",
                "append:querystring.foo": "bar",
                "append:querystring.bash": "bosh",
                "overwrite:path": "/changed/path",
            },
            IntegrationUri=uri,
        )
        int_id = result["IntegrationId"]
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="JWT",
            AuthorizerId=authorizer_id,
            AuthorizationScopes=["http://example.com/scope1"],
            RouteKey="POST /test/{proxy+}",
            Target=f"integrations/{int_id}",
        )
        # create deployment
        stage_name = "dev"
        create_deployment(aws_client.apigatewayv2, api_id, stage_name=stage_name)

        # assert responses
        endpoint = api_invoke_url(api_id=api_id, stage=stage_name, path="/test/foobar")
        result = requests.post(endpoint, headers={"Authorization": ""}, verify=False)
        assert result.status_code == 401
        assert to_str(result.content) == '{"message":"Unauthorized"}'

        # get auth token
        password = "Test123!"
        username = "user@domain.com"
        aws_client.cognito_idp.sign_up(
            ClientId=cognito_client_id,
            Username=username,
            Password=password,
        )
        aws_client.cognito_idp.admin_confirm_sign_up(UserPoolId=cognito_pool_id, Username=username)
        _, access_token = get_auth_token_via_login_form(
            user_pool_result.user_pool,
            user_pool_result.pool_client,
            username=username,
            password=password,
            region_name=region_name,
            scope="openid email http://example.com/scope1",
        )

        endpoint = api_invoke_url(api_id=api_id, stage=stage_name, path="/test/foo")
        result = requests.post(endpoint, headers={"Authorization": access_token}, verify=False)
        body = result.json()

        assert result.status_code == 200

        headers = body["headers"]
        query = body["query"]
        path = body["path"]
        scopes = headers["Scope"].split()

        # assert headers
        assert headers["Usetoken"] == "access"
        assert "http://example.com/scope1" in scopes
        assert headers["Apiid"] == api_id
        assert headers["Sub"]
        assert not headers["Username"]
        # assert query
        assert query == "foo=bar&bash=bosh"
        # assert path
        assert path == "/changed/path"


class TestImportAPIs:
    @markers.aws.unknown
    def test_import_apis(self, aws_client):
        client = aws_client.apigatewayv2
        api_spec = load_file(API_SPEC_FILE)

        def run_asserts(api_id):
            result = client.get_models(ApiId=api_id)["Items"]
            model_names = [m["Name"] for m in result]
            assert len(model_names) == 6
            for name in ["Pets", "Pet", "PetType", "NewPet"]:
                assert name in model_names

            all_routes = client.get_routes(ApiId=api_id)["Items"]
            routes = [r["RouteKey"] for r in all_routes]
            assert len(routes) == 3
            for route in ["GET /pets", "POST /pets", "GET /pets/{petId}"]:
                assert route in routes

            result = client.get_authorizers(ApiId=api_id)["Items"]
            authorizer = [a for a in result if a["Name"] == "my-auth-gw-imported"]
            assert len(authorizer) == 1
            assert authorizer[0].get("IdentitySource") == ["route.request.header.Authorization"]
            protected_route = [r for r in all_routes if r["RouteKey"] == "GET /pets/{petId}"][0]
            assert authorizer[0].get("AuthorizerId") == protected_route.get("AuthorizerId")

            integrations = aws_client.apigatewayv2.get_integrations(ApiId=api_id)["Items"]
            assert len(integrations) == 3
            aws_proxy_integration = filter(
                lambda x: (x["IntegrationType"] == "AWS_PROXY"), integrations
            )
            assert next(aws_proxy_integration)["PayloadFormatVersion"] == "2.0"

        # import API
        result = client.import_api(Basepath="/", Body=api_spec)
        api_id = result["ApiId"]
        run_asserts(api_id)

        # re-import API
        client.reimport_api(ApiId=api_id, Body=api_spec)
        run_asserts(api_id)

        # clean up
        client.delete_api(ApiId=api_id)
