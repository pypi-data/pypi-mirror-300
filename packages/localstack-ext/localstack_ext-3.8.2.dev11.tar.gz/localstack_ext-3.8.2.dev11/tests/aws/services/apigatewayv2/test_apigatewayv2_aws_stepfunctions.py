import json

import requests
from localstack.aws.api.lambda_ import Runtime
from localstack.testing.pytest import markers
from localstack.utils.aws.arns import get_partition
from localstack.utils.strings import short_uid
from localstack.utils.sync import retry
from tests.aws.services.apigateway.apigateway_fixtures import api_invoke_url
from tests.aws.services.apigateway.conftest import LAMBDA_JS, is_next_gen_api

STEP_FUNCTION_DEFINITION = """
{
  "Comment": "A Hello World example of the Amazon States Language using an AWS Lambda Function",
  "StartAt": "HelloWorld",
  "States": {
    "HelloWorld": {
      "Type": "Task",
      "Resource": "%s",
      "End": true
    }
  }
}
"""


# TODO: add tests for the following integrations
#  - StartSyncExecution
#  - StopExecution
class TestHttpApiAwsProxySubtypeStepFunctions:
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            "$..headers.Server",
            # There is a difference in notation for the float type (AWS is scientific), so it changes the length
            "$..headers.Content-Length",
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
            "$..headers.x-amz-id-2",
            # wrong casing in legacy
            "$..headers.x-amzn-requestid",
            "$..headers.x-amzn-RequestId",
            # TODO: headers added as returned by the internal boto client, seems filtered in AWS, and seems like
            #  `request` headers? not sure what they are doing in the response, must come from SFN
            "$..headers.Accept-Encoding",
            "$..headers.Authorization",
            "$..headers.X-Amz-Date",
        ],
    )
    @markers.aws.validated
    def test_step_functions_integration_start_execution(
        self,
        create_v2_api,
        create_stepfunctions,
        create_lambda_function,
        create_role,
        create_policy,
        aws_client,
        region_name,
        snapshot,
    ):
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("IntegrationId"),
                snapshot.transform.resource_name(),
                snapshot.transform.key_value(
                    "startDate", reference_replacement=False, value_replacement="<start-date>"
                ),
                # headers transformers
                snapshot.transform.key_value(
                    "Date", reference_replacement=False, value_replacement="<date>"
                ),
                snapshot.transform.key_value("x-amzn-RequestId"),
                snapshot.transform.key_value("x-amz-id-2"),
                snapshot.transform.key_value("apigw-requestid"),
            ]
        )

        create_api = create_v2_api(ProtocolType="HTTP", Name=f"http-sfn-{short_uid()}")
        api_id = create_api["ApiId"]
        # create IAM role and policy for API Gateway to invoke Step Functions
        role_name = f"apigw-role-{short_uid()}"
        assume_role_doc = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Principal": {"Service": "apigateway.amazonaws.com"},
                    "Effect": "Allow",
                }
            ],
        }
        apigw_role_arn = create_role(
            RoleName=role_name, AssumeRolePolicyDocument=json.dumps(assume_role_doc)
        )["Role"]["Arn"]
        aws_client.iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=f"arn:{get_partition(region_name)}:iam::aws:policy/AWSStepFunctionsFullAccess",
        )

        # create Lambda function
        lambda_name = f"{short_uid()}"
        lambda_fn = LAMBDA_JS % "Foobar"
        lambda_arn = create_lambda_function(
            handler_file=lambda_fn, func_name=lambda_name, runtime=Runtime.nodejs20_x
        )["CreateFunctionResponse"]["FunctionArn"]

        # create IAM role and policy for Step Functions to invoke Lambda
        role_name = f"sfn-role-{short_uid()}"
        assume_role_doc = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Principal": {"Service": "states.amazonaws.com"},
                    "Effect": "Allow",
                }
            ],
        }
        policy_doc = {
            "Version": "2012-10-17",
            "Statement": [{"Effect": "Allow", "Action": "lambda:*", "Resource": "*"}],
        }
        role_arn = create_role(
            RoleName=role_name, AssumeRolePolicyDocument=json.dumps(assume_role_doc)
        )["Role"]["Arn"]
        policy_arn = create_policy(
            PolicyName=f"test-policy-{short_uid()}", PolicyDocument=json.dumps(policy_doc)
        )["Policy"]["Arn"]
        aws_client.iam.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
        # create Step Functions state machine
        sfn_state_machine_arn = create_stepfunctions(
            name=f"{short_uid()}",
            definition=STEP_FUNCTION_DEFINITION % lambda_arn,
            roleArn=role_arn,
        )
        # create API Gateway integration with Step Functions
        integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            CredentialsArn=apigw_role_arn,
            IntegrationType="AWS_PROXY",
            IntegrationSubtype="StepFunctions-StartExecution",
            PayloadFormatVersion="1.0",
            RequestParameters={
                "StateMachineArn": sfn_state_machine_arn,
                "Input": "$request.body",
            },
        )
        snapshot.match("sfn-integration", integration)
        # create API Gateway route targeting Step Functions service
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="NONE",
            RouteKey="POST /test",
            Target=f"integrations/{integration['IntegrationId']}",
        )
        # create API Gateway stage
        aws_client.apigatewayv2.create_stage(ApiId=api_id, StageName="$default", AutoDeploy=True)

        # invoke API Gateway
        endpoint = api_invoke_url(api_id=api_id, path="test")

        def check_result() -> requests.Response:
            result = requests.post(
                endpoint,
                headers={"Content-Type": "application/json"},
                verify=False,
                json={"input": "{}"},
            )
            assert result.status_code == 200
            assert sfn_state_machine_arn.split(":")[-1] in result.json()["executionArn"]
            return result

        response = retry(check_result, retries=5, sleep=3)

        snapshot_response = {
            "content": response.json(),
            "headers": dict(response.headers),
        }
        snapshot.match("invoke-response", snapshot_response)
        # LocalStack returns the `startDate` field in the regular float notation, and AWS returns it in scientific
        # notation.
        # LocalStack: 1726326490.963
        # AWS: 1.726326538934E9

        # TODO: add test cases for NextGen for 2 missing integrations
        #  add error test cases
