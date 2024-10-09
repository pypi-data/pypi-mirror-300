import json
import textwrap
from typing import Any

import pytest
import requests
import urllib3
from botocore.auth import SigV4Auth
from localstack.aws.api.lambda_ import Runtime
from localstack.pro.core.services.cognito_idp.cognito_utils import (
    get_auth_token_via_login_form,
    get_issuer_url,
)
from localstack.testing.aws.util import is_aws_cloud
from localstack.testing.pytest import markers
from localstack.utils.aws import arns
from localstack.utils.strings import short_uid
from localstack.utils.sync import retry
from tests.aws.services.apigateway.apigateway_fixtures import api_invoke_url
from tests.aws.services.apigateway.conftest import LAMBDA_ECHO_EVENT, is_next_gen_api
from tests.aws.services.apigatewayv2.conftest import (
    LAMBDA_AUTHORIZER_IAM_RESPONSE,
    LAMBDA_AUTHORIZER_V2_SIMPLE_RESPONSE,
)


@pytest.fixture
def trigger_lambda_pre_token(create_lambda_with_invocation_forwarding):
    lambda_source = textwrap.dedent(
        """
    def handler(event, *args):
        trigger, response, request = event['triggerSource'], event['response'], event['request']
        response["claimsAndScopeOverrideDetails"] = {
            "accessTokenGeneration": {
                "scopesToAdd": ["http://example.com/scope1"],
            },
        }
        return event
       """
    )
    return create_lambda_with_invocation_forwarding(lambda_source=lambda_source)


class TestIAMAuthorization:
    @markers.aws.validated
    @pytest.mark.skipif(
        condition=not is_next_gen_api() and not is_aws_cloud(),
        reason="Incomplete behavior in legacy implementation",
    )
    def test_iam_authorization_missing_token(
        self, create_v2_api, aws_client, apigw_echo_http_server_anything
    ):
        # create HTTP API
        result = create_v2_api(ProtocolType="HTTP", Name=f"test-iam-auth-{short_uid()}")
        api_id = result["ApiId"]

        integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            IntegrationUri=apigw_echo_http_server_anything,
            PayloadFormatVersion="1.0",
            IntegrationMethod="ANY",
        )
        integration_id = integration["IntegrationId"]
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="ANY /",
            AuthorizationType="AWS_IAM",
            Target=f"integrations/{integration_id}",
        )
        aws_client.apigatewayv2.create_stage(ApiId=api_id, StageName="$default", AutoDeploy=True)

        url = api_invoke_url(api_id=api_id)

        def _invoke_url(invoke_url: str, headers: dict):
            invoker_response = requests.get(invoke_url, headers=headers)
            assert invoker_response.status_code == 403
            assert invoker_response.json() == {"message": "Forbidden"}

        default_retry_kwargs = {
            "function": _invoke_url,
            "retries": 5,
            "sleep": 2,
            "invoke_url": url,
        }

        no_token_headers = {}
        retry(headers=no_token_headers, **default_retry_kwargs)

        wrong_auth_headers = {"Authorization": "Bearer invalid-token"}
        retry(headers=wrong_auth_headers, **default_retry_kwargs)

        wrong_auth_headers = {"Authorization": "invalid-token bla=test"}
        retry(headers=wrong_auth_headers, **default_retry_kwargs)

        wrong_auth_headers = {"Authorization": "Bearer invalid-token-bla=test"}
        retry(headers=wrong_auth_headers, **default_retry_kwargs)

        wrong_auth_headers = {
            "Authorization": "Credential=AKIAIOSFODNN7EXAMPLE/20130524/us-east-1/s3/aws4_request"
        }
        retry(headers=wrong_auth_headers, **default_retry_kwargs)

        wrong_auth_headers = {"Authorization": "Signature=random"}
        retry(headers=wrong_auth_headers, **default_retry_kwargs)

        wrong_auth_headers = {
            "Authorization": "AWS4-HMAC-SHA256 Credential=AKIAIOSFODNN7EXAMPLE/20130524/us-east-1/s3/aws4_request"
        }
        retry(headers=wrong_auth_headers, **default_retry_kwargs)

    @markers.snapshot.skip_snapshot_verify(
        paths=[
            # Not included by aws
            "$..body.headers.Accept",
            # TODO pop Authorization header in the integration. Validate if it should always be done
            #  or only when authorizers are configured
            "$..body.headers.Authorization",
            # TODO add X-Amz-Security-Token header
            "$..body.headers.X-Amz-Security-Token",
        ]
    )
    @pytest.mark.skipif(
        condition=not is_next_gen_api() and not is_aws_cloud(),
        reason="Incomplete behavior in legacy implementation",
    )
    @markers.aws.validated
    def test_iam_authorizer_success(
        self,
        aws_client,
        region_name,
        create_v2_api,
        apigw_echo_http_server_anything,
        apigwv2_httpbin_headers_transformers,
        aws_http_client_factory,
        snapshot,
    ):
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("Request-Authorization"),
                snapshot.transform.key_value("Context-Accesskey"),
                snapshot.transform.key_value("Context-Userarn"),
                snapshot.transform.key_value("Context-Caller"),
                snapshot.transform.key_value("X-Amz-Date"),
                snapshot.transform.key_value("X-Amz-Security-Token"),
            ],
        )

        # create HTTP API
        result = create_v2_api(ProtocolType="HTTP", Name=f"test-iam-auth-{short_uid()}")
        api_id = result["ApiId"]

        # create route with iam authorizer
        integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            IntegrationUri=apigw_echo_http_server_anything,
            PayloadFormatVersion="1.0",
            IntegrationMethod="ANY",
            RequestParameters={
                "append:header.Request-Authorization": "$request.header.Authorization",
                "append:header.Context-AccountId": "$context.identity.accountId",
                "append:header.Context-Caller": "$context.identity.caller",
                "append:header.Context-User": "$context.identity.user",
                "append:header.Context-UserArn": "$context.identity.userArn",
                "append:header.Context-AccessKey": "$context.identity.accessKey",
            },
        )
        integration_id = integration["IntegrationId"]
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="ANY /",
            AuthorizationType="AWS_IAM",
            Target=f"integrations/{integration_id}",
        )
        aws_client.apigatewayv2.create_stage(ApiId=api_id, StageName="$default", AutoDeploy=True)

        invalid_headers = {"Authorization": "Bearer invalid-token"}

        invoke_url = api_invoke_url(api_id=api_id)

        apigw_http_client = aws_http_client_factory(
            "execute-api", signer_factory=SigV4Auth, region=region_name
        )

        def _invoke(expected_status_code: int, http_client=None, headers: dict = None):
            headers = headers or {}
            headers["user-agent"] = "user-agent"
            invoker_response = http_client.get(invoke_url, headers=headers)
            assert invoker_response.status_code == expected_status_code
            return {"status_code": invoker_response.status_code, "body": invoker_response.json()}

        response = retry(
            lambda: _invoke(expected_status_code=403, http_client=requests, headers=invalid_headers)
        )
        snapshot.match("unauthorized-request", response)

        response = retry(lambda: _invoke(expected_status_code=200, http_client=apigw_http_client))
        snapshot.match("authorized-request", response)


class TestHttpApiLambdaAuthorizer:
    @pytest.fixture
    def register_authorizer_snapshot_transformers(self, snapshot):
        def _register(payload_version):
            snapshot.add_transformers_list(
                [
                    snapshot.transform.key_value("domainName"),
                    snapshot.transform.key_value("apiId"),
                    snapshot.transform.key_value("sourceIp"),
                ]
            )
            if payload_version == "1.0":
                snapshot.add_transformers_list(
                    [
                        snapshot.transform.key_value("Host"),
                        snapshot.transform.key_value("X-Amzn-Trace-Id"),
                        snapshot.transform.key_value("X-Forwarded-For"),
                        snapshot.transform.key_value("X-Forwarded-Port"),
                        snapshot.transform.key_value("extendedRequestId"),
                        snapshot.transform.key_value(
                            "requestTime",
                            reference_replacement=False,
                            value_replacement="<request-time>",
                        ),
                        snapshot.transform.key_value(
                            "requestTimeEpoch",
                            reference_replacement=False,
                            value_replacement="<request-time-epoch>",
                        ),
                        snapshot.transform.key_value(
                            "X-Forwarded-Proto",
                            reference_replacement=False,
                            value_replacement="<x-forwarded-proto>",
                        ),
                    ]
                )
            else:
                snapshot.add_transformers_list(
                    [
                        snapshot.transform.key_value("host"),
                        snapshot.transform.key_value("x-amzn-trace-id"),
                        snapshot.transform.key_value("x-forwarded-for"),
                        snapshot.transform.key_value("x-forwarded-port"),
                        snapshot.transform.key_value("extendedRequestId"),
                        snapshot.transform.key_value("requestId"),
                        snapshot.transform.key_value(
                            "requestTime",
                            reference_replacement=False,
                            value_replacement="<request-time>",
                        ),
                        snapshot.transform.key_value(
                            "time",
                            reference_replacement=False,
                            value_replacement="<time>",
                        ),
                        snapshot.transform.key_value(
                            "timeEpoch",
                            reference_replacement=False,
                            value_replacement="<request-time-epoch>",
                        ),
                        snapshot.transform.key_value(
                            "x-forwarded-proto",
                            reference_replacement=False,
                            value_replacement="<x-forwarded-proto>",
                        ),
                    ]
                )

        return _register

    @pytest.mark.parametrize(
        "payload_format_version", [("1.0", False), ("2.0", True), ("2.0", False)]
    )
    @markers.snapshot.skip_snapshot_verify(
        # TODO validate if added by aws, or simply not removed?
        paths=["$..body.event.headers.Content-Length", "$..body.event.headers.content-length"]
    )
    @pytest.mark.skipif(
        not is_next_gen_api() and not is_aws_cloud(),
        reason="Incomplete behavior in legacy implementation",
    )
    @markers.aws.validated
    def test_request_authorizer_http(
        self,
        payload_format_version,
        create_lambda_authorizer,
        aws_client,
        snapshot,
        create_v2_api,
        add_permission_for_integration_lambda,
        apigw_echo_http_server_anything,
        register_authorizer_snapshot_transformers,
    ):
        payload_version, simple_response = payload_format_version
        register_authorizer_snapshot_transformers(payload_version)

        # create HTTP API
        result = create_v2_api(ProtocolType="HTTP", Name=f"test-iam-auth-{short_uid()}")
        api_id = result["ApiId"]

        # create lambda authorizer function
        lambda_arn, invoke_arn = create_lambda_authorizer(
            LAMBDA_AUTHORIZER_V2_SIMPLE_RESPONSE
            if simple_response
            else LAMBDA_AUTHORIZER_IAM_RESPONSE
        )
        add_permission_for_integration_lambda(api_id, lambda_arn)

        # create lambda authorizer
        authorizer = aws_client.apigatewayv2.create_authorizer(
            ApiId=api_id,
            AuthorizerType="REQUEST",
            IdentitySource=[
                "$request.header.x-user",
                "$request.querystring.qs",
                "$stageVariables.stage",
            ],
            Name=f"lambda-auth-{short_uid()}",
            AuthorizerPayloadFormatVersion=payload_version,
            AuthorizerUri=invoke_arn,
            EnableSimpleResponses=simple_response,
        )

        # create integration
        integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            IntegrationUri=apigw_echo_http_server_anything,
            PayloadFormatVersion="1.0",
            IntegrationMethod="ANY",
            ResponseParameters={
                "200": {
                    "append:header.event": "$context.authorizer.event",
                    # Adding principalId as the doc mentions it being populated for
                    # lambda authorizer, but it isn't populated
                    "append:header.principal-id": "$context.identity.principalId",
                }
            },
        )
        integration_id = integration["IntegrationId"]
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="ANY /",
            AuthorizationType="CUSTOM",
            AuthorizerId=authorizer["AuthorizerId"],
            Target=f"integrations/{integration_id}",
        )

        # create stage
        aws_client.apigatewayv2.create_stage(
            ApiId=api_id,
            StageName="$default",
            AutoDeploy=True,
            StageVariables={"stage": "stage_value"},
        )

        invoke_url = api_invoke_url(api_id=api_id)

        def invoke_api(headers, querystring, expected_status_code):
            _response = requests.get(
                invoke_url, params=querystring, headers={"user-agent": "python-user", **headers}
            )
            assert _response.status_code == expected_status_code
            return _response

        # Missing querystring in the request
        response = retry(
            lambda: invoke_api(
                headers={"X-User": "allow"}, querystring={}, expected_status_code=401
            ),
            retries=10,
            sleep=1,
        )
        snapshot.match(
            "missing-querystring", {"status_code": response.status_code, "body": response.json()}
        )

        # Missing header in the request
        response = retry(
            lambda: invoke_api(headers={}, querystring={"qs": "any"}, expected_status_code=401),
            retries=10,
            sleep=1,
        )
        snapshot.match(
            "missing-header", {"status_code": response.status_code, "body": response.json()}
        )

        # Complete but denied by the authorizer
        response = retry(
            lambda: invoke_api(
                headers={"X-User": "deny"}, querystring={"qs": "any"}, expected_status_code=403
            ),
            retries=10,
            sleep=1,
        )
        snapshot.match(
            "authorizer-deny", {"status_code": response.status_code, "body": response.json()}
        )

        # Successful
        response = retry(
            lambda: invoke_api(
                headers={"X-User": "allow"}, querystring={"qs": "any"}, expected_status_code=200
            ),
            retries=10,
            sleep=1,
        )

        # Aws returns the identity sources in a random order, sorting them here will allow us to snapshot them
        event = json.loads(response.headers["event"])
        identity_sources = event["identitySource"]
        if payload_version == "1.0":
            identity_sources = ",".join(sorted(identity_sources.split(",")))
            event["identitySource"] = identity_sources
            # payload 1.0 includes both identitySource and authorization token. They appear to be the same
            # TODO add test to confirm they behave the same under different scenarios: casing, multivalues, etc
            authorization_token = event["authorizationToken"]
            event["authorizationToken"] = ",".join(sorted(authorization_token.split(",")))
        else:
            event["identitySource"].sort()

        # we are logging the event headers here as it contains the event passed to the authorizer
        snapshot.match(
            "successful-authorizer",
            {
                "status_code": response.status_code,
                "body": {"event": event},
                "principalId": response.headers.get("principal-id"),
            },
        )

    @markers.aws.validated
    @pytest.mark.parametrize(
        "payload_format_version", [("1.0", False), ("2.0", True), ("2.0", False)]
    )
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            "$..authorizer.event.headers.Content-Length",
            "$..authorizer.lambda.event.headers.content-length",
        ]
    )
    @markers.snapshot.skip_snapshot_verify(
        condition=lambda: not is_next_gen_api(),
        paths=[
            "$..accessKey",
            "$..accountId",
            "$..caller",
            "$..cognitoAmr",
            "$..cognitoAuthenticationProvider",
            "$..cognitoAuthenticationType",
            "$..cognitoIdentityId",
            "$..cognitoIdentityPoolId",
            "$..principalOrgId",
            "$..principalOrgId",
            "$..user",
            "$..userArn",
            "$..authorizer.event.authorizationToken",
            "$..authorizer.event.headers",
            "$..authorizer.event.identitySource",
            "$..authorizer.event.multiValueHeaders",
            "$..authorizer.event.multiValueQueryStringParameters",
            "$..authorizer.event.requestContext.extendedRequestId",
            "$..authorizer.event.identitySource",
            "$..authorizer.event.requestContext.path",
            "$..authorizer.event.requestContext.protocol",
            "$..authorizer.event.requestContext.requestId",
            "$..authorizer.event.requestContext.requestTime",
            "$..authorizer.event.requestContext.requestTimeEpoch",
            "$..authorizer.event.requestContext.resourceId",
            "$..authorizer.lambda.event.cookies",
            "$..authorizer.lambda.event.headers",
            "$..authorizer.lambda.event.pathParameters",
            "$..authorizer.lambda.event.queryStringParameters",
            "$..authorizer.lambda.event.requestContext.authentication",
            "$..authorizer.lambda.event.requestContext.routeKey",
            "$..authorizer.lambda.event.requestContext.time",
            "$..authorizer.lambda.event.routeKey",
            "$..authorizer.lambda.event.stageVariables",
        ],
    )
    def test_request_authorizer_lambda_context(
        self,
        create_v2_api,
        create_lambda_function,
        add_permission_for_integration_lambda,
        snapshot,
        payload_format_version,
        aws_client_factory,
        aws_client,
        region_name,
        create_lambda_authorizer,
        register_authorizer_snapshot_transformers,
    ):
        payload_version, simple_response = payload_format_version
        register_authorizer_snapshot_transformers(payload_version)

        # create http api
        result = create_v2_api(Name=f"test-{short_uid()}", ProtocolType="HTTP")
        api_id = result["ApiId"]

        # create lambda authorizer function
        auth_lambda_arn, auth_invoke_arn = create_lambda_authorizer(
            LAMBDA_AUTHORIZER_V2_SIMPLE_RESPONSE
            if simple_response
            else LAMBDA_AUTHORIZER_IAM_RESPONSE
        )
        add_permission_for_integration_lambda(api_id, auth_lambda_arn)

        authorizer_id = aws_client.apigatewayv2.create_authorizer(
            ApiId=api_id,
            Name=f"test_authorizer-{short_uid()}",
            AuthorizerType="REQUEST",
            AuthorizerPayloadFormatVersion=payload_version,
            EnableSimpleResponses=simple_response,
            IdentitySource=["$request.header.x-user"],
            AuthorizerUri=auth_invoke_arn,
        )["AuthorizerId"]

        # create lambda integration
        lambda_name = f"lambda-test-{short_uid()}"
        lambda_arn = create_lambda_function(
            handler_file=LAMBDA_ECHO_EVENT,
            func_name=lambda_name,
            runtime=Runtime.nodejs20_x,
        )["CreateFunctionResponse"]["FunctionArn"]
        add_permission_for_integration_lambda(api_id, lambda_arn)

        # Thanks to this test. I realised that you can enter a wrong region name for in the invoke arn
        # arn:aws:apigateway:eu-west-1:lambda:path/2015-03-31/functions/<lambda arn>/invocations
        # The eu-west-1 in this case can be any? valid region, even if either the api ot the lambda are in that region
        uri = arns.apigateway_invocations_arn(lambda_arn, region_name="eu-west-1")
        integration_id = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="AWS_PROXY",
            IntegrationMethod="POST",
            IntegrationUri=uri,
            PayloadFormatVersion=payload_version,
        )["IntegrationId"]

        # create GET /test route
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="CUSTOM",
            AuthorizerId=authorizer_id,
            RouteKey="GET /test",
            Target=f"integrations/{integration_id}",
        )
        aws_client.apigatewayv2.create_stage(ApiId=api_id, StageName="$default", AutoDeploy=True)

        private_endpoint = api_invoke_url(api_id=api_id, path="/test")

        def _call_and_assert():
            # we need to use `urllib3` here, because `requests` strip leading slashes following this PR
            # https://github.com/psf/requests/pull/6644
            response = urllib3.request(
                "GET",
                private_endpoint,
                headers={"X-User": "allow", "User-Agent": "urllib3-test"},
            )
            assert response.status == 200

            # lambda authorizer passes the context into the integration lambda
            # the integration lambda returns the context in the response body
            # we can use this to verify that the authorizer rendered the correct identitySource
            context = json.loads(response.data)["requestContext"]
            return {"authorizer": context["authorizer"], "identity": context.get("identity")}

        def remove_multivalue_headers(_result) -> dict[str, Any]:
            # it seems that the list headers might be creating an issue with the snapshot in ci
            # TODO remove this block when removing legacy
            event = json.loads(_result["authorizer"]["event"])
            event.pop("multiValueHeaders")
            _result["authorizer"]["event"] = event
            return _result

        result = retry(_call_and_assert, retries=10, sleep=2)
        if not (is_aws_cloud() or is_next_gen_api()) and payload_version == "1.0":
            result = remove_multivalue_headers(result)
        snapshot.match("lambda_request_authorizer", result)

        # testing double slash in path
        private_endpoint = api_invoke_url(api_id=api_id, path="//test")
        result = retry(_call_and_assert, retries=10, sleep=2)
        if not (is_aws_cloud() or is_next_gen_api()) and payload_version == "1.0":
            result = remove_multivalue_headers(result)
        snapshot.match("lambda_request_authorizer_double_slash", result)


class TestHttpApiJwtAuthorizer:
    @pytest.fixture
    def create_cognito_pool_and_domain(self, aws_client, create_user_pool_client):
        def _create(
            domain_name: str, extra_scopes: list[str] = None, lambda_trigger_arn: str = None
        ):
            scopes = ["openid", "email"]
            pool_kwargs = {
                "UserPoolAddOns": {"AdvancedSecurityMode": "ENFORCED"},
            }
            if extra_scopes:
                scopes.extend(extra_scopes)
            if lambda_trigger_arn:
                pool_kwargs["LambdaConfig"] = {
                    "PreTokenGenerationConfig": {
                        "LambdaArn": lambda_trigger_arn,
                        "LambdaVersion": "V2_0",
                    }
                }

            user_pool_result = create_user_pool_client(
                pool_kwargs=pool_kwargs,
                client_kwargs={
                    "AllowedOAuthScopes": scopes,
                    "AllowedOAuthFlows": ["code", "implicit"],
                    "CallbackURLs": ["https://example.com"],
                    "SupportedIdentityProviders": ["COGNITO"],
                    "AllowedOAuthFlowsUserPoolClient": True,
                },
            )
            user_pool = user_pool_result.user_pool
            user_pool_id = user_pool["Id"]

            # Create a Domain
            aws_client.cognito_idp.create_user_pool_domain(
                Domain=domain_name, UserPoolId=user_pool_id
            )
            user_pool["Domain"] = domain_name

            return user_pool_result

        return _create

    @markers.snapshot.skip_snapshot_verify(
        paths=[
            # AWS has a second of delay between `auth_time` and `iat`
            "$..claims.iat",
            # AWS populates for access token but LS Cognito doesn't
            "$..claims.version",
            # AWS populates for id token but LS Cognito doesn't
            "$..claims.at_hash",
            "$..claims.jti",
            '$..claims["cognito:user_status"]',
        ]
    )
    # wrong implementation in legacy
    @markers.snapshot.skip_snapshot_verify(condition=lambda: not is_next_gen_api())
    @markers.aws.validated
    @pytest.mark.parametrize("payload_format", ["1.0", "2.0"])
    def test_jwt_authorizer_lambda_target(
        self,
        payload_format,
        create_v2_api,
        add_permission_for_integration_lambda,
        create_lambda_function,
        aws_client,
        region_name,
        trigger_lambda_pre_token,
        snapshot,
        create_cognito_pool_and_domain,
    ):
        if is_next_gen_api() or is_aws_cloud():
            # TODO remove this check when migrating away from legacy
            #  Legacy is returning `int` for many, which fails the transformer. Along with other shape mismatch.
            #  The previous test wasn't snapshotting either, probably for the same reasons
            snapshot.add_transformers_list(
                [
                    snapshot.transform.key_value("audience"),
                    snapshot.transform.key_value("issuer-url"),
                    snapshot.transform.key_value("auth_time"),
                ],
                priority=-1,
            )
            snapshot.add_transformers_list(
                [
                    snapshot.transform.key_value("AuthorizerId"),
                    snapshot.transform.key_value("sourceIp"),
                    snapshot.transform.key_value("sub"),
                    snapshot.transform.key_value("iat"),
                    snapshot.transform.key_value("exp"),
                    snapshot.transform.key_value("jti"),
                    snapshot.transform.key_value("at_hash"),
                ]
            )

        # Create user pool and client
        domain_name = f"ls-{short_uid()}"
        user_pool_result = create_cognito_pool_and_domain(
            domain_name=domain_name,
            extra_scopes=["http://example.com/scope1"],
            lambda_trigger_arn=trigger_lambda_pre_token,
        )
        user_pool = user_pool_result.user_pool
        app_client = user_pool_result.pool_client

        user_pool_id = user_pool["Id"]
        app_client_id = app_client["ClientId"]

        result = create_v2_api(ProtocolType="HTTP", Name=f"api-{short_uid()}")
        api_id = result["ApiId"]

        if is_aws_cloud():
            issuer = f"https://cognito-idp.{region_name}.amazonaws.com/{user_pool_id}"
        else:
            issuer = get_issuer_url(pool_id=user_pool_id)

        snapshot.match("audience", app_client_id)
        snapshot.match("issuer-url", issuer)

        authorizer = aws_client.apigatewayv2.create_authorizer(
            Name="jwt-authorizer",
            ApiId=api_id,
            AuthorizerType="JWT",
            JwtConfiguration={
                "Audience": [app_client_id],
                "Issuer": issuer,
            },
            IdentitySource=["$request.header.Authorization"],
        )
        authorizer_id = authorizer["AuthorizerId"]
        snapshot.match("create-authorizer", authorizer)

        # creates a lambda integration
        lambda_name = f"int-{short_uid()}"
        lambda_arn = create_lambda_function(
            handler_file=LAMBDA_ECHO_EVENT, func_name=lambda_name, runtime=Runtime.nodejs20_x
        )["CreateFunctionResponse"]["FunctionArn"]
        add_permission_for_integration_lambda(api_id=api_id, lambda_arn=lambda_arn)

        integration_id = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="AWS_PROXY",
            PayloadFormatVersion=payload_format,
            IntegrationMethod="POST",
            IntegrationUri=lambda_arn,
        )["IntegrationId"]

        # Route with no scope
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="JWT",
            AuthorizerId=authorizer_id,
            RouteKey="ANY /no-scope",
            Target=f"integrations/{integration_id}",
        )

        # Route with scope1
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="JWT",
            AuthorizerId=authorizer_id,
            AuthorizationScopes=["http://example.com/scope1"],
            RouteKey="ANY /scope1",
            Target=f"integrations/{integration_id}",
        )

        # Route with email scope
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="JWT",
            AuthorizerId=authorizer_id,
            AuthorizationScopes=["email"],
            RouteKey="ANY /email-scope",
            Target=f"integrations/{integration_id}",
        )

        # Route with invalid scope
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="JWT",
            AuthorizerId=authorizer_id,
            AuthorizationScopes=["http://example.com/scope2"],
            RouteKey="ANY /invalid-scope",
            Target=f"integrations/{integration_id}",
        )

        # Method with multiple scopes
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="JWT",
            AuthorizerId=authorizer_id,
            AuthorizationScopes=["http://example.com/scope1", "http://example.com/scope2"],
            RouteKey="ANY /multi-scope",
            Target=f"integrations/{integration_id}",
        )

        # create deployment
        stage_name = "test-stage"
        aws_client.apigatewayv2.create_stage(ApiId=api_id, StageName=stage_name, AutoDeploy=True)

        # get auth token
        password = "Test123!"
        username = "user@domain.com"

        aws_client.cognito_idp.sign_up(ClientId=app_client_id, Username=username, Password=password)
        aws_client.cognito_idp.admin_confirm_sign_up(UserPoolId=user_pool_id, Username=username)
        id_token, access_token = get_auth_token_via_login_form(
            user_pool,
            app_client,
            username=username,
            password=password,
            region_name=region_name,
            scope="openid email",
        )

        _, access_token_openid = get_auth_token_via_login_form(
            user_pool,
            app_client,
            username=username,
            password=password,
            region_name=region_name,
            scope="openid",
        )

        def invoke_url(path: str):
            return api_invoke_url(api_id, stage=stage_name, path=path)

        def invoke_api(path: str = "no-scope", auth_token: str = None, expected_status: int = None):
            headers = {"user-agent": "test-jwt"}
            if auth_token is not None:
                headers["Authorization"] = auth_token

            _response = requests.get(invoke_url(path), headers=headers)

            if expected_status is not None:
                assert _response.status_code == expected_status

            result = _response.json()

            if _response.status_code == 200:
                request_context = result["requestContext"]
                result = {
                    "authorizer": request_context.get("authorizer"),
                    "identity": request_context.get("identity"),
                }

            return {
                "content": result,
                "statusCode": _response.status_code,
            }

        # Missing auth Token
        response = retry(lambda: invoke_api(expected_status=401))
        snapshot.match("no-header-token", response)

        # Access token with bearer prefix
        response = invoke_api(path="scope1", auth_token=f"Bearer {access_token}")
        snapshot.match("access_token-scope1-Bearer", response)

        # Id token with bearer prefix
        response = invoke_api(path="no-scope", auth_token=f"Bearer {id_token}")
        snapshot.match("id_token-no-scope-Bearer", response)

        for token_type, token in (
            ("id_token", id_token),
            ("access_token", access_token),
            ("access_token_openid", access_token_openid),
        ):
            # Without scope defined id token will succeed, Access Tokens will fail
            response = invoke_api(path="no-scope", auth_token=token)
            snapshot.match(f"{token_type}-no-scope", response)

            # If multiple scopes are declared, only one valid scope is sufficient for access token
            response = invoke_api(path="multi-scope", auth_token=token)
            snapshot.match(f"{token_type}-multi-scope", response)

            # With an invalid scope all token will fail
            response = invoke_api(path="invalid-scope", auth_token=token)
            snapshot.match(f"{token_type}-invalid-scope", response)

            # With a scope defined id token will fail, Access will succeed.
            # This is the scope populated by the lambda resource server
            response = invoke_api(path="scope1", auth_token=token)
            snapshot.match(f"{token_type}-scope1-scope", response)

            # Email Scope will fail for id token and openid access token (lacking the  email scope)
            # but will succeed for the access token
            response = invoke_api(path="email-scope", auth_token=token)
            snapshot.match(f"{token_type}-email-scope", response)

    @markers.aws.validated
    def test_jwt_authorizer_failure(
        self,
        create_v2_api,
        aws_client,
        region_name,
        apigw_echo_http_server_anything,
        create_cognito_pool_and_domain,
        snapshot,
    ):
        # Create user pool and client
        domain_name = f"ls-{short_uid()}"
        user_pool_result = create_cognito_pool_and_domain(domain_name=domain_name)
        user_pool = user_pool_result.user_pool
        app_client = user_pool_result.pool_client

        user_pool_id = user_pool["Id"]
        app_client_id = app_client["ClientId"]

        # Create a second user pool and client to provide token from a wrong issuer
        user_pool_result_2 = create_cognito_pool_and_domain(domain_name=f"ls-{short_uid()}")
        user_pool_2_id = user_pool_result_2.user_pool["Id"]
        app_client_2_id = user_pool_result_2.pool_client["ClientId"]

        result = create_v2_api(ProtocolType="HTTP", Name=f"api-{short_uid()}")
        api_id = result["ApiId"]

        if is_aws_cloud():
            issuer = f"https://cognito-idp.{region_name}.amazonaws.com/{user_pool_id}"
            wrong_issuer = f"https://cognito-idp.{region_name}.amazonaws.com/{user_pool_2_id}"
        else:
            issuer = get_issuer_url(pool_id=user_pool_id)
            wrong_issuer = get_issuer_url(pool_id=user_pool_2_id)

        authorizer_valid = aws_client.apigatewayv2.create_authorizer(
            Name="jwt-authorizer-valid",
            ApiId=api_id,
            AuthorizerType="JWT",
            JwtConfiguration={
                "Audience": [app_client_id],
                "Issuer": issuer,
            },
            IdentitySource=["$request.header.Authorization"],
        )["AuthorizerId"]

        authorizer_wrong_issuer = aws_client.apigatewayv2.create_authorizer(
            Name="jwt-authorizer-wrong-issuer",
            ApiId=api_id,
            AuthorizerType="JWT",
            JwtConfiguration={
                "Audience": [app_client_id],
                "Issuer": wrong_issuer,
            },
            IdentitySource=["$request.header.Authorization"],
        )["AuthorizerId"]

        authorizer_wrong_audience = aws_client.apigatewayv2.create_authorizer(
            Name="jwt-authorizer-wrong-audience",
            ApiId=api_id,
            AuthorizerType="JWT",
            JwtConfiguration={
                "Audience": [app_client_2_id],
                "Issuer": issuer,
            },
            IdentitySource=["$request.header.Authorization"],
        )["AuthorizerId"]

        # creates a http integration
        integration_id = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            IntegrationMethod="ANY",
            IntegrationUri=apigw_echo_http_server_anything,
            PayloadFormatVersion="1.0",
        )["IntegrationId"]

        # Create route valid issuer
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="JWT",
            AuthorizerId=authorizer_valid,
            RouteKey="ANY /valid-issuer",
            Target=f"integrations/{integration_id}",
        )

        # Create route wrong issuer
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="JWT",
            AuthorizerId=authorizer_wrong_issuer,
            RouteKey="ANY /wrong-issuer",
            Target=f"integrations/{integration_id}",
        )

        # Create route wrong audience
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="JWT",
            AuthorizerId=authorizer_wrong_audience,
            RouteKey="ANY /wrong-audience",
            Target=f"integrations/{integration_id}",
        )

        # create deployment
        stage_name = "test-stage"
        aws_client.apigatewayv2.create_stage(ApiId=api_id, StageName=stage_name, AutoDeploy=True)

        # get auth token
        password = "Test123!"
        username = "user@domain.com"

        aws_client.cognito_idp.sign_up(ClientId=app_client_id, Username=username, Password=password)
        aws_client.cognito_idp.admin_confirm_sign_up(UserPoolId=user_pool_id, Username=username)
        _, access_token = get_auth_token_via_login_form(
            user_pool,
            app_client,
            username=username,
            password=password,
            region_name=region_name,
            scope="openid email",
        )

        invoke_url = api_invoke_url(api_id, stage=stage_name)
        headers = {"user-agent": "test-jwt", "Authorization": access_token}

        def invoke_api(path: str, expected_status: int):
            _response = requests.get(invoke_url + path, headers=headers)

            assert _response.status_code == expected_status

            return {
                "content": _response.json(),
                "statusCode": _response.status_code,
            }

        # Valid request. We are not snapshotting here as this check is only to validate
        # the api was reachable before deleting the user pool. Previous tests are snapshotting the responses
        retry(lambda: invoke_api(path="/valid-issuer", expected_status=200))

        response = retry(lambda: invoke_api(path="/wrong-issuer", expected_status=401))
        snapshot.match("wrong-issuer", response)

        if not is_next_gen_api() and not is_aws_cloud():
            # TODO remove this check when migrating away from legacy
            #  Legacy is not verifying the audience when `client_id` is in the scope instead of `aud`.
            expected_status = 200
        else:
            expected_status = 401
        retry(lambda: invoke_api(path="/wrong-audience", expected_status=expected_status))
        snapshot.match("wrong-audience", response)
