import json
import logging
import os
import re
import textwrap

import pytest
import requests
from localstack.aws.api.lambda_ import Runtime
from localstack.constants import APPLICATION_JSON, TAG_KEY_CUSTOM_ID
from localstack.services.apigateway.context import ApiGatewayVersion
from localstack.testing.aws.util import is_aws_cloud
from localstack.testing.pytest import markers
from localstack.utils import files, testutil
from localstack.utils.aws import arns
from localstack.utils.aws.arns import get_partition, parse_arn
from localstack.utils.aws.request_context import mock_aws_request_headers
from localstack.utils.files import load_file
from localstack.utils.strings import short_uid, to_str
from localstack.utils.sync import retry

from tests.aws.services.apigateway.apigateway_fixtures import (
    UrlType,
    api_invoke_url,
)
from tests.aws.services.apigateway.conftest import (
    APIGW_ASSUME_ROLE_POLICY,
    LAMBDA_ECHO,
    LAMBDA_ECHO_EVENT,
    LAMBDA_JS,
    LAMBDA_REQUEST_AUTH,
    LAMBDA_TOKEN_AUTH,
    get_auth_login_via_token_endpoint,
    invoke_api_using_authorizer,
    is_next_gen_api,
)

LOG = logging.getLogger(__name__)

GRAPHQL_REQUEST = os.path.join(os.path.dirname(__file__), "../../templates", "graphql-request.json")

TEST_SCHEMA = """
type Post {
    id: String!
    title: String!
}

type Query {
    singlePost(id: String!): Post!
}

schema {
    query: Query
}
"""

API_SPEC_FILE = os.path.join(os.path.dirname(__file__), "../../templates", "openapi3.0.spec.yaml")

TEST_LAMBDA_AUTHORIZER_IAM_RESPONSE = os.path.join(
    os.path.dirname(__file__), "../../files/lambda_auth_iam.py"
)


@pytest.fixture
def _create_rest_api_with_token_authorizer(
    create_lambda_function,
    create_rest_apigw,
    apigateway_lambda_integration_role,
    account_id,
    aws_client_factory,
    snapshot,
):
    def _create(api_name=None, region_name=None, rest_api_id=None):
        aws_client = aws_client_factory(region_name=region_name)
        api_name = api_name or f"api-{short_uid()}"
        kwargs = {"tags": {TAG_KEY_CUSTOM_ID: rest_api_id}} if rest_api_id else {}
        rest_api_id, _, root_resource_id = create_rest_apigw(
            name=api_name, region_name=region_name, **kwargs
        )
        region_name = aws_client.apigateway._client_config.region_name
        apigw_role_name = parse_arn(apigateway_lambda_integration_role)["resource"]
        snapshot.add_transformer(snapshot.transform.regex(apigw_role_name, "<apigw-role-name>"))
        snapshot.add_transformer(snapshot.transform.regex(rest_api_id, "<rest-api-id>"))
        snapshot.add_transformer(snapshot.transform.regex(account_id, "<account_id>"))
        snapshot.add_transformer(
            snapshot.transform.key_value("cacheNamespace", "<cache-namespace>")
        )
        snapshot.add_transformer(
            snapshot.transform.jsonpath(
                "$..headers.User-Agent", "<user-agent>", reference_replacement=False
            )
        )
        snapshot.add_transformer(snapshot.transform.apigateway_proxy_event())

        # create API GW authorizer
        auth_function_name = f"lambda_auth-{short_uid()}"
        snapshot.add_transformer(
            snapshot.transform.regex(auth_function_name, "<auth-function-name>")
        )
        auth_function_response = create_lambda_function(
            handler_file=LAMBDA_TOKEN_AUTH,
            func_name=auth_function_name,
            runtime=Runtime.nodejs20_x,
            client=aws_client.lambda_,
        )
        lambda_arn = auth_function_response["CreateFunctionResponse"]["FunctionArn"]
        auth_url = arns.apigateway_invocations_arn(lambda_arn, region_name)

        create_authorizer_response = aws_client.apigateway.create_authorizer(
            restApiId=rest_api_id,
            name="test_authorizer",
            type="TOKEN",
            identitySource="method.request.header.Authorization",
            authorizerUri=auth_url,
            authorizerCredentials=apigateway_lambda_integration_role,
            # disable authorizer caching for testing
            authorizerResultTtlInSeconds=0,
        )
        authorizer_id = create_authorizer_response.get("id")
        snapshot.add_transformer(snapshot.transform.regex(authorizer_id, "<authorizer-id>"))
        snapshot.match("create_authorizer_token_based", create_authorizer_response)

        # Lambda authorizer SourceArn pattern:
        # https://docs.aws.amazon.com/apigateway/latest/developerguide/arn-format-reference.html#apigateway-execute-api-arns
        region_name = aws_client.apigateway._client_config.region_name
        source_arn = "arn:aws:execute-api:{}:{}:{}/authorizers/{}".format(
            region_name, account_id, rest_api_id, authorizer_id
        )
        aws_client.lambda_.add_permission(
            FunctionName=auth_function_name,
            Action="lambda:InvokeFunction",
            StatementId="lambda-authorizer-invoke-permission",
            Principal="apigateway.amazonaws.com",
            SourceArn=source_arn,
        )

        return rest_api_id, auth_function_name, authorizer_id

    return _create


@pytest.fixture
def _create_method_and_integration(aws_client_factory):
    def _create(
        rest_api_id,
        resource_id,
        authorizer_id=None,
        response_templates=None,
        integration_kwargs=None,
        region_name=None,
    ):
        aws_client = aws_client_factory(region_name=region_name)

        kwargs = {"authorizerId": authorizer_id} if authorizer_id else {}
        aws_client.apigateway.put_method(
            restApiId=rest_api_id,
            resourceId=resource_id,
            httpMethod="GET",
            authorizationType="CUSTOM",
            requestParameters={"method.request.header.Authorization": True},
            **kwargs,
        )

        integration_kwargs = integration_kwargs or {}
        integration_kwargs.setdefault("type", "MOCK")
        aws_client.apigateway.put_integration(
            restApiId=rest_api_id,
            resourceId=resource_id,
            httpMethod="GET",
            requestTemplates={APPLICATION_JSON: """{"statusCode": 200}"""},
            **integration_kwargs,
        )

        aws_client.apigateway.put_method_response(
            restApiId=rest_api_id,
            resourceId=resource_id,
            httpMethod="GET",
            statusCode="200",
        )

        kwargs = {"responseTemplates": response_templates} if response_templates else {}
        aws_client.apigateway.put_integration_response(
            restApiId=rest_api_id,
            resourceId=resource_id,
            httpMethod="GET",
            statusCode="200",
            selectionPattern="200",
            **kwargs,
        )

    return _create


def _invoke_and_assert(
    url: str,
    auth_header: str = None,
    expected_status_code: int = 200,
    method: str = "GET",
    data: str | bytes = None,
    json_body: dict = None,
):
    """Invoke the API Gateway API with the given URL, and assert the expected response code"""
    kwargs = {}
    if auth_header:
        kwargs["headers"] = {"Authorization": auth_header}
    if data:
        kwargs["data"] = data
    if json_body:
        kwargs["json"] = json_body
    result = requests.request(method, url, verify=False, **kwargs)
    assert result.status_code == expected_status_code
    return result


class TestRestAPIs:
    @markers.aws.validated
    def test_rest_import_openapi_3_0(
        self,
        create_rest_apigw_openapi,
        create_lambda_function,
        apigateway_lambda_integration_role,
        account_id,
        snapshot,
        aws_client,
        region_name,
    ):
        snapshot.add_transformer(snapshot.transform.key_value("rootResourceId"))
        # load openapi spec 3.0
        api_spec = load_file(API_SPEC_FILE)

        # create lambda authorizer
        lambda_auth_name = f"lambda_auth-{short_uid()}"
        lambda_auth_arn = create_lambda_function(
            handler_file=TEST_LAMBDA_AUTHORIZER_IAM_RESPONSE,
            func_name=lambda_auth_name,
            runtime=Runtime.python3_12,
        )["CreateFunctionResponse"]["FunctionArn"]

        # create lambda integration
        lambda_name = f"lambda-{short_uid()}"
        lambda_arn = create_lambda_function(
            handler_file=LAMBDA_ECHO % "false",
            func_name=lambda_name,
            runtime=Runtime.nodejs20_x,
        )["CreateFunctionResponse"]["FunctionArn"]

        # openapi spec string replacement
        auth_uri = arns.apigateway_invocations_arn(lambda_auth_arn, region_name=region_name)
        uri = arns.apigateway_invocations_arn(lambda_arn, region_name=region_name)
        api_spec = api_spec.replace("${authorizerUri}", auth_uri)
        api_spec = api_spec.replace("${authorizerCredentials}", apigateway_lambda_integration_role)
        api_spec = api_spec.replace("${lambdaUri}", uri)

        # create rest api
        api_id, response = create_rest_apigw_openapi(body=api_spec, failOnWarnings=True)
        snapshot.add_transformer(snapshot.transform.regex(api_id, "<rest-api-id>"))
        snapshot.match("import_openapi_3_0", response)

        source_arn = "arn:aws:execute-api:{}:{}:{}/*/*/*".format(
            aws_client.apigateway.meta.region_name, account_id, api_id
        )
        aws_client.lambda_.add_permission(
            FunctionName=lambda_arn,
            StatementId=str(short_uid()),
            Action="lambda:InvokeFunction",
            Principal="apigateway.amazonaws.com",
            SourceArn=source_arn,
        )

        stage_name = "dev"
        aws_client.apigateway.create_deployment(restApiId=api_id, stageName=stage_name)

        def call_api():
            endpoint = api_invoke_url(
                api_id=api_id, stage=stage_name, path="/api/v1/user/test%2B1@mail.com"
            )
            result = requests.get(
                endpoint,
                headers={"X-Authorization": "allow", "Authorization": "value"},
                verify=False,
            )
            assert result.status_code == 200

            endpoint = api_invoke_url(
                api_id=api_id, stage=stage_name, path="/api/v1/user/test+1@mail.com"
            )
            result = requests.get(
                endpoint,
                headers={"X-Authorization": "deny", "Authorization": "value"},
                verify=False,
            )
            assert result.status_code == 403

            endpoint = api_invoke_url(
                api_id=api_id, stage=stage_name, path="/api/v1/user/test+1@mail.com"
            )
            result = requests.get(endpoint, headers={"Authorization": "deny"}, verify=False)
            assert result.status_code == 401

        retry(call_api, retries=10, sleep=1)

    # TODO: remove this test once we remove legacy, it doesn't work against AWS and there are better ones in
    #  test_authorizers. Keep for "regression" in legacy
    @pytest.mark.skipif(
        condition=is_next_gen_api(),
        reason="This test doesn't work against AWS or NextGen",
    )
    @markers.aws.needs_fixing
    def test_cognito_authorizers(
        self,
        create_rest_apigw,
        create_lambda_function,
        aws_client,
        region_name,
        create_user_pool_client,
    ):
        # setup
        api_id, _, root_resource_id = create_rest_apigw(name="test-cognito-auth")

        user_pool_result = create_user_pool_client(
            client_kwargs={
                "ExplicitAuthFlows": ["USER_PASSWORD_AUTH"],
            },
        )
        user_pool = user_pool_result.user_pool
        app_client = user_pool_result.pool_client
        app_client_id = app_client["ClientId"]
        cognito_pool_id = user_pool["Id"]

        authorizer_id = aws_client.apigateway.create_authorizer(
            restApiId=api_id,
            name="test_authorizer",
            type="COGNITO_USER_POOLS",
            providerARNs=[user_pool["Arn"]],
            identitySource="method.request.header.Authorization",
        )["id"]
        resource_id = aws_client.apigateway.create_resource(
            restApiId=api_id, parentId=root_resource_id, pathPart="demo"
        )["id"]
        aws_client.apigateway.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod="ANY",
            authorizationType="COGNITO_USER_POOLS",
            authorizerId=authorizer_id,
        )
        user_pass = "Test123!"
        aws_client.cognito_idp.sign_up(
            ClientId=app_client_id,
            Username="demo@user.com",
            Password=user_pass,
        )
        aws_client.cognito_idp.admin_confirm_sign_up(
            UserPoolId=cognito_pool_id, Username="demo@user.com"
        )
        token = aws_client.cognito_idp.initiate_auth(
            ClientId=app_client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": "demo@user.com", "PASSWORD": user_pass},
        )["AuthenticationResult"]["IdToken"]
        lambda_name = f"auth-{short_uid()}"
        lambda_auth_arn = create_lambda_function(
            handler_file=LAMBDA_JS, func_name=lambda_name, runtime=Runtime.nodejs20_x
        )["CreateFunctionResponse"]["FunctionArn"]
        uri = arns.apigateway_invocations_arn(lambda_auth_arn, region_name)

        aws_client.apigateway.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod="ANY",
            type="AWS_PROXY",
            integrationHttpMethod="POST",
            uri=uri,
        )
        stage_name = "local"
        aws_client.apigateway.create_deployment(restApiId=api_id, stageName=stage_name)

        endpoint = api_invoke_url(api_id, stage_name, path="/demo")
        # test invalid authorization
        result = requests.get(endpoint, headers={"Authorization": "invalid-token"}, verify=False)
        assert to_str(result.content) == json.dumps({"message": "Unauthorized"})

        # test valid authorization using bearer token
        # TODO: AWS returns 403, as Cognito authorizers don't accept bearer prefix, but require direct passthrough of
        #  the token. See:
        # https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-integrate-with-cognito.html
        # Only apigwv2 JWT authorizer can accept the Bearer prefix
        # https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html
        # Rework the test and fix the behavior
        result = requests.get(endpoint, headers={"Authorization": f"Bearer {token}"}, verify=False)
        assert result.status_code == 200

        # amazon seems to accept valid bearer token without the "bearer" prefix
        result = requests.get(endpoint, headers={"Authorization": token}, verify=False)
        assert result.status_code == 200

        result = requests.get(endpoint, headers={"Authorization": token[:-1]}, verify=False)
        assert result.status_code == 403
        assert to_str(result.content) == json.dumps({"Message": "Access Denied"})

    @markers.aws.needs_fixing
    def test_apigw_v1_lambda_request_authorizer(
        self, create_lambda_function, aws_client, region_name
    ):
        def create_authorizer_v1_func(api_obj):
            return create_authorizer_func(api_obj, "1.0")

        def create_authorizer_func(api_obj, response_format_version):
            # create Lambda
            lambda_name = f"auth-{short_uid()}"
            lambda_code = LAMBDA_REQUEST_AUTH % response_format_version
            zip_file = testutil.create_lambda_archive(lambda_code, get_content=True)
            lambda_arn = create_lambda_function(func_name=lambda_name, zip_file=zip_file)[
                "CreateFunctionResponse"
            ]["FunctionArn"]
            # create API GW authorizer
            auth_name = f"auth-{short_uid()}"
            auth_url = arns.apigateway_invocations_arn(lambda_arn, region_name)
            return aws_client.apigateway.create_authorizer(
                restApiId=api_obj["id"],
                name=auth_name,
                type="REQUEST",
                identitySource="method.request.header.x-user",
                authorizerUri=auth_url,
            )

        valid_headers = {"X-User": "valid-user"}
        invalid_headers = {"X-User": "invalid-user"}
        # invoke API GW v2 API using authorizer response format 1.0
        invoke_api_using_authorizer(
            aws_client.apigateway,
            aws_client.lambda_,
            create_lambda_function,
            create_authorizer_v1_func,
            valid_headers,
            invalid_headers,
            version=ApiGatewayVersion.V1,
        )

    @markers.aws.needs_fixing
    def test_iam_authorizer(self, create_lambda_function, aws_client, create_user, region_name):
        # create IAM user and access keys
        iam_user = f"user-{short_uid()}"
        create_user(UserName=iam_user)
        keys = aws_client.iam.create_access_key(UserName=iam_user)["AccessKey"]

        def create_authorizer_func(rest_api):
            # create API GW authorizer
            auth_name = f"auth-{short_uid()}"
            return aws_client.apigateway.create_authorizer(
                restApiId=rest_api["id"],
                name=auth_name,
                type="AWS_IAM",
                providerARNs=[],
            )

        valid_headers = mock_aws_request_headers(
            service="apigateway",
            aws_access_key_id=keys["AccessKeyId"],
            region_name=region_name,
        )
        invalid_headers = {"Authorization": "Bearer invalid-token"}
        return invoke_api_using_authorizer(
            aws_client.apigateway,
            aws_client.lambda_,
            create_lambda_function,
            create_authorizer_func,
            valid_headers,
            invalid_headers,
            iam_user_name=iam_user,
        )

    # TODO: check overlap with test_cognito_authorizers(..) method above
    #  remove when removing legacy
    @markers.aws.needs_fixing
    def test_cognito_authorizer(self, create_user_pool_client, create_lambda_function, aws_client):
        cognito = aws_client.cognito_idp

        # create Cognito user pool and user
        pool_name = f"auth-{short_uid()}"
        user_pool = cognito.create_user_pool(PoolName=pool_name).get("UserPool")
        pool_id = user_pool.get("Id")
        pool_client = cognito.create_user_pool_client(UserPoolId=pool_id, ClientName=pool_name)
        client_id = pool_client["UserPoolClient"]["ClientId"]
        pool_arn = user_pool.get("Arn")
        username = "user123"
        password = "password123"
        cognito.admin_create_user(UserPoolId=pool_id, Username=username, TemporaryPassword=password)

        def create_authorizer_func(rest_api):
            # create API GW authorizer
            auth_name = f"auth-{short_uid()}"
            return aws_client.apigateway.create_authorizer(
                restApiId=rest_api["id"],
                name=auth_name,
                type="COGNITO_USER_POOLS",
                identitySource="method.request.header.X-Auth-Token",
                providerARNs=[pool_arn],
            )

        result = cognito.initiate_auth(
            ClientId=client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": username, "PASSWORD": password},
        )
        id_token = result["AuthenticationResult"]["IdToken"]
        valid_headers = {"X-Auth-Token": f"Bearer {id_token}"}
        invalid_headers = {"X-Auth-Token": "Bearer invalid-token"}
        return invoke_api_using_authorizer(
            aws_client.apigateway,
            aws_client.lambda_,
            create_lambda_function,
            create_authorizer_func,
            valid_headers,
            invalid_headers,
        )

    # TODO: Remove this test when transitioning to apigw NextGen.
    #  this test is replaced by the more complete test_authorizers.TestRestApiAuthorizers.test_authorizer_cognito...
    @markers.snapshot.skip_snapshot_verify(
        paths=["$..UserPoolId", "$..Username"], condition=lambda: not is_next_gen_api()
    )
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            '$..claims["cognito:user_status"]',
            "$..claims.event_id",
            "$..claims.iss",
            "$..claims.jti",
            "$..claims.origin_jti",
            "$..claims.username",
            "$..claims.version",
        ]
    )
    @markers.aws.validated
    @pytest.mark.parametrize("token_type", ["client_credentials", "username"])
    def test_cognito_authorizer_token_types(
        self,
        token_type,
        create_user_pool_client,
        create_lambda_with_invocation_forwarding,
        get_lambda_invocation_events,
        snapshot,
        aws_client,
        region_name,
        create_rest_apigw,
    ):
        # create REST API
        api_id, _, root_resource_id = create_rest_apigw(name=f"test-{short_uid()}")
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("aud"),
                snapshot.transform.key_value("client_id"),
                snapshot.transform.key_value("jti"),
                snapshot.transform.key_value("origin_jti"),
                snapshot.transform.key_value("sub"),
                # These values end up being int out of sqs
                snapshot.transform.key_value(
                    "auth_time", reference_replacement=False, value_replacement="<auth_time>"
                ),
                snapshot.transform.key_value(
                    "exp", reference_replacement=False, value_replacement="<exp>"
                ),
                snapshot.transform.key_value(
                    "iat", reference_replacement=False, value_replacement="<iat>"
                ),
            ]
        )

        # create Cognito user pool, user pool client and resource server
        scope = "resource-server/scope1"
        user_pool_and_client = create_user_pool_client(
            client_kwargs={
                "AllowedOAuthFlows": ["client_credentials"],
                "AllowedOAuthScopes": [scope],
                "ExplicitAuthFlows": [
                    "ALLOW_REFRESH_TOKEN_AUTH",
                    "ALLOW_CUSTOM_AUTH",
                    "ALLOW_USER_SRP_AUTH",
                ],
                "SupportedIdentityProviders": ["COGNITO"],
                "AllowedOAuthFlowsUserPoolClient": True,
                "GenerateSecret": True,
            },
        )

        pool_domain = f"domain-{short_uid()}"
        pool_id = user_pool_and_client.user_pool["Id"]
        aws_client.cognito_idp.create_user_pool_domain(Domain=pool_domain, UserPoolId=pool_id)

        # create authorizer
        authorizer_id = aws_client.apigateway.create_authorizer(
            restApiId=api_id,
            name="test_authorizer",
            type="COGNITO_USER_POOLS",
            providerARNs=[user_pool_and_client.user_pool["Arn"]],
            identitySource="method.request.header.X-Auth-Token",
        )["id"]

        resource_id = aws_client.apigateway.create_resource(
            restApiId=api_id, parentId=root_resource_id, pathPart="test"
        )["id"]
        kwargs = {"authorizationScopes": [scope]} if token_type == "client_credentials" else {}

        aws_client.apigateway.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod="ANY",
            authorizationType="COGNITO_USER_POOLS",
            authorizerId=authorizer_id,
            **kwargs,
        )

        # create integration Lambda function
        lambda_arn = create_lambda_with_invocation_forwarding()

        target = arns.apigateway_invocations_arn(
            lambda_arn, region_name=aws_client.apigateway.meta.region_name
        )

        aws_account_id = aws_client.sts.get_caller_identity()["Account"]
        source_arn = "arn:aws:execute-api:{}:{}:{}/*/*/test".format(
            aws_client.apigateway.meta.region_name, aws_account_id, api_id
        )
        aws_client.lambda_.add_permission(
            FunctionName=lambda_arn,
            StatementId=str(short_uid()),
            Action="lambda:InvokeFunction",
            Principal="apigateway.amazonaws.com",
            SourceArn=source_arn,
        )

        aws_client.apigateway.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod="ANY",
            integrationHttpMethod="POST",
            # TODO: parameterize this test for "AWS" integration type as well!
            type="AWS_PROXY",
            uri=target,
        )
        aws_client.apigateway.create_deployment(restApiId=api_id, stageName="dev")

        if token_type == "client_credentials":
            access_token = get_auth_login_via_token_endpoint(
                client_id=user_pool_and_client.pool_client["ClientId"],
                client_secret=user_pool_and_client.pool_client["ClientSecret"],
                domain=pool_domain,
                region_name=region_name,
                scope=scope,
            )

        elif token_type == "username":
            aws_client.cognito_idp.admin_create_user(UserPoolId=pool_id, Username="test")
            aws_client.cognito_idp.admin_set_user_password(
                UserPoolId=pool_id, Username="test", Password="Test123!", Permanent=True
            )
            result = aws_client.cognito_idp.create_user_pool_client(
                UserPoolId=pool_id,
                ClientName="client2",
                ExplicitAuthFlows=["ALLOW_REFRESH_TOKEN_AUTH", "ALLOW_USER_PASSWORD_AUTH"],
            )
            client_id = result["UserPoolClient"]["ClientId"]
            result = aws_client.cognito_idp.initiate_auth(
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": "test",
                    "PASSWORD": "Test123!",
                },
                ClientId=client_id,
            )
            access_token = result["AuthenticationResult"]["IdToken"]

        # assert we have an authorized request with the access token
        def _assert_authorized_request():
            url = api_invoke_url(api_id=api_id, path="/dev/test")
            resp = requests.get(
                url, headers={"X-Auth-Token": f"Bearer {access_token}"}, verify=False
            )
            assert resp.status_code == 200

        retry(_assert_authorized_request, retries=10, sleep=0.8)

        # assert we have an unauthorized request with an invalid access token
        endpoint = api_invoke_url(api_id=api_id, path="/dev/test")
        response = requests.get(endpoint, headers={"X-Auth-Token": "invalid-token"}, verify=False)
        assert response.status_code == 401

        # assert the payload of received invocation events
        messages = get_lambda_invocation_events(lambda_arn, count=1)
        authorizer_info = messages[0]["event"]["requestContext"]["authorizer"]
        snapshot.match("lambda-auth-info", authorizer_info)

    @markers.aws.validated
    @pytest.mark.parametrize(
        ["url_type", "caching"],
        [(UrlType.HOST_BASED, True), (UrlType.HOST_BASED, False), (UrlType.PATH_BASED, True)],
    )
    def test_lambda_request_authorizer_different_paths(
        self,
        url_type,
        caching,
        create_rest_apigw,
        create_lambda_function,
        apigateway_lambda_integration_role,
        snapshot,
        cleanups,
        aws_client,
        region_name,
    ):
        # Create API Gateway
        gateway_name = f"gw-{short_uid()}"
        stage_name = "test"
        rest_api_id, _, _ = create_rest_apigw(name=gateway_name)

        # Create authorizer with lambda
        lambda_auth_name = f"lambda_auth-{short_uid()}"
        authorizer_name = f"authorizer-{short_uid()}"
        lambda_auth_arn = create_lambda_function(
            handler_file=LAMBDA_REQUEST_AUTH, func_name=lambda_auth_name
        )["CreateFunctionResponse"]["FunctionArn"]
        auth_url = arns.apigateway_invocations_arn(lambda_auth_arn, region_name=region_name)

        identity_source = "method.request.header.X-User"
        authorizer_ttl = 300
        if not caching:
            # If caching is disabled, Identity source is optional, and handling of missing
            # sources does not result in an UnauthorizedError
            identity_source = ""
            authorizer_ttl = 0

        authorizer = aws_client.apigateway.create_authorizer(
            restApiId=rest_api_id,
            name=authorizer_name,
            type="REQUEST",
            identitySource=identity_source,
            authorizerResultTtlInSeconds=authorizer_ttl,
            authorizerUri=auth_url,
            authorizerCredentials=apigateway_lambda_integration_role,
        )
        authorizer_id = authorizer["id"]

        # Create lambdas
        lambda_private_name = f"lambda_private_{short_uid()}"
        lambda_public_name = f"lambda_public_{short_uid()}"
        lambda_private_arn = create_lambda_function(
            handler_file=LAMBDA_JS % "private",
            func_name=lambda_private_name,
            runtime=Runtime.nodejs20_x,
        )["CreateFunctionResponse"]["FunctionArn"]
        lambda_public_arn = create_lambda_function(
            handler_file=LAMBDA_JS % "public",
            func_name=lambda_public_name,
            runtime=Runtime.nodejs20_x,
        )["CreateFunctionResponse"]["FunctionArn"]
        lambda_private_target_arn = arns.apigateway_invocations_arn(
            lambda_private_arn, region_name=aws_client.apigateway.meta.region_name
        )
        lambda_public_target_arn = arns.apigateway_invocations_arn(
            lambda_public_arn, region_name=aws_client.apigateway.meta.region_name
        )

        # Create API Gateway - Lambda integrations
        root_resource_id = aws_client.apigateway.get_resources(restApiId=rest_api_id)["items"][0][
            "id"
        ]
        public_resource_id = aws_client.apigateway.create_resource(
            restApiId=rest_api_id, parentId=root_resource_id, pathPart="public"
        )["id"]
        private_resource_id = aws_client.apigateway.create_resource(
            restApiId=rest_api_id, parentId=root_resource_id, pathPart="private"
        )["id"]
        private_resource_id_id = aws_client.apigateway.create_resource(
            restApiId=rest_api_id, parentId=private_resource_id, pathPart="{id}"
        )["id"]

        # define two method integrations - for the public and the private (protected) resource
        method_integrations = (
            (public_resource_id, lambda_public_target_arn, None),
            (private_resource_id, lambda_private_target_arn, authorizer_id),
            (private_resource_id_id, lambda_private_target_arn, authorizer_id),
        )
        for resource_id, target_arn, authorizer_id in method_integrations:
            kwargs = {"authorizationType": "NONE"}
            if authorizer_id:
                kwargs = {"authorizationType": "CUSTOM", "authorizerId": authorizer_id}
            aws_client.apigateway.put_method(
                restApiId=rest_api_id,
                resourceId=resource_id,
                httpMethod="GET",
                **kwargs,
            )
            aws_client.apigateway.put_integration(
                restApiId=rest_api_id,
                resourceId=resource_id,
                type="AWS_PROXY",
                httpMethod="GET",
                uri=target_arn,
                integrationHttpMethod="POST",
                credentials=apigateway_lambda_integration_role,
            )

        # Deploy API Gateway
        aws_client.apigateway.create_deployment(restApiId=rest_api_id, stageName=stage_name)

        # Test API Gateway
        private_endpoint = api_invoke_url(
            api_id=rest_api_id, stage=stage_name, path="/private", url_type=url_type
        )

        def _call_and_assert():
            result = requests.get(private_endpoint, headers={"X-User": "valid-user"}, verify=False)
            assert result.ok
            result = to_str(result.content)
            assert "private" in result
            return result

        result = retry(_call_and_assert, retries=10, sleep=2)
        snapshot.match("private_endpoint_authorized_result", result)
        result = requests.get(private_endpoint, headers={"X-User": "invalid-user"}, verify=False)
        assert 403 == result.status_code
        snapshot.match("private_endpoint_unauthorized_result", result.text)

        private_endpoint_id = api_invoke_url(
            api_id=rest_api_id, stage=stage_name, path="/private/42", url_type=url_type
        )
        result = requests.get(private_endpoint_id, headers={"X-User": "valid-user"}, verify=False)
        assert result.status_code < 400
        result = to_str(result.content)
        assert "private" in result
        snapshot.match("private_endpoint_id_authorized_result", result)
        result = requests.get(private_endpoint_id, headers={"X-User": "invalid-user"}, verify=False)
        assert 403 == result.status_code
        snapshot.match("private_endpoint_id_unauthorized_result", result.text)

        result = requests.get(private_endpoint, headers={"Missing": "headers"})
        snapshot.match(
            "private_endpoint_missing_headers", {"status": result.status_code, "text": result.text}
        )

        public_endpoint = api_invoke_url(
            api_id=rest_api_id, stage=stage_name, path="/public", url_type=url_type
        )
        result = requests.get(public_endpoint, verify=False)
        assert result.status_code < 400
        result = to_str(result.content)
        snapshot.match("public_result", result)
        assert "public" in result

    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            "$.create_authorizer_token_based.authType",
            "$.token_authorizer_allow.origin",
        ]
    )
    @markers.snapshot.skip_snapshot_verify(
        condition=lambda: not is_next_gen_api(),
        paths=[
            # put_integration
            "$..connectionType",
            "$..passthroughBehavior",
            "$..requestParameters",
            "$..timeoutInMillis",
            # put_method
            "$..methodResponses",
            # create_authorizer
            "$..authType",
            "$..authorizerResultTtlInSeconds",
            # integration API behavior
            "token_authorizer_allow..origin",
            "token_authorizer_allow..url",
            # token_authorizer_allow LS Lambda does not populate this field
            "$..origin",
            # token_authorizer_missing LS ads this field
            "$..Type",
        ],
    )
    def test_lambda_token_authorizer(
        self,
        apigateway_lambda_integration_role,
        snapshot,
        aws_client,
        create_echo_http_server,
        _create_rest_api_with_token_authorizer,
        _create_method_and_integration,
    ):
        """Test Lambda TOKEN-based Lambda authorizer for REST API with integration.
        Authorizer example based on AWS docs:
        https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html
        """
        snapshot.add_transformer(
            [
                snapshot.transform.key_value("uri"),
                snapshot.transform.key_value("domain"),
            ]
        )
        # create REST API and token authorizer
        rest_api_id, auth_function_name, authorizer_id = _create_rest_api_with_token_authorizer()

        # get root resource
        root_resource_id = aws_client.apigateway.get_resources(restApiId=rest_api_id)["items"][0][
            "id"
        ]
        # create GET "/" method
        _create_method_and_integration(rest_api_id, root_resource_id, authorizer_id=authorizer_id)

        # create "/demo" resource
        resource_id = aws_client.apigateway.create_resource(
            restApiId=rest_api_id, parentId=root_resource_id, pathPart="demo"
        )["id"]

        # create POST "/demo" method
        put_method_response = aws_client.apigateway.put_method(
            restApiId=rest_api_id,
            resourceId=resource_id,
            httpMethod="POST",
            authorizationType="CUSTOM",
            authorizerId=authorizer_id,
            requestParameters={"method.request.header.Authorization": True},
        )
        snapshot.match("put_method_with_custom_authorizer", put_method_response)

        # create "HTTP" integration
        put_integration_response = aws_client.apigateway.put_integration(
            restApiId=rest_api_id,
            resourceId=resource_id,
            httpMethod="POST",
            type="HTTP",
            integrationHttpMethod="POST",
            uri=create_echo_http_server(trim_x_headers=True),
            credentials=apigateway_lambda_integration_role,
        )
        snapshot.match("put_integration", put_integration_response)

        aws_client.apigateway.put_method_response(
            restApiId=rest_api_id,
            resourceId=resource_id,
            httpMethod="POST",
            statusCode="200",
        )

        aws_client.apigateway.put_integration_response(
            restApiId=rest_api_id,
            resourceId=resource_id,
            httpMethod="POST",
            statusCode="200",
            selectionPattern="200",
        )

        # Deploy API Gateway
        stage_name = "test"
        aws_client.apigateway.create_deployment(restApiId=rest_api_id, stageName=stage_name)

        endpoint = api_invoke_url(
            api_id=rest_api_id, stage=stage_name, path="/demo", url_type=UrlType.PATH_BASED
        )

        def _call_and_assert(action: str | None = "allow", expected_status_code=200):
            return _invoke_and_assert(
                endpoint,
                auth_header=action,
                method="POST",
                json_body={"mykey": "myvalue"},
                expected_status_code=expected_status_code,
            )

        # Authorizer status codes:
        # https://docs.aws.amazon.com/apigateway/latest/developerguide/call-api-with-api-gateway-lambda-authorization.html
        # retry until apigateway deployment is ready
        allow_response = retry(
            _call_and_assert, retries=10, sleep=2, action="allow", expected_status_code=200
        )
        allow_response_json = json.loads(allow_response.text)
        allow_response_json.pop("headers")
        snapshot.match("token_authorizer_allow", allow_response_json)
        # Unsupported in LS: response.reason == "OK" | "Forbidden" | "Unauthorized" | "Internal Server Error"

        deny_response = _call_and_assert(action="deny", expected_status_code=403)
        snapshot.match("token_authorizer_deny", deny_response.text)

        unauthorized_response = _call_and_assert(action="unauthorized", expected_status_code=401)
        snapshot.match("token_authorizer_unauthorized", unauthorized_response.text)

        fail_response = _call_and_assert(action="fail", expected_status_code=500)
        snapshot.match("token_authorizer_fail", fail_response.text)

        missing_headers = _call_and_assert(action=None, expected_status_code=401)
        snapshot.match("token_authorizer_missing", missing_headers.text)

        root_endpoint = api_invoke_url(
            api_id=rest_api_id, stage=stage_name, path="/", url_type=UrlType.PATH_BASED
        )
        result = requests.get(root_endpoint, headers={"Authorization": "allow"}, verify=False)
        assert result.status_code == 200

        # Ideally validate authorizer through AWS testing API (not implemented in moto as of 2023-01-05)
        # https://docs.aws.amazon.com/apigateway/latest/api/API_TestInvokeAuthorizer.html
        # test_invoke_authorizer_response = apigateway_client.test_invoke_authorizer(
        #     restApiId=rest_api_id, authorizerId=authorizer_id, headers={"Authorization": "allow"}
        # )
        # snapshot.match("test_invoke_authorizer_policy", test_invoke_authorizer_response["policy"])

    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            # put_integration
            "$..connectionType",
            "$..passthroughBehavior",
            "$..requestParameters",
            "$..timeoutInMillis",
            # put_method
            "$..methodResponses",
            # create_authorizer
            "$..authType",
            "$..authorizerResultTtlInSeconds",
        ]
    )
    def test_lambda_token_authorizer_path_suffixes(
        self,
        apigateway_lambda_integration_role,
        snapshot,
        aws_client,
        _create_rest_api_with_token_authorizer,
        _create_method_and_integration,
    ):
        """
        Test Lambda TOKEN-based lambda authorizer for REST API with MOCK integration.
        Authorizer example based on AWS docs:
        https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html
        """

        # create REST API and token authorizer
        rest_api_id, auth_function_name, authorizer_id = _create_rest_api_with_token_authorizer()

        # Using output from authorizer in API Gateway mapping template:
        # https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-output.html
        # https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html
        response_template = textwrap.dedent(
            """
        {
            "stringKey": "$context.authorizer.stringKey",
            "numberKey": $context.authorizer.numberKey,
            "booleanKey": $context.authorizer.booleanKey,
            "methodArn": "$context.authorizer.methodArn"
        }
        """
        )

        # get root resource
        root_resource_id = aws_client.apigateway.get_resources(restApiId=rest_api_id)["items"][0][
            "id"
        ]
        # Create GET "/" method and integration
        response_templates = {APPLICATION_JSON: response_template}
        _create_method_and_integration(
            rest_api_id,
            root_resource_id,
            authorizer_id=authorizer_id,
            response_templates=response_templates,
        )

        # create "/demo" resource
        resource_id = aws_client.apigateway.create_resource(
            restApiId=rest_api_id, parentId=root_resource_id, pathPart="demo"
        )["id"]
        # create GET "/demo" method and integration
        _create_method_and_integration(
            rest_api_id,
            resource_id=resource_id,
            authorizer_id=authorizer_id,
            response_templates=response_templates,
        )

        # Deploy API Gateway
        stage_name = "test"
        aws_client.apigateway.create_deployment(restApiId=rest_api_id, stageName=stage_name)

        url = api_invoke_url(
            api_id=rest_api_id, stage=stage_name, path="/", url_type=UrlType.PATH_BASED
        )

        # Authorizer status codes:
        # https://docs.aws.amazon.com/apigateway/latest/developerguide/call-api-with-api-gateway-lambda-authorization.html
        # retry until apigateway deployment is ready
        allow_response = retry(
            _invoke_and_assert, url=url, auth_header="allow", retries=10, sleep=2
        )
        snapshot.match("token_authorizer_allow", json.loads(allow_response.text))

        path_snap_name_mappings = {
            "/": "token_authorizer_get_root",
            "/demo": "token_authorizer_get_demo",
            "/demo/": "token_authorizer_get_demo_single_slash",
            "/demo//": "token_authorizer_get_demo_double_slash",
            "/demo///": "token_authorizer_get_demo_triple_slash",
            "/demo#": "token_authorizer_get_demo_hash",
            "/demo?key=value": "token_authorizer_get_demo_param",
        }
        action_status_mappings = {
            "deny": 403,
            "allow": 200,
        }
        for path, snap_name in path_snap_name_mappings.items():
            for action, status in action_status_mappings.items():
                LOG.debug("Testing path: %s, action: %s", path, action)
                endpoint = api_invoke_url(
                    api_id=rest_api_id, stage=stage_name, path=path, url_type=UrlType.PATH_BASED
                )
                result = requests.get(endpoint, headers={"Authorization": action}, verify=False)
                assert result.status_code == status
                result_text = result.text
                if action == "allow":
                    result_text = json.loads(result.text)
                snapshot.match(
                    f"{snap_name}_{action}_content_type", result.headers.get("Content-Type")
                )
                snapshot.match(f"{snap_name}_{action}", result_text)

    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        paths=["$..authType", "$..integrationLatency", "$..principalId"]
    )
    def test_lambda_token_authorizer_event_payload(
        self,
        create_lambda_function,
        apigateway_lambda_integration_role,
        region_name,
        create_role_with_policy,
        snapshot,
        aws_client_factory,
        _create_rest_api_with_token_authorizer,
        _create_method_and_integration,
        secondary_region_name,
    ):
        test_region = region_name
        # test for non-default region (only locally), to ensure the API and authorizer lookup works properly
        if not is_aws_cloud():
            test_region = secondary_region_name
            snapshot.add_transformer(snapshot.transform.regex(test_region, "<region>"))

        client_factory = aws_client_factory(region_name=test_region)
        apigateway_client = client_factory.apigateway

        # create REST API and token authorizer - note: using custom API ID locally
        kwargs = {"rest_api_id": f"my-api-{short_uid()}"} if not is_aws_cloud() else {}
        rest_api_id, auth_function_name, authorizer_id = _create_rest_api_with_token_authorizer(
            region_name=test_region, **kwargs
        )

        # get root resource
        root_resource_id = apigateway_client.get_resources(restApiId=rest_api_id)["items"][0]["id"]

        # create echo Lambda
        lambda_name = f"lambda-{short_uid()}"
        response = create_lambda_function(
            handler_file=LAMBDA_ECHO_EVENT,
            func_name=lambda_name,
            runtime=Runtime.nodejs20_x,
            client=client_factory.lambda_,
        )
        lambda_echo_arn = response["CreateFunctionResponse"]["FunctionArn"]
        # create Lambda execution role with policy
        _, role_arn = create_role_with_policy(
            "Allow", "lambda:InvokeFunction", json.dumps(APIGW_ASSUME_ROLE_POLICY), "*"
        )

        # Create GET "/" method and integration
        uri = arns.apigateway_invocations_arn(lambda_echo_arn, region_name=test_region)
        kwargs = {
            "type": "AWS_PROXY",
            "uri": uri,
            "integrationHttpMethod": "POST",
            "credentials": role_arn,
        }
        _create_method_and_integration(
            rest_api_id,
            root_resource_id,
            authorizer_id=authorizer_id,
            integration_kwargs=kwargs,
            region_name=test_region,
        )

        # deploy API Gateway
        stage_name = "test"
        apigateway_client.create_deployment(restApiId=rest_api_id, stageName=stage_name)

        # invoke API, retry until API Gateway deployment is ready
        url = api_invoke_url(
            api_id=rest_api_id, stage=stage_name, path="/", url_type=UrlType.PATH_BASED
        )
        response = retry(_invoke_and_assert, url=url, auth_header="allow", retries=10, sleep=2)

        # snapshot authorizer details in response context
        req_context = response.json()["requestContext"]
        snapshot.match("response-authorizer-context", req_context["authorizer"])

        # run a few more invocations, to ensure subsequent requests contain the auth context as well
        for i in range(3):
            response = _invoke_and_assert(url=url, auth_header="allow")
            auth_context = response.json()["requestContext"]["authorizer"]
            assert auth_context.get("booleanKey")
            assert auth_context.get("numberKey")
            assert auth_context.get("stringKey")

    @markers.aws.validated
    def test_apigateway_to_appsync_integration(
        self,
        dynamodb_create_table_with_parameters,
        create_role_with_policy_for_principal,
        create_rest_apigw,
        appsync_create_api,
        aws_client,
        account_id,
        region_name,
    ):
        # create appsync api
        appsync_name = f"appsync-{short_uid()}"
        response = appsync_create_api(
            name=appsync_name,
            authenticationType="API_KEY",
        )
        appsync_id = response["apiId"]
        api_key = aws_client.appsync.create_api_key(
            apiId=appsync_id,
        )["apiKey"]["id"]

        # Create some test schema in API handling posts with names
        aws_client.appsync.start_schema_creation(apiId=appsync_id, definition=TEST_SCHEMA)

        # create dynamodb table
        table_name = f"appsync-table-{short_uid()}"
        dynamodb_create_table_with_parameters(
            TableName=table_name,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )

        aws_client.dynamodb.put_item(
            TableName=table_name,
            Item={
                "id": {"S": "1"},
                "name": {"S": "PostTitle"},
            },
        )

        _, role_arn = create_role_with_policy_for_principal(
            principal={"Service": "appsync.amazonaws.com"},
            resource="*",
            effect="Allow",
            actions=["dynamodb:*"],
        )

        # create appsync data source, in this case dynamodb
        datasource_name = f"dt_dynamodb_{short_uid()}"
        aws_client.appsync.create_data_source(
            apiId=appsync_id,
            name=datasource_name,
            type="AMAZON_DYNAMODB",
            serviceRoleArn=role_arn,
            dynamodbConfig={
                "awsRegion": region_name,
                "tableName": table_name,
            },
        )

        # create appsync resolver
        aws_client.appsync.create_resolver(
            apiId=appsync_id,
            typeName="Query",
            fieldName="singlePost",
            dataSourceName=datasource_name,
            requestMappingTemplate="""
            {
                "version" : "2017-02-28",
                "operation" : "GetItem",
                "key" : {
                    "id" : $util.dynamodb.toDynamoDBJson($ctx.args.id)
                }
            }
            """,
            responseMappingTemplate="""
            #if($ctx.result.statusCode == 200)
                $ctx.result.body
            #else
                $util.toJson($ctx.result)
            #end
            """,
        )

        # create rest api
        api_name = f"api-{short_uid()}"
        api_id, _, root_resource_id = create_rest_apigw(name=api_name)

        # create resource, method, integration
        res_id = aws_client.apigateway.create_resource(
            restApiId=api_id,
            parentId=root_resource_id,
            pathPart="graphql",
        )["id"]
        aws_client.apigateway.put_method(
            restApiId=api_id,
            resourceId=res_id,
            httpMethod="POST",
            authorizationType="NONE",
        )

        # get graphql endpoint from response uris
        graphql_endpoint = response["uris"]["GRAPHQL"]
        # extract subdomain from graphql endpoint
        if is_aws_cloud():
            subdomain = re.search(r"https?://([a-z0-9]+).*", graphql_endpoint)[1]
        else:
            subdomain = appsync_id

        _, apigw_role = create_role_with_policy_for_principal(
            principal={"Service": "apigateway.amazonaws.com"},
            resource=f"arn:{get_partition(region_name)}:appsync:{region_name}:{account_id}:apis/{appsync_id}/*",
            effect="Allow",
            actions=["appsync:GraphQL"],
        )

        graphql_request = files.load_file(GRAPHQL_REQUEST)
        aws_client.apigateway.put_integration(
            restApiId=api_id,
            resourceId=res_id,
            httpMethod="POST",
            integrationHttpMethod="POST",
            credentials=apigw_role,
            type="AWS",
            uri=f"arn:{get_partition(region_name)}:apigateway:{region_name}:{subdomain}.appsync-api:path/graphql",
            requestParameters={"integration.request.header.x-api-key": f"'{api_key}'"},
            # read from json file
            requestTemplates={"application/json": graphql_request},
        )

        aws_client.apigateway.put_method_response(
            restApiId=api_id,
            resourceId=res_id,
            httpMethod="POST",
            statusCode="200",
        )

        aws_client.apigateway.put_integration_response(
            restApiId=api_id,
            resourceId=res_id,
            httpMethod="POST",
            statusCode="200",
        )

        deployment_id = aws_client.apigateway.create_deployment(restApiId=api_id)["id"]

        # create stage
        stage_name = "dev"
        aws_client.apigateway.create_stage(
            restApiId=api_id, stageName=stage_name, deploymentId=deployment_id
        )

        # invoke api
        def call_api():
            public_endpoint = api_invoke_url(api_id=api_id, stage=stage_name, path="/graphql")
            result = requests.post(public_endpoint, verify=False)
            assert result.status_code == 200
            assert result.json() == {"data": {"singlePost": {"id": "1"}}}

        retry(call_api, retries=10, sleep=1)


class TestIAMAuthorization:
    @markers.aws.validated
    @pytest.mark.skipif(
        condition=not is_next_gen_api() and not is_aws_cloud(),
        reason="Incomplete behavior in legacy implementation",
    )
    def test_iam_authorization_missing_token(self, create_rest_apigw, aws_client, snapshot):
        # create REST API
        rest_api_id, _, root_resource_id = create_rest_apigw(name=f"test-iam-auth-{short_uid()}")

        aws_client.apigateway.put_method(
            restApiId=rest_api_id,
            resourceId=root_resource_id,
            httpMethod="GET",
            authorizationType="AWS_IAM",
        )
        aws_client.apigateway.put_method_response(
            restApiId=rest_api_id, resourceId=root_resource_id, httpMethod="GET", statusCode="200"
        )
        aws_client.apigateway.put_integration(
            restApiId=rest_api_id,
            resourceId=root_resource_id,
            httpMethod="GET",
            integrationHttpMethod="GET",
            type="MOCK",
        )
        stage_name = "dev"
        aws_client.apigateway.create_deployment(restApiId=rest_api_id, stageName=stage_name)
        url = api_invoke_url(api_id=rest_api_id, stage=stage_name, path="/")

        def _invoke_url(invoke_url: str, expected_status_code: int, headers: dict):
            invoker_response = requests.get(invoke_url, headers=headers)
            assert invoker_response.status_code == expected_status_code
            return invoker_response

        default_retry_kwargs = {
            "function": _invoke_url,
            "retries": 5,
            "sleep": 2,
            "invoke_url": url,
        }
        no_token_headers = {}
        result = retry(expected_status_code=403, headers=no_token_headers, **default_retry_kwargs)
        snapshot.match("no-token", result.json())

        wrong_auth_headers = {"Authorization": "Bearer invalid-token"}
        result = retry(expected_status_code=403, headers=wrong_auth_headers, **default_retry_kwargs)
        snapshot.match("wrong-token", result.json())

        wrong_auth_headers = {"Authorization": "invalid-token bla=test"}
        result = retry(expected_status_code=403, headers=wrong_auth_headers, **default_retry_kwargs)
        snapshot.match("wrong-token-no-bearer", result.json())

        wrong_auth_headers = {"Authorization": "Bearer invalid-token-bla=test"}
        result = retry(expected_status_code=403, headers=wrong_auth_headers, **default_retry_kwargs)
        snapshot.match("wrong-token-bearer-with-equal", result.json())

        wrong_auth_headers = {
            "Authorization": "Credential=AKIAIOSFODNN7EXAMPLE/20130524/us-east-1/s3/aws4_request"
        }
        result = retry(expected_status_code=403, headers=wrong_auth_headers, **default_retry_kwargs)
        snapshot.match("wrong-token-incomplete", result.json())

        wrong_auth_headers = {"Authorization": "Signature=random"}
        result = retry(expected_status_code=403, headers=wrong_auth_headers, **default_retry_kwargs)
        snapshot.match("wrong-token-incomplete-signature", result.json())

        wrong_auth_headers = {
            "Authorization": "AWS4-HMAC-SHA256 Credential=AKIAIOSFODNN7EXAMPLE/20130524/us-east-1/s3/aws4_request"
        }
        result = retry(expected_status_code=403, headers=wrong_auth_headers, **default_retry_kwargs)
        snapshot.match("wrong-token-incomplete-signature-with-algo", result.json())
