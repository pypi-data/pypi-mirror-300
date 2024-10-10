import json
import logging

import pytest
from localstack.http import Response
from localstack.testing.aws.util import is_aws_cloud
from localstack.testing.pytest.fixtures import PUBLIC_HTTP_ECHO_SERVER_URL
from localstack.utils import testutil
from localstack.utils.json import json_safe
from localstack.utils.strings import short_uid
from localstack.utils.sync import wait_until
from pytest_httpserver import HTTPServer
from rolo import Request
from tests.aws.services.apigateway.conftest import APIGW_ASSUME_ROLE_POLICY

LOG = logging.getLogger(__name__)

# TODO when we remove legacy, we can uncomment the `isAuthorized` line to be strict about headers capitalization
LAMBDA_AUTHORIZER_V2_SIMPLE_RESPONSE = """
import json

def handler(event, context):
    print(json.dumps(event))
    headers = event["headers"]
    return {
        # "isAuthorized": headers["x-user"] == "allow",
        "isAuthorized": headers.get("x-user") == "allow" or headers.get("X-User") == "allow",
        "context": {"event": json.dumps(event)},
    }
"""


LAMBDA_AUTHORIZER_IAM_RESPONSE = """
import json

def handler(event, context, *args):
    print(json.dumps(event))
    headers = event.get("headers")

    if not (resource := headers.get("allow-resource")):
        if event["version"] == "1.0":
            resource = event.get("methodArn")
            allow = headers.get("X-User") == "allow"
        else:
            resource = event.get("routeArn")
            # allow = headers.get("x-user") == "allow"
            allow = headers.get("x-user") == "allow" or headers.get("X-User") == "allow"

    allow = "Allow" if allow else "Deny"

    return {
        "principalId": event["requestContext"]["accountId"],
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {"Action": "execute-api:Invoke", "Effect": allow, "Resource": resource}
            ],
        },
        "context": {"event": json.dumps(event)}
    }
"""


@pytest.fixture
def create_v2_api(aws_client):
    apis = []

    def _create(**kwargs):
        if not kwargs.get("Name"):
            kwargs["Name"] = f"api-{short_uid()}"
        response = aws_client.apigatewayv2.create_api(**kwargs)
        apis.append(response)
        return response

    yield _create

    for api in apis:
        try:
            aws_client.apigatewayv2.delete_api(ApiId=api["ApiId"])
        except Exception as e:
            LOG.debug("Unable to delete API Gateway v2 API %s: %s", api, e)


@pytest.fixture
def apigw_echo_http_server(httpserver: HTTPServer):
    """Spins up a local HTTP echo server and returns the endpoint URL
    Aims at emulating more closely the output of httpbin.org that is used to create the
    snapshots
    TODO tests the behavior and outputs of all fields"""

    def _echo(request: Request) -> Response:
        headers = dict(request.headers)
        headers.pop("Connection", None)
        try:
            json_body = json.loads(request.data)
        except json.JSONDecodeError:
            json_body = None

        if raw_uri := request.environ.get("RAW_URI"):
            # strip leading slashes as httpbin.org would do
            raw_url = f"{request.host_url}{raw_uri.lstrip('/')}"
        else:
            raw_url = request.url

        multivalue_args = {}
        for key, value in request.args.items(multi=True):
            if key in multivalue_args:
                if isinstance(multivalue_args[key], list):
                    multivalue_args[key].append(value)
                else:
                    multivalue_args[key] = [multivalue_args[key], value]
            else:
                multivalue_args[key] = value

        result = {
            "args": multivalue_args,
            "data": request.data,
            "files": request.files,
            "form": request.form,
            "headers": headers,
            "json": json_body,
            "origin": request.remote_addr,
            "url": raw_url,
            "method": request.method,
        }
        response_body = json.dumps(json_safe(result))
        return Response(
            response_body,
            status=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": "true",
                "Content-Type": "application/json",
            },
        )

    httpserver.expect_request("").respond_with_handler(_echo)
    http_endpoint = httpserver.url_for("/")

    return http_endpoint


@pytest.fixture
def apigw_echo_http_server_anything(apigw_echo_http_server):
    """
    Returns an HTTP echo server URL for POST requests that work both locally and for parity tests (against real AWS)
    """
    if is_aws_cloud():
        return f"{PUBLIC_HTTP_ECHO_SERVER_URL}/anything"

    return f"{apigw_echo_http_server}/anything"


@pytest.fixture
def add_permission_for_integration_lambda(aws_client, account_id, region_name):
    def _add_permission(api_id, lambda_arn):
        aws_client.lambda_.add_permission(
            FunctionName=lambda_arn,
            StatementId=str(short_uid()),
            Action="lambda:InvokeFunction",
            Principal="apigateway.amazonaws.com",
            SourceArn=f"arn:aws:execute-api:{region_name}:{account_id}:{api_id}/*/*",
        )

    yield _add_permission


@pytest.fixture
def apigwv2_httpbin_headers_transformers(snapshot):
    snapshot.add_transformers_list(
        [
            # as APIGW has multiple servers, the origin IP address varies between requests
            snapshot.transform.key_value("origin", "<origin>", reference_replacement=False),
            snapshot.transform.key_value("Forwarded", "<forwarded>", reference_replacement=False),
            snapshot.transform.jsonpath("$..headers.X-Amzn-Trace-Id", "trace-id"),
            snapshot.transform.jsonpath("$..headers.Host", "host"),
        ]
    )


@pytest.fixture
def add_aws_proxy_snapshot_transformers(snapshot):
    # TODO: update global transformers, but we will need to regenerate all snapshots at once
    snapshot.add_transformers_list(
        [
            snapshot.transform.resource_name(),
            snapshot.transform.key_value("extendedRequestId"),
            snapshot.transform.key_value("requestId"),
            snapshot.transform.key_value(
                "requestTime", value_replacement="<time>", reference_replacement=False
            ),
            snapshot.transform.key_value("sourceIp"),
            snapshot.transform.key_value("domainName"),
            snapshot.transform.key_value(
                "time", value_replacement="<time>", reference_replacement=False
            ),
            snapshot.transform.key_value(
                "requestTimeEpoch", value_replacement="<time-epoch>", reference_replacement=False
            ),
            snapshot.transform.key_value(
                "timeEpoch", value_replacement="<time-epoch>", reference_replacement=False
            ),
            snapshot.transform.jsonpath("$..headers.Host", value_replacement="host"),
            snapshot.transform.jsonpath("$..multiValueHeaders.Host[0]", value_replacement="host"),
        ],
        priority=-1,
    )

    transformed_headers = []
    for header in ("X-Forwarded-For", "X-Forwarded-Port", "X-Forwarded-Proto", "X-Amzn-Trace-Id"):
        transformed_headers.append(
            snapshot.transform.key_value(
                header,
                value_replacement=f"<{header}>",
                reference_replacement=False,
            ),
        )
        transformed_headers.append(
            snapshot.transform.key_value(
                header.lower(),
                value_replacement=f"<{header.lower()}>",
                reference_replacement=False,
            ),
        )
    snapshot.add_transformers_list(transformed_headers, priority=-1)


@pytest.fixture
def create_v2_vpc_link(aws_client):
    vpc_links = []

    def _create(**kwargs):
        if not kwargs.get("Name"):
            kwargs["Name"] = f"vpc-link-{short_uid()}"
        response = aws_client.apigatewayv2.create_vpc_link(**kwargs)
        vpc_id = response["VpcLinkId"]
        vpc_links.append(vpc_id)
        wait_until(
            lambda: aws_client.apigatewayv2.get_vpc_link(VpcLinkId=vpc_id)["VpcLinkStatus"]
            == "AVAILABLE",
            _max_wait=360,
        )

        return response

    yield _create

    for vpc_link_id in vpc_links:
        try:
            aws_client.apigatewayv2.delete_vpc_link(VpcLinkId=vpc_link_id)
        except Exception as e:
            LOG.debug("Unable to delete API Gateway v2 VPC Link %s: %s", vpc_link_id, e)


@pytest.fixture
def ec2_create_security_group_with_vpc(aws_client):
    # TODO: fix ec2_create_security_group in Community
    ec2_sgs = []

    def factory(ports=None, **kwargs):
        if "GroupName" not in kwargs:
            kwargs["GroupName"] = f"test-sg-{short_uid()}"
        security_group = aws_client.ec2.create_security_group(**kwargs)

        permissions = [
            {
                "FromPort": port,
                "IpProtocol": "tcp",
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                "ToPort": port,
            }
            for port in ports or []
        ]

        aws_client.ec2.authorize_security_group_ingress(
            GroupId=security_group["GroupId"],
            IpPermissions=permissions,
        )

        ec2_sgs.append((security_group["GroupId"], kwargs.get("VpcId")))
        return security_group

    yield factory

    for sg_group_id, vpc_id in ec2_sgs:
        try:
            params = {"GroupId": sg_group_id}
            if vpc_id:
                params["VpcId"] = vpc_id

            aws_client.ec2.delete_security_group(**params)
        except Exception as e:
            LOG.debug("Error cleaning up EC2 security group: %s, %s", sg_group_id, e)


@pytest.fixture
def create_lambda_authorizer(create_lambda_function, aws_client, region_name):
    def _create(lambda_source: str, region_name=region_name):
        function_name = f"test_apigw_auth-{short_uid()}"

        # create Lambda authorizer
        zip_file = testutil.create_lambda_archive(lambda_source, get_content=True)
        response = create_lambda_function(
            func_name=function_name, zip_file=zip_file, client=aws_client.lambda_
        )
        function_arn = response["CreateFunctionResponse"]["FunctionArn"]

        # allow apigateway to call lambda functions, e.g., our trigger lambda
        aws_client.lambda_.add_permission(
            FunctionName=function_name,
            StatementId=f"invoke-lambda-{short_uid()}",
            Action="lambda:InvokeFunction",
            Principal="apigateway.amazonaws.com",
        )

        return (
            function_arn,
            f"arn:aws:apigateway:{region_name}:lambda:path/2015-03-31/functions/{function_arn}/invocations",
        )

    yield _create


@pytest.fixture
def create_iam_role_and_attach_policy(create_role, aws_client):
    """
    Creates an IAM role and attaches a policy to it. The role is deleted after the test.
    NOTE: use and abuse of this fixture and use existing AWS policies like,
    'arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess' or
    'arn:aws:iam::aws:policy/AmazonKinesisFullAccess' instead of creating a new policy.
    """

    def _create(policy_arn: str, assume_role_policy: dict = APIGW_ASSUME_ROLE_POLICY):
        role_name = f"role-{short_uid()}"
        # Create the IAM role
        response = create_role(
            RoleName=role_name, AssumeRolePolicyDocument=json.dumps(assume_role_policy)
        )

        # Get the newly created role ARN
        role_arn = response["Role"]["Arn"]

        # Attach the policy to the role
        aws_client.iam.attach_role_policy(PolicyArn=policy_arn, RoleName=role_name)
        return role_arn

    yield _create
