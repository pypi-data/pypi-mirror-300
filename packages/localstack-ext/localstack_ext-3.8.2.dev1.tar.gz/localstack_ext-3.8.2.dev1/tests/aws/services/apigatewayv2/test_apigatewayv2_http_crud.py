import pytest
from botocore.exceptions import ClientError
from localstack.aws.api.lambda_ import Runtime
from localstack.pro.core.services.cognito_idp.cognito_utils import get_issuer_url
from localstack.testing.aws.util import is_aws_cloud
from localstack.testing.pytest import markers
from localstack.utils.aws import arns
from localstack.utils.aws.arns import get_partition
from localstack.utils.strings import short_uid
from localstack.utils.sync import retry
from tests.aws.services.apigateway.conftest import LAMBDA_HELLO, is_next_gen_api
from tests.aws.services.apigatewayv2.conftest import LAMBDA_AUTHORIZER_V2_SIMPLE_RESPONSE

TEST_LAMBDA_SIMPLE = """
def handler(event, context):
    return {}
"""


@pytest.fixture
def create_dummy_integration(aws_client):
    """This is a dummy integration to be used only to test CRUD operations over the provider."""

    def _create(api_id: str):
        integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            IntegrationUri="https://example.com",
            IntegrationMethod="GET",
            PayloadFormatVersion="1.0",
        )
        route = aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="ANY /api",
            Target=f"integrations/{integration['IntegrationId']}",
            AuthorizationType="NONE",
        )
        return integration, route

    return _create


@pytest.mark.skipif(
    not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in legacy"
)
class TestApigatewayV2HttpDeploymentCrud:
    @pytest.fixture(autouse=True)
    def deployment_transformers(self, snapshot):
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("api-id"),
                snapshot.transform.key_value("DeploymentId"),
            ]
        )

    @markers.aws.validated
    def test_get_deployment(self, create_v2_api, aws_client, create_dummy_integration, snapshot):
        apigw_client = aws_client.apigatewayv2
        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]
        snapshot.match("api-id", api_id)
        create_dummy_integration(api_id)

        response = apigw_client.create_deployment(ApiId=api_id)
        deployment_id = response["DeploymentId"]

        # Get deployments from invalid api
        with pytest.raises(ClientError) as e:
            apigw_client.get_deployments(ApiId="invalidId")
        snapshot.match("get-deployments-invalid-api", e.value.response)

        # Get deployment from invalid api
        with pytest.raises(ClientError) as e:
            apigw_client.get_deployment(ApiId="invalidId", DeploymentId=deployment_id)
        snapshot.match("get-deployment-invalid-api", e.value.response)

        # Get deployment with invalid deployment
        with pytest.raises(ClientError) as e:
            apigw_client.get_deployment(ApiId=api_id, DeploymentId="invalidId")
        snapshot.match("get-deployment-invalid-deployment", e.value.response)

        # Get deployments
        response = apigw_client.get_deployments(ApiId=api_id)
        snapshot.match("get-deployments", response)

        # Get deployment
        response = apigw_client.get_deployment(ApiId=api_id, DeploymentId=deployment_id)
        snapshot.match("get-deployment", response)

    @markers.aws.validated
    def test_create_deployment(self, create_v2_api, aws_client, snapshot, create_dummy_integration):
        apigw_client = aws_client.apigatewayv2
        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]
        snapshot.match("api-id", api_id)
        create_dummy_integration(api_id)

        apigw_client.create_stage(ApiId=api_id, StageName="stage")
        apigw_client.create_stage(ApiId=api_id, StageName="auto", AutoDeploy=True)

        def _wait_for_auto_deploy():
            _response = apigw_client.get_stage(ApiId=api_id, StageName="auto")
            assert _response.get("DeploymentId")
            return _response

        # On aws there can be a delay for the deployment after creating a auto-deploy stage
        response = retry(_wait_for_auto_deploy)
        snapshot.match("create_auto-stage", response)

        def _sort_stages(stages: list[dict]):
            return sorted(stages, key=lambda stage: stage["StageName"])

        response = apigw_client.get_stages(ApiId=api_id)
        snapshot.match("stages-before-deployments", _sort_stages(response["Items"]))

        with pytest.raises(ClientError) as e:
            apigw_client.create_deployment(ApiId="invalidId")
        snapshot.match("create-invalid-api-id", e.value.response)

        # if a stage name is provided, it must be of an existing stage
        with pytest.raises(ClientError) as e:
            apigw_client.create_deployment(ApiId=api_id, StageName="stage1")
        snapshot.match("create-with-invalid-stage", e.value.response)

        # A deployment can be created with no stage
        response = apigw_client.create_deployment(ApiId=api_id)
        snapshot.match("create-with-no-stage", response)

        # A deployment with a stage name will attach itself to the stage
        response = apigw_client.create_deployment(ApiId=api_id, StageName="stage")
        snapshot.match("create-with-stage", response)

        response = apigw_client.get_stages(ApiId=api_id)
        snapshot.match("stages-after-named-stage-deployment", _sort_stages(response["Items"]))

        # A deployment to an auto-deploy stage is created, but will return "FAILED"
        response = apigw_client.create_deployment(ApiId=api_id, StageName="auto")
        snapshot.match("create-with-auto-deploy-stage", response)

        response = apigw_client.get_stages(ApiId=api_id)
        snapshot.match("get-stages-after", _sort_stages(response["Items"]))

    @markers.aws.validated
    def test_update_deployment(self, create_v2_api, aws_client, snapshot, create_dummy_integration):
        apigw_client = aws_client.apigatewayv2
        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]
        snapshot.match("api-id", api_id)
        create_dummy_integration(api_id)

        apigw_client.create_stage(ApiId=api_id, StageName="stage")

        response = apigw_client.create_deployment(ApiId=api_id)
        snapshot.match("create-with-no-stage", response)
        deployment_id = response["DeploymentId"]

        # Attempt update with invalid api_id
        with pytest.raises(ClientError) as e:
            apigw_client.update_deployment(
                ApiId="invalidID", DeploymentId=deployment_id, Description="invalid description"
            )
        snapshot.match("update-with-invalid-api", e.value.response)

        # Attempt update with invalid deployment id
        with pytest.raises(ClientError) as e:
            apigw_client.update_deployment(
                ApiId=api_id, DeploymentId="invalidID", Description="invalid description"
            )
        snapshot.match("update-with-invalid-deployment", e.value.response)

        # Update without description
        response = apigw_client.update_deployment(ApiId=api_id, DeploymentId=deployment_id)
        snapshot.match("update-with-no-description", response)

        # Update the deployment description
        response = apigw_client.update_deployment(
            ApiId=api_id, DeploymentId=deployment_id, Description="description"
        )
        snapshot.match("update-deployment-with-description", response)

        # Update override description
        response = apigw_client.update_deployment(ApiId=api_id, DeploymentId=deployment_id)
        snapshot.match("update-override-description", response)

    @markers.aws.validated
    def test_delete_deployment(self, create_v2_api, aws_client, snapshot, create_dummy_integration):
        apigw_client = aws_client.apigatewayv2
        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]
        snapshot.match("api-id", api_id)
        create_dummy_integration(api_id)

        apigw_client.create_stage(ApiId=api_id, StageName="stage")

        response = apigw_client.create_deployment(ApiId=api_id, StageName="stage")
        snapshot.match("create-deployment", response)
        deployment_id = response["DeploymentId"]

        # Attempt to delete from an invalid api id
        with pytest.raises(ClientError) as e:
            apigw_client.delete_deployment(ApiId="invalidID", DeploymentId=deployment_id)
        snapshot.match("delete-invalid-api-id", e.value.response)

        # Attempt to delete an invalid deployment
        with pytest.raises(ClientError) as e:
            apigw_client.delete_deployment(ApiId=api_id, DeploymentId="invalidID")
        snapshot.match("delete-invalid-deployment-id", e.value.response)

        # Attempt to delete while attach to a stage
        with pytest.raises(ClientError) as e:
            apigw_client.delete_deployment(ApiId=api_id, DeploymentId=deployment_id)
        snapshot.match("delete-with-stage-still-pointing", e.value.response)

        apigw_client.delete_stage(ApiId=api_id, StageName="stage")

        # Successful delete
        response = apigw_client.delete_deployment(ApiId=api_id, DeploymentId=deployment_id)
        snapshot.match("delete-deployment", response)


@pytest.mark.skipif(
    not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in legacy"
)
class TestApigatewayV2HttpStageCrud:
    @pytest.fixture(autouse=True)
    def deployment_transformers(self, snapshot):
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("api-id"),
                snapshot.transform.key_value("DeploymentId"),
            ]
        )

    @markers.aws.validated
    def test_get_stage(self, create_v2_api, aws_client, snapshot, create_dummy_integration):
        apigw_client = aws_client.apigatewayv2
        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]
        snapshot.match("api-id", api_id)
        create_dummy_integration(api_id)
        apigw_client.create_stage(ApiId=api_id, StageName="stage")

        # Attempt get stages invalid api id
        with pytest.raises(ClientError) as e:
            apigw_client.get_stages(ApiId="invalidID")
        snapshot.match("get-stages-invalid-api", e.value.response)

        # Attempt get stage invalid api id
        with pytest.raises(ClientError) as e:
            apigw_client.get_stage(ApiId="invalidID", StageName="stage")
        snapshot.match("get-stage-invalid-api", e.value.response)

        # Attempt get stage invalid stage name
        with pytest.raises(ClientError) as e:
            apigw_client.get_stage(ApiId=api_id, StageName="invalid")
        snapshot.match("get-stage-invalid-stage-name", e.value.response)

        # Successful get stages
        response = apigw_client.get_stages(ApiId=api_id)
        snapshot.match("get-stages", response)

        # Successful get stage
        response = apigw_client.get_stage(ApiId=api_id, StageName="stage")
        snapshot.match("get-stage", response)

    @markers.aws.validated
    def test_create_stage(self, create_v2_api, aws_client, snapshot, create_dummy_integration):
        apigw_client = aws_client.apigatewayv2
        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]
        snapshot.match("api-id", api_id)
        integration, _ = create_dummy_integration(api_id)

        def _wait_for_auto_deploy(previous_deploy_id: str = ""):
            _response = apigw_client.get_stage(ApiId=api_id, StageName="auto")
            assert _response.get("DeploymentId") and _response["DeploymentId"] != previous_deploy_id
            return _response

        # Attempt to create stage with invalid api
        with pytest.raises(ClientError) as e:
            apigw_client.create_stage(ApiId="invalid", StageName="stage")
        snapshot.match("create-stage-invalid-api", e.value.response)

        # Attempt to create stage with no stage name
        with pytest.raises(ClientError) as e:
            apigw_client.create_stage(ApiId=api_id, StageName="")
        snapshot.match("create-stage-empty-string", e.value.response)

        # Attempt to create stage with /
        with pytest.raises(ClientError) as e:
            apigw_client.create_stage(ApiId=api_id, StageName="stage/name")
        snapshot.match("create-stage-with-forward-slashes", e.value.response)

        # Attempt to create stage with $
        with pytest.raises(ClientError) as e:
            apigw_client.create_stage(ApiId=api_id, StageName="$stage")
        snapshot.match("create-stage-with-special-char", e.value.response)

        # Successful stage creation
        response = apigw_client.create_stage(ApiId=api_id, StageName="stage")
        snapshot.match("create-stage", response)

        # attempt to create stage with same name
        with pytest.raises(ClientError) as e:
            apigw_client.create_stage(ApiId=api_id, StageName="stage")
        snapshot.match("create-stage-with-same-name", e.value.response)

        # create $default stage
        response = apigw_client.create_stage(ApiId=api_id, StageName="$default")
        snapshot.match("create-default-stage", response)

        # create stage auto deploy
        response = apigw_client.create_stage(ApiId=api_id, StageName="auto", AutoDeploy=True)
        snapshot.match("create-stage-auto", response)
        # On aws there can be a delay for the deployment after creating an auto-deploy stage
        response = retry(_wait_for_auto_deploy)
        snapshot.match("get-stage-auto", response)
        auto_deploy_id = response["DeploymentId"]

        # create Stage from existing deployment
        response = apigw_client.create_stage(
            ApiId=api_id, StageName="from-existing", DeploymentId=auto_deploy_id
        )
        snapshot.match("create-stage-from-existing", response)

        # adding a route will trigger a deployment
        apigw_client.create_route(
            ApiId=api_id,
            RouteKey="ANY /new",
            Target=f"integrations/{integration['IntegrationId']}",
            AuthorizationType="NONE",
        )
        response = retry(lambda: _wait_for_auto_deploy(auto_deploy_id))
        snapshot.match("auto-deploy-stage", response)

    @markers.aws.validated
    def test_update_stage(self, create_v2_api, aws_client, snapshot, create_dummy_integration):
        apigw_client = aws_client.apigatewayv2
        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]
        snapshot.match("api-id", api_id)
        create_dummy_integration(api_id)
        apigw_client.create_stage(ApiId=api_id, StageName="stage")

        # attempt to update stage with invalid api id
        with pytest.raises(ClientError) as e:
            apigw_client.update_stage(
                ApiId="invalidId", StageName="stage", Description="description"
            )
        snapshot.match("update-with-invalid-api", e.value.response)

        # attempt to update stage with invalid stage name
        with pytest.raises(ClientError) as e:
            apigw_client.update_stage(ApiId=api_id, StageName="invalid", Description="description")
        snapshot.match("update-with-invalid-stage-name", e.value.response)

        # Update stage description
        response = apigw_client.update_stage(
            ApiId=api_id, StageName="stage", Description="description"
        )
        snapshot.match("update-stage", response)

        # update stage deployment
        deployment_id = apigw_client.create_deployment(ApiId=api_id)["DeploymentId"]
        response = apigw_client.update_stage(
            ApiId=api_id, StageName="stage", DeploymentId=deployment_id
        )
        snapshot.match("update-stage-deployment", response)

        # Attempt to update to auto deploy and set deployment id
        with pytest.raises(ClientError) as e:
            apigw_client.update_stage(
                ApiId=api_id, StageName="stage", AutoDeploy=True, DeploymentId=deployment_id
            )
        snapshot.match("update-auto-deploy-and-deployment-id", e.value.response)

        # Assert that the change to autodeploy was not applied
        response = apigw_client.get_stage(ApiId=api_id, StageName="stage")
        snapshot.match("get-stage-after-auto-deploy-update-fail", response)

        # update stage to auto deploy
        response = apigw_client.update_stage(ApiId=api_id, StageName="stage", AutoDeploy=True)
        snapshot.match("update-stage-auto", response)

        # Attempt to update deployment of auto deploy stage
        with pytest.raises(ClientError) as e:
            apigw_client.update_stage(ApiId=api_id, StageName="stage", DeploymentId=deployment_id)
        snapshot.match("update-stage-deployment-auto-deploy", e.value.response)

    @markers.aws.validated
    def test_delete_stage(self, create_v2_api, aws_client, snapshot, create_dummy_integration):
        apigw_client = aws_client.apigatewayv2
        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]
        snapshot.match("api-id", api_id)
        create_dummy_integration(api_id)
        apigw_client.create_stage(ApiId=api_id, StageName="stage")

        # Attempt to delete stage with invalid api id
        with pytest.raises(ClientError) as e:
            apigw_client.delete_stage(ApiId="invalidId", StageName="stage")
        snapshot.match("delete-stage-invalid-api", e.value.response)

        # attempt to delete stage with invalid name
        with pytest.raises(ClientError) as e:
            apigw_client.delete_stage(ApiId=api_id, StageName="invalid")
        snapshot.match("delete-stage-invalid-name", e.value.response)

        # Successful delete
        response = apigw_client.delete_stage(ApiId=api_id, StageName="stage")
        snapshot.match("delete-stage", response)

    @markers.aws.validated
    def test_auto_deploy_stage_http(
        self,
        create_v2_api,
        aws_client,
        create_lambda_function,
        region_name,
        snapshot,
    ):
        apigw_client = aws_client.apigatewayv2

        http_api = create_v2_api(ProtocolType="HTTP", Target="https://httpbin.org/anything")
        api_id = http_api["ApiId"]

        previous_deploy_id = ""

        retries = 5 if is_aws_cloud() else 1
        sleep = 1 if is_aws_cloud() else 0.5

        def _wait_for_auto_deploy():
            _response = apigw_client.get_stage(ApiId=api_id, StageName="$default")
            assert _response.get("DeploymentId") and _response["DeploymentId"] != previous_deploy_id
            return _response

        # Original deployment
        response = retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)
        previous_deploy_id = response["DeploymentId"]

        # Creating a different api doesn't trigger
        create_v2_api(ProtocolType="HTTP")
        with pytest.raises(AssertionError):
            retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)

        # update api triggers
        apigw_client.update_api(ApiId=api_id, CorsConfiguration={"AllowCredentials": True})
        response = retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)
        previous_deploy_id = response["DeploymentId"]

        # Create integration doesn't trigger
        integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            IntegrationUri="https://httpbin.org/anything",
            IntegrationMethod="GET",
            PayloadFormatVersion="1.0",
        )
        with pytest.raises(AssertionError):
            retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)

        # Creating a route triggers
        route = apigw_client.create_route(
            ApiId=api_id,
            RouteKey="ANY /api",
            Target=f"integrations/{integration['IntegrationId']}",
            AuthorizationType="NONE",
        )
        response = retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)
        previous_deploy_id = response["DeploymentId"]

        # Updating a route triggers
        apigw_client.update_route(ApiId=api_id, RouteId=route["RouteId"], AuthorizationType="NONE")
        response = retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)
        previous_deploy_id = response["DeploymentId"]

        # Updating an integration triggers
        apigw_client.update_integration(
            ApiId=api_id, IntegrationId=integration["IntegrationId"], PassthroughBehavior="NEVER"
        )
        response = retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)
        previous_deploy_id = response["DeploymentId"]

        # Deleting a route triggers
        apigw_client.delete_route(ApiId=api_id, RouteId=route["RouteId"])
        response = retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)
        previous_deploy_id = response["DeploymentId"]

        # deleting an integration doesn't trigger
        apigw_client.delete_integration(ApiId=api_id, IntegrationId=integration["IntegrationId"])
        with pytest.raises(AssertionError):
            retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)

        # creates a lambda authorizer
        lambda_name = f"int-{short_uid()}"
        lambda_arn = create_lambda_function(
            handler_file=TEST_LAMBDA_SIMPLE,
            func_name=lambda_name,
            runtime=Runtime.python3_12,
        )["CreateFunctionResponse"]["FunctionArn"]
        auth_url = arns.apigateway_invocations_arn(lambda_arn, region_name)

        # creating an authorizer doesn't trigger
        authorizer = apigw_client.create_authorizer(
            ApiId=api_id,
            Name="test-authorizer",
            AuthorizerUri=auth_url,
            AuthorizerType="REQUEST",
            IdentitySource=["$request.header.Authorization"],
            AuthorizerPayloadFormatVersion="2.0",
        )
        with pytest.raises(AssertionError):
            retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)

        # updating an authorizer triggers (even if not attached)
        apigw_client.update_authorizer(
            ApiId=api_id, AuthorizerId=authorizer["AuthorizerId"], AuthorizerUri=auth_url
        )
        response = retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)
        previous_deploy_id = response["DeploymentId"]

        deployments = apigw_client.get_deployments(ApiId=api_id)
        snapshot.match("get-deployments", deployments)

    @markers.aws.validated
    def test_create_stage_after_deployment(
        self, create_v2_api, aws_client, snapshot, create_dummy_integration
    ):
        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]
        snapshot.match("api-id", api_id)
        integration, _ = create_dummy_integration(api_id)

        create_deployment = aws_client.apigatewayv2.create_deployment(ApiId=api_id)
        snapshot.match("create-with-no-stage", create_deployment)
        deployment_id = create_deployment["DeploymentId"]

        create_stage = aws_client.apigatewayv2.create_stage(
            ApiId=api_id, StageName="test", DeploymentId=deployment_id
        )
        snapshot.match("create-stage-with-deployment", create_stage)

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.create_stage(
                ApiId=api_id, StageName="another", DeploymentId="bad-id"
            )
        snapshot.match("create-stage-with-bad-deployment", e.value.response)

        create_stage_auto = aws_client.apigatewayv2.create_stage(
            ApiId=api_id,
            StageName="test-auto",
            DeploymentId=deployment_id,
            AutoDeploy=True,
        )
        snapshot.match("create-stage-with-deployment-auto-deploy", create_stage_auto)

        deployments = aws_client.apigatewayv2.get_deployments(ApiId=api_id)
        snapshot.match("get-deployments", deployments)

        deployments = aws_client.apigatewayv2.get_stages(ApiId=api_id)
        snapshot.match("get-stages", deployments)


class TestApigatewayV2HttpIntegrationCrud:
    # TODO add the ConnectionType to create_integration
    @pytest.mark.skipif(
        not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in legacy"
    )
    @markers.aws.validated
    def test_request_parameters_headers(self, create_v2_api, aws_client, snapshot):
        apigw_client = aws_client.apigatewayv2

        snapshot.add_transformers_list([snapshot.transform.key_value("IntegrationId")])

        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]

        create_integration_kwargs = {
            "ApiId": api_id,
            "IntegrationType": "HTTP_PROXY",
            "IntegrationUri": "https://example.com",
            "IntegrationMethod": "GET",
            "PayloadFormatVersion": "1.0",
            "RequestParameters": {"append:header.header_value": "$request.headers.foo"},
        }

        # "$request.headers.foo" will be rejected
        with pytest.raises(ClientError) as e:
            apigw_client.create_integration(**create_integration_kwargs)
        snapshot.match("create-invalid-mapping", e.value.response)

        # Can't do twice the same headers
        create_integration_kwargs["RequestParameters"] = {
            "append:header.header_1": "static value",
            "overwrite:header.header_1": "static value",
        }
        with pytest.raises(ClientError) as e:
            apigw_client.create_integration(**create_integration_kwargs)
        snapshot.match("create-duplicate-headers", e.value.response)

        # Uniqueness is case insensitive
        create_integration_kwargs["RequestParameters"] = {
            "append:header.header_1": "static value",
            "overwrite:header.HEADER_1": "static value",
        }
        with pytest.raises(ClientError) as e:
            apigw_client.create_integration(**create_integration_kwargs)
        snapshot.match("create-duplicate-headers-case-insensitive", e.value.response)

        # An empty mapping will be ignored on create
        create_integration_kwargs["RequestParameters"] = {"append:header.header_1": ""}
        response = apigw_client.create_integration(**create_integration_kwargs)
        snapshot.match("create-with-no-mapping", response)

        # create with all actions
        create_integration_kwargs["RequestParameters"] = {
            "append:header.header_append": "static value",
            "overwrite:header.header_overwrite": "$request.header.foo",
            "remove:header.header_remove": "''",
        }
        integration = apigw_client.create_integration(**create_integration_kwargs)
        snapshot.match("create-with-all-actions", integration)

        # passing the same header with an empty string will delete request parameter
        update_integration_kwargs = {
            "ApiId": api_id,
            "IntegrationId": integration["IntegrationId"],
            "RequestParameters": {
                "remove:header.header_remove": "",
            },
        }
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-delete-parameter-mapping", response)

        # A remove header must have single quotes
        update_integration_kwargs["RequestParameters"] = {"remove:header.header_remove": '""'}
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("remove-needs-single-quotes", e.value.response)

        # Sending a parameter that exists with the same action but different casing will fail
        update_integration_kwargs["RequestParameters"] = {
            "append:header.header_appenD": "static value"
        }
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-with-different-casing", e.value.response)

        # Sending a parameter with the same casing but different action will fail
        update_integration_kwargs["RequestParameters"] = {
            "overwrite:header.header_append": "static value"
        }
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-with-different-action-will-fail", e.value.response)

        # Sending with same casing and same action create_integration()replace
        update_integration_kwargs["RequestParameters"] = {
            "append:header.header_append": "${request.header.foo}"
        }
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-with-same-casing-and-action", response)

        # Missing param_name
        update_integration_kwargs["RequestParameters"] = {"append:header": "static value"}
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("missing-param-name", e.value.response)

        # sending multi headers
        update_integration_kwargs["RequestParameters"] = {
            "append:header.multi_header.1": "$request.header.foo",
            "append:header.multi_header.2": "static value",
            "overwrite:header.multi_header.3": "static value",
            "remove:header.multi_header.4": "''",
        }
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-with-multivalue", response)

        # sending complex value
        update_integration_kwargs["RequestParameters"] = {
            "append:header.append_header": "${request.body}followed with text$request.path",
        }
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-with-multiple-param", response)

        # missing closing curly braces
        update_integration_kwargs["RequestParameters"] = {
            "append:header.append_header": "${request.body",
        }
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-missing-curly", e.value.response)

        # update with extra closing curly
        update_integration_kwargs["RequestParameters"] = {
            "append:header.append_header": "$request.body}",
        }
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-extra-curly", e.value.response)

        # destinations are case-insensitive
        update_integration_kwargs["RequestParameters"] = {
            "append:HEADER.DestinatioN": "But they will be useless",
        }
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-case-sensitive", response)

        # Multiple errors
        update_integration_kwargs["RequestParameters"] = {
            "append:header.first": "valid",
            "append:header.First": "$invalid",
        }
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("multiple-errors", e.value.response)

        # Reserved header
        update_integration_kwargs["RequestParameters"] = {"append:header.authorization": "illegal"}
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("reserved-header", e.value.response)

        # Reserved header prefix
        update_integration_kwargs["RequestParameters"] = {
            "append:header.apigw-any-suffix": "illegal"
        }
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("reserved-header-prefix", e.value.response)

        # Reserved header multiple errors
        update_integration_kwargs["RequestParameters"] = {"append:header.authorization": "$illegal"}
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("reserved-header-multiple-errors", e.value.response)

        # A second $ in the value will start a new source
        update_integration_kwargs["RequestParameters"] = {"append:header.foo": "$request.path$"}
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("with-static-sign", response)

        # A source with $ with length 2 or less will become a static value
        update_integration_kwargs["RequestParameters"] = {"append:header.foo": "$a"}
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("with-sign-become-static", response)

        # A source with $ with length more than 2 will need to be valid
        update_integration_kwargs["RequestParameters"] = {"append:header.foo": "$aa"}
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("sign-with-length-over-2", e.value.response)

        # any { in static value will fail
        update_integration_kwargs["RequestParameters"] = {"append:header.foo": "{"}
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("open-curly", e.value.response)

        # any } in static value will fail
        update_integration_kwargs["RequestParameters"] = {"append:header.foo": "}"}
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("close-curly", e.value.response)

        # any { in dynamic will fail
        update_integration_kwargs["RequestParameters"] = {
            "append:header.foo": "$request.header.foo{"
        }
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("open-curly-in-dynamic", e.value.response)

        # any } in dynamic value will fail
        update_integration_kwargs["RequestParameters"] = {
            "append:header.foo": "$request.header.foo}"
        }
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("close-curly-in-dynamic", e.value.response)

        # A { inside a ${} block is ok
        update_integration_kwargs["RequestParameters"] = {
            "append:header.foo": "${request.header.foo{}"
        }
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("open-curly-in-block", response)

        # any } in ${} value will fail as it will be seen as a `}` static value
        update_integration_kwargs["RequestParameters"] = {
            "append:header.foo": "${request.header.foo}}"
        }
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("close-curly-in-block", e.value.response)

        # A $ at the end of a block isn't matched as there are no valid char after it
        update_integration_kwargs["RequestParameters"] = {
            "append:header.foo": "${request.header.foo$request.header.foo$}"
        }
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("greedy-block-match", response)

        # parameter name must match regex
        update_integration_kwargs["RequestParameters"] = {"append:header.foo%": ""}
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("illegal-char-in-param-name", e.value.response)

    @pytest.mark.skipif(
        not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in legacy"
    )
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            # AWS adds an extra `.`
            "$.append-not-allowed..Message",
            "$.remove-not-allowed..Message",
        ]
    )
    @markers.aws.validated
    def test_request_parameters_path(self, create_v2_api, aws_client, snapshot):
        apigw_client = aws_client.apigatewayv2

        snapshot.add_transformers_list([snapshot.transform.key_value("IntegrationId")])

        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]

        create_integration_kwargs = {
            "ApiId": api_id,
            "IntegrationType": "HTTP_PROXY",
            "IntegrationUri": "https://example.com",
            "IntegrationMethod": "GET",
            "PayloadFormatVersion": "1.0",
            "RequestParameters": {"overwrite:path": "$request.header.foo"},
        }
        integration = apigw_client.create_integration(**create_integration_kwargs)
        snapshot.match("create-with-path-override", integration)

        update_integration_kwargs = {
            "ApiId": api_id,
            "IntegrationId": integration["IntegrationId"],
            "RequestParameters": {
                "overwrite:path": "",
            },
        }

        # removing path parameter
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("remove-with-path-override", response)

        # path is case-insensitive
        update_integration_kwargs["RequestParameters"] = {
            "overwrite:Path": "$request.header.foo",
        }
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-case-sensitive", response)

        # append not allowed
        update_integration_kwargs["RequestParameters"] = {
            "append:path": "$request.header.foo",
        }
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("append-not-allowed", e.value.response)

        # remove not allowed
        update_integration_kwargs["RequestParameters"] = {"remove:path": "''"}
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("remove-not-allowed", e.value.response)

    @pytest.mark.skipif(
        not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in legacy"
    )
    @markers.aws.validated
    def test_response_parameters(self, create_v2_api, aws_client, snapshot):
        apigw_client = aws_client.apigatewayv2

        snapshot.add_transformers_list([snapshot.transform.key_value("IntegrationId")])

        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]

        create_integration_kwargs = {
            "ApiId": api_id,
            "IntegrationType": "HTTP_PROXY",
            "IntegrationUri": "https://example.com",
            "IntegrationMethod": "GET",
            "PayloadFormatVersion": "1.0",
            "ResponseParameters": {"200": {"overwrite:header.header": "$response.header.foo"}},
        }

        integration = apigw_client.create_integration(**create_integration_kwargs)
        snapshot.match("create-with-header-override", integration)

        # remove parameter mapping with empty block
        update_integration_kwargs = {
            "ApiId": api_id,
            "IntegrationId": integration["IntegrationId"],
            "ResponseParameters": {"200": {}},
        }
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-remove-integration-response", response)

        # response under 200
        update_integration_kwargs["ResponseParameters"] = {
            "199": {"overwrite:header.header": "$response.header.foo"}
        }
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("response-under-200", e.value.response)

        # response over 599
        update_integration_kwargs["ResponseParameters"] = {
            "600": {"overwrite:header.header": "$response.header.foo"}
        }
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("response-over-599", e.value.response)

        # response not int
        update_integration_kwargs["ResponseParameters"] = {
            "200 ": {"overwrite:header.header": "$response.header.foo"}
        }
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("response-not-int", e.value.response)

    @pytest.mark.skipif(
        not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in legacy"
    )
    @markers.aws.validated
    def test_response_parameters_statuscode(self, create_v2_api, aws_client, snapshot):
        apigw_client = aws_client.apigatewayv2

        snapshot.add_transformers_list([snapshot.transform.key_value("IntegrationId")])

        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]

        create_integration_kwargs = {
            "ApiId": api_id,
            "IntegrationType": "HTTP_PROXY",
            "IntegrationUri": "https://example.com",
            "IntegrationMethod": "GET",
            "PayloadFormatVersion": "1.0",
            "ResponseParameters": {"200": {"overwrite:statuscode": "$response.header.foo"}},
        }

        integration = apigw_client.create_integration(**create_integration_kwargs)
        snapshot.match("create-with-statuscode-override", integration)

        # update with invalid mapping
        update_integration_kwargs = {
            "ApiId": api_id,
            "IntegrationId": integration["IntegrationId"],
            "ResponseParameters": {"200": {"overwrite:statuscode": "$resp.header.foo"}},
        }
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("invalid-mapping", e.value.response)

        # update with static source
        update_integration_kwargs["ResponseParameters"] = {"200": {"overwrite:statuscode": "201"}}
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-static-code", response)

        # update with static under 100
        update_integration_kwargs["ResponseParameters"] = {"200": {"overwrite:statuscode": "99"}}
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-static-below-100", e.value.response)

        # update with static 600 and above
        update_integration_kwargs["ResponseParameters"] = {"200": {"overwrite:statuscode": "600"}}
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-static-above-600", e.value.response)

        # update with static source non int
        update_integration_kwargs["ResponseParameters"] = {"200": {"overwrite:statuscode": "20.1"}}
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-static-code-non-int", e.value.response)

        # when a response is empty, it gets removed from the integration
        update_integration_kwargs["ResponseParameters"] = {"200": {"overwrite:statuscode": ""}}
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-with-empty-will-remove", response)

        # update with append
        update_integration_kwargs["ResponseParameters"] = {"200": {"append:statuscode": "201"}}
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-with-append", e.value.response)

        # If multiple configuration are passed, all must be valid
        update_integration_kwargs["ResponseParameters"] = {
            "200": {"overwrite:statuscode": "201"},
            "201": {"append:statuscode": "201"},
        }
        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-not-all-valid", e.value.response)
        response = apigw_client.get_integration(
            ApiId=api_id, IntegrationId=integration["IntegrationId"]
        )
        snapshot.match("get-integration-after-invalid-update", response)

    @markers.aws.validated
    def test_http_integration_invalid_use_cases(self, aws_client, create_v2_api, snapshot):
        """
        This is just a bunch of negative tests to our HTTP integration.
        """
        result = create_v2_api(ProtocolType="HTTP", Name=f"{short_uid()}")
        api_id = result["ApiId"]

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.create_integration(
                ApiId=api_id,
                IntegrationType="HTTP_PROXY",
                IntegrationMethod="ANY",
                IntegrationUri="http://example.com",
            )
        snapshot.match("invalid-integration-req-no-payload", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.create_integration(
                ApiId=api_id,
                IntegrationType="HTTP",  # HTTP v2 only supports HTTP_PROXY or AWS_PROXY
                PayloadFormatVersion="1.0",
                IntegrationMethod="ANY",
                IntegrationUri="http://example.com",
            )
        snapshot.match("invalid-integration-type", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.create_integration(
                ApiId=api_id,
                IntegrationType="HTTP_PROXY",
                PayloadFormatVersion="2.0",  # HTTP v2 only supports 1.0
                IntegrationMethod="ANY",
                IntegrationUri="http://example.com",
            )
        snapshot.match("invalid-payload-format-version", e.value.response)

    @pytest.mark.skipif(
        not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in Legacy"
    )
    @markers.aws.validated
    def test_aws_proxy_request_parameters(
        self, aws_client, create_v2_api, snapshot, region_name, create_iam_role_and_attach_policy
    ):
        apigw_client = aws_client.apigatewayv2

        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("IntegrationId"),
                snapshot.transform.key_value("role-arn"),
            ]
        )

        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]

        role_arn = create_iam_role_and_attach_policy(
            policy_arn=f"arn:{get_partition(region_name)}:iam::aws:policy/AmazonKinesisFullAccess",
        )
        snapshot.match("role-arn", role_arn)

        def _remove_required_keys_from_error_message(e):
            message: str = e.value.response["Message"]
            for key in ["StreamName", "Data", "PartitionKey"]:
                assert key in message
                message = message.replace(key, "")
            e.value.response["Message"] = message
            e.value.response["Error"]["Message"] = message
            return e

        with pytest.raises(ClientError) as e:
            apigw_client.create_integration(
                ApiId=api_id,
                IntegrationType="AWS_PROXY",
                IntegrationSubtype="Kinesis-PutRecord",
                PayloadFormatVersion="1.0",
                CredentialsArn=role_arn,
            )
        e = _remove_required_keys_from_error_message(e)
        snapshot.match("missing-required-parameters", e.value.response)

        with pytest.raises(ClientError) as e:
            apigw_client.create_integration(
                ApiId=api_id,
                IntegrationType="AWS_PROXY",
                IntegrationSubtype="Kinesis-PutRecord",
                PayloadFormatVersion="1.0",
                CredentialsArn=role_arn,
                RequestParameters={
                    "streamname": "$request.header.StreamName",
                    "data": "$request.header.Data",
                    "partitionkey": "$request.header.PartitionKey",
                },
            )
        snapshot.match("wrong-casing", e.value.response)

        with pytest.raises(ClientError) as e:
            apigw_client.create_integration(
                ApiId=api_id,
                IntegrationType="AWS_PROXY",
                IntegrationSubtype="Kinesis-PutRecord",
                PayloadFormatVersion="1.0",
                CredentialsArn=role_arn,
                RequestParameters={
                    "StreamName": "$request.header.StreamName",
                    "Data": "$request.header.Data",
                    "PartitionKey": "$request.header.PartitionKey",
                    "InvalidParameter": "$request.header.InvalidParameter",
                },
            )
        snapshot.match("extra-invalid-parameter", e.value.response)

        integration = apigw_client.create_integration(
            ApiId=api_id,
            IntegrationType="AWS_PROXY",
            IntegrationSubtype="Kinesis-PutRecord",
            PayloadFormatVersion="1.0",
            CredentialsArn=role_arn,
            RequestParameters={
                "StreamName": "$request.header.StreamName",
                "Data": "$request.header.Data",
                "PartitionKey": "$request.header.PartitionKey",
                "SequenceNumberForOrdering": "$request.header.SequenceNumberForOrdering",
            },
        )
        snapshot.match("create-with-optional-parameter", integration)
        integration_id = integration["IntegrationId"]

        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(
                ApiId=api_id,
                IntegrationId=integration_id,
                IntegrationType="AWS_PROXY",
                IntegrationSubtype="Kinesis-PutRecord",
                RequestParameters={
                    "StreamName": "$request.querystring.StreamName",
                },
            )
        e = _remove_required_keys_from_error_message(e)
        snapshot.match("update-single-parameter", e.value.response)

        integration = apigw_client.update_integration(
            ApiId=api_id,
            IntegrationId=integration_id,
            IntegrationType="AWS_PROXY",
            IntegrationSubtype="Kinesis-PutRecord",
            RequestParameters={
                "StreamName": "$request.querystring.StreamName",
                "Data": "$request.querystring.Data",
                "PartitionKey": "$request.querystring.PartitionKey",
            },
        )
        snapshot.match("update-with-required-parameter", integration)

        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(
                ApiId=api_id,
                IntegrationId=integration_id,
                IntegrationType="AWS_PROXY",
                IntegrationSubtype="Kinesis-PutRecord",
            )
        e = _remove_required_keys_from_error_message(e)
        snapshot.match("update-with-no-parameters", e.value.response)

        with pytest.raises(ClientError) as e:
            apigw_client.update_integration(
                ApiId=api_id,
                IntegrationId=integration_id,
                IntegrationType="AWS_PROXY",
                IntegrationSubtype="Kinesis-PutRecord",
                RequestParameters={
                    "StreamName": "$request.querystring.StreamName",
                    "Data": "$request.querystring.Data",
                    "PartitionKey": "",
                },
            )
        snapshot.match("update-with-required-parameter-blank", e.value.response)

    @pytest.mark.skipif(
        not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in Legacy"
    )
    @markers.aws.validated
    def test_aws_proxy_subtypes_validation(
        self, aws_client, create_v2_api, snapshot, region_name, create_iam_role_and_attach_policy
    ):
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("IntegrationId"),
                snapshot.transform.resource_name(),
            ]
        )
        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]

        role_arn = create_iam_role_and_attach_policy(
            policy_arn=f"arn:{get_partition(region_name)}:iam::aws:policy/AmazonKinesisFullAccess",
        )

        default_parameters = {
            "StreamName": "$request.header.StreamName",
            "Data": "$request.header.Data",
            "PartitionKey": "$request.header.PartitionKey",
        }

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.create_integration(
                ApiId=api_id,
                IntegrationType="AWS_PROXY",
                IntegrationSubtype="Kinesis-PutRecord",
                PayloadFormatVersion="1.0",
                RequestParameters=default_parameters,
            )
        snapshot.match("missing-credentials-arn", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.create_integration(
                ApiId=api_id,
                IntegrationType="AWS_PROXY",
                IntegrationSubtype="Kinesis-PutRecordInvalid",
                PayloadFormatVersion="1.0",
                RequestParameters=default_parameters,
                CredentialsArn=role_arn,
            )
        snapshot.match("invalid-subtype", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.create_integration(
                ApiId=api_id,
                IntegrationType="HTTP_PROXY",
                IntegrationSubtype="Kinesis-PutRecord",
                PayloadFormatVersion="1.0",
                RequestParameters=default_parameters,
                CredentialsArn=role_arn,
            )
        snapshot.match("invalid-integration-type", e.value.response)

        # create valid one to test UpdateIntegration
        integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="AWS_PROXY",
            IntegrationSubtype="Kinesis-PutRecord",
            PayloadFormatVersion="1.0",
            CredentialsArn=role_arn,
            RequestParameters={
                "StreamName": "$request.header.StreamName",
                "Data": "$request.header.Data",
                "PartitionKey": "$request.header.PartitionKey",
            },
        )
        snapshot.match("create-integration", integration)
        integration_id = integration["IntegrationId"]

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.update_integration(
                ApiId=api_id,
                IntegrationId=integration_id,
                IntegrationType="HTTP_PROXY",
                IntegrationSubtype="Kinesis-PutRecord",
                RequestParameters=default_parameters,
            )
        snapshot.match("update-wrong-integration-type", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.update_integration(
                ApiId=api_id,
                IntegrationId=integration_id,
                IntegrationType="AWS_PROXY",
                IntegrationSubtype="Kinesis-PutRecordInvalid",
                RequestParameters=default_parameters,
            )
        snapshot.match("update-wrong-integration-subtype", e.value.response)


class TestApigatewayV2QuickCreate:
    @pytest.mark.parametrize("integration_type", ["AWS_PROXY", "HTTP_PROXY"])
    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        condition=lambda: not is_next_gen_api(),
        paths=[
            "$..ApiKeySelectionExpression",
            "$..CreatedDate",
            "$..DisableExecuteApiEndpoint",
            "$..RouteSelectionExpression",
            "$.get-api.Tags",
            "$.get-routes.Items..ApiGatewayManaged",
            "$.get-routes.Items..ApiKeyRequired",
            "$.get-routes.Items..AuthorizationType",
            "$.get-routes.Items..Target",
            "$.get-integrations.Items..ApiGatewayManaged",
            "$.get-integrations.Items..ConnectionType",
            "$.get-integrations.Items..IntegrationMethod",
            "$.get-integrations.Items..PayloadFormatVersion",
            "$.get-integrations.Items..TimeoutInMillis",
        ],
    )
    def test_apigatewayv2_quick_create_default(
        self,
        create_v2_api,
        create_lambda_function,
        aws_client,
        snapshot,
        integration_type,
    ):
        snapshot.add_transformers_list(
            [
                snapshot.transform.resource_name(),
                snapshot.transform.key_value("ApiId"),
                snapshot.transform.key_value("IntegrationId"),
                snapshot.transform.key_value("RouteId"),
            ]
        )
        snapshot.add_transformer(snapshot.transform.key_value("ApiEndpoint"), priority=-2)
        if integration_type == "AWS_PROXY":
            lambda_name = f"quick-create-{short_uid()}"
            result = create_lambda_function(
                handler_file=LAMBDA_HELLO,
                func_name=lambda_name,
                runtime=Runtime.python3_12,
            )
            integration_uri = result["CreateFunctionResponse"]["FunctionArn"]
        else:
            # AWS auto-detect the integration type based on the URI, Lambda ARN vs fully qualified URL
            integration_uri = "https://example.com"

        create_api = create_v2_api(
            ProtocolType="HTTP",
            Name="test-quick-create",
            Target=integration_uri,
        )
        snapshot.match("create-api", create_api)
        api_id = create_api["ApiId"]

        get_api = aws_client.apigatewayv2.get_api(ApiId=api_id)
        snapshot.match("get-api", get_api)

        get_integrations = aws_client.apigatewayv2.get_integrations(ApiId=api_id)
        snapshot.match("get-integrations", get_integrations)

        get_routes = aws_client.apigatewayv2.get_routes(ApiId=api_id)
        snapshot.match("get-routes", get_routes)


class TestApigatewayV2HttpRouteCrud:
    @pytest.mark.skipif(
        not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in legacy"
    )
    @markers.aws.validated
    def test_route_with_authorizer_none(self, create_v2_api, aws_client, snapshot):
        snapshot.add_transformer(snapshot.transform.key_value("RouteId"))

        apigw_client = aws_client.apigatewayv2

        result = create_v2_api(ProtocolType="HTTP", Name=f"{short_uid()}")
        api_id = result["ApiId"]

        route = apigw_client.create_route(ApiId=api_id, RouteKey="ANY /no-authorizer")
        snapshot.match("no-authorizer", route)

        route = apigw_client.create_route(
            ApiId=api_id, RouteKey="ANY /none-authorizer", AuthorizationType="NONE"
        )
        snapshot.match("none-authorizer", route)

        route = apigw_client.create_route(
            ApiId=api_id, RouteKey="ANY /invalid-type", AuthorizationType="invalid"
        )
        snapshot.match("invalid-type", route)

        route = apigw_client.create_route(
            ApiId=api_id,
            RouteKey="ANY /none-with-id",
            AuthorizationType="NONE",
            AuthorizerId="randomId",
        )
        snapshot.match("none-with-id", route)

        with pytest.raises(ClientError) as e:
            apigw_client.create_route(
                ApiId=api_id, RouteKey="ANY /with-scopes", AuthorizationScopes=["email"]
            )
        snapshot.match("with-scopes", e.value.response)

        with pytest.raises(ClientError) as e:
            apigw_client.update_route(
                ApiId=api_id, RouteId=route["RouteId"], AuthorizerId="randomId"
            )
        snapshot.match("update-with-only-id", e.value.response)

        with pytest.raises(ClientError) as e:
            apigw_client.update_route(
                ApiId=api_id, RouteId=route["RouteId"], AuthorizationScopes=["email"]
            )
        snapshot.match("update-with-only-scopes", e.value.response)

        update_to_none = apigw_client.update_route(
            ApiId=api_id, RouteId=route["RouteId"], OperationName="test"
        )
        snapshot.match("update-something-else-than-auth", update_to_none)

    @pytest.mark.skipif(
        not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in legacy"
    )
    @markers.aws.validated
    def test_route_with_authorizer_iam(self, create_v2_api, aws_client, snapshot):
        snapshot.add_transformer(snapshot.transform.key_value("RouteId"))

        apigw_client = aws_client.apigatewayv2

        result = create_v2_api(ProtocolType="HTTP", Name=f"{short_uid()}")
        api_id = result["ApiId"]

        route = apigw_client.create_route(
            ApiId=api_id, RouteKey="ANY /iam-authorizer", AuthorizationType="AWS_IAM"
        )
        snapshot.match("iam-authorizer", route)

        route = apigw_client.create_route(
            ApiId=api_id,
            RouteKey="ANY /iam-authorizer-with-id",
            AuthorizationType="AWS_IAM",
            AuthorizerId="randomId",
        )
        snapshot.match("iam-authorizer-with-id", route)

        with pytest.raises(ClientError) as e:
            apigw_client.create_route(
                ApiId=api_id,
                RouteKey="ANY /iam-authorizer-with-scopes",
                AuthorizationType="AWS_IAM",
                AuthorizationScopes=["email"],
            )
        snapshot.match("iam-authorizer-with-scopes", e.value.response)

        route = apigw_client.update_route(
            ApiId=api_id, RouteId=route["RouteId"], AuthorizationType="NONE"
        )
        snapshot.match("iam-authorizer-removed-with-none", route)

    @pytest.mark.skipif(
        not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in legacy"
    )
    @markers.aws.validated
    def test_route_with_authorizer_lambda(
        self, create_v2_api, aws_client, snapshot, create_lambda_authorizer
    ):
        snapshot.add_transformers_list(
            [snapshot.transform.key_value("RouteId"), snapshot.transform.key_value("AuthorizerId")]
        )

        apigw_client = aws_client.apigatewayv2

        result = create_v2_api(ProtocolType="HTTP", Name=f"{short_uid()}")
        api_id = result["ApiId"]

        _, lambda_authorizer_uri = create_lambda_authorizer(LAMBDA_AUTHORIZER_V2_SIMPLE_RESPONSE)
        authorizer_id = apigw_client.create_authorizer(
            ApiId=api_id,
            AuthorizerType="REQUEST",
            IdentitySource=["$request.header.Authorization"],
            Name=f"lambda-authorizer-{short_uid()}",
            AuthorizerUri=lambda_authorizer_uri,
            AuthorizerPayloadFormatVersion="2.0",
            EnableSimpleResponses=True,
        )["AuthorizerId"]

        route = apigw_client.create_route(
            ApiId=api_id,
            RouteKey="ANY /lambda-authorizer",
            AuthorizationType="CUSTOM",
            AuthorizerId=authorizer_id,
        )
        snapshot.match("lambda-authorizer", route)

        with pytest.raises(ClientError) as e:
            apigw_client.create_route(
                ApiId=api_id,
                RouteKey="ANY /lambda-authorizer-invalid-id",
                AuthorizationType="CUSTOM",
                AuthorizerId="randomId",
            )
        snapshot.match("lambda-authorizer-invalid-id", e.value.response)

        with pytest.raises(ClientError) as e:
            apigw_client.create_route(
                ApiId=api_id,
                RouteKey="ANY /lambda-authorizer-with-scopes",
                AuthorizationType="CUSTOM",
                AuthorizerId=authorizer_id,
                AuthorizationScopes=["email"],
            )
        snapshot.match("lambda-authorizer-with-scopes", e.value.response)

        with pytest.raises(ClientError) as e:
            apigw_client.update_route(
                ApiId=api_id, RouteId=route["RouteId"], AuthorizerId=authorizer_id
            )
        snapshot.match("lambda-authorizer-update-with-only-id", e.value.response)

        route = apigw_client.update_route(
            ApiId=api_id, RouteId=route["RouteId"], AuthorizationType="NONE"
        )
        snapshot.match("none-authorizer", route)

        # TODO add test to validate default if no payload version is provided

    @pytest.mark.skipif(
        not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in legacy"
    )
    @markers.aws.validated
    def test_route_with_authorizer_jwt(
        self, create_v2_api, aws_client, snapshot, create_user_pool_client, region_name
    ):
        snapshot.add_transformers_list(
            [snapshot.transform.key_value("RouteId"), snapshot.transform.key_value("AuthorizerId")]
        )

        apigw_client = aws_client.apigatewayv2

        result = create_v2_api(ProtocolType="HTTP", Name=f"{short_uid()}")
        api_id = result["ApiId"]

        user_pool_result = create_user_pool_client(
            client_kwargs={
                "AllowedOAuthScopes": ["email", "openid"],
                "AllowedOAuthFlows": ["code", "implicit"],
                "SupportedIdentityProviders": ["COGNITO"],
                "CallbackURLs": ["https://example.com"],
                "AllowedOAuthFlowsUserPoolClient": True,
            },
        )
        user_pool = user_pool_result.user_pool
        app_client = user_pool_result.pool_client

        cognito_pool_id = user_pool["Id"]
        app_client_id = app_client["ClientId"]

        issuer_url = (
            f"https://cognito-idp.{region_name}.amazonaws.com/{cognito_pool_id}"
            if is_aws_cloud()
            else get_issuer_url(pool_id=cognito_pool_id)
        )
        cognito_authorizer = apigw_client.create_authorizer(
            ApiId=api_id,
            Name=f"cognito-authorizer-{short_uid()}",
            AuthorizerType="JWT",
            IdentitySource=["$request.header.Authorization"],
            JwtConfiguration={
                "Audience": [app_client_id],
                "Issuer": issuer_url,
            },
        )
        authorizer_id = cognito_authorizer["AuthorizerId"]

        route = apigw_client.create_route(
            ApiId=api_id,
            RouteKey="ANY /jwt-authorizer",
            AuthorizationType="JWT",
            AuthorizerId=authorizer_id,
        )
        snapshot.match("jwt-authorizer", route)

        with pytest.raises(ClientError) as e:
            apigw_client.create_route(
                ApiId=api_id,
                RouteKey="ANY /jwt-authorizer-invalid-id",
                AuthorizationType="JWT",
                AuthorizerId="invalidId",
            )
        snapshot.match("jwt-authorizer-invalid-id", e.value.response)

        route = apigw_client.create_route(
            ApiId=api_id,
            RouteKey="ANY /jwt-authorizer-with-scopes",
            AuthorizationType="JWT",
            AuthorizerId=authorizer_id,
            AuthorizationScopes=["email"],
        )
        snapshot.match("jwt-authorizer-with-scopes", route)

        # Test update a route that has scope with no scope (the previously defined scope will remain)
        route = apigw_client.update_route(
            ApiId=api_id,
            RouteId=route["RouteId"],
            AuthorizationType="JWT",
            AuthorizerId=authorizer_id,
        )
        snapshot.match("jwt-authorizer-update-no-scopes", route)

        # Test update a route with empty scope to remove it
        route = apigw_client.update_route(
            ApiId=api_id,
            RouteId=route["RouteId"],
            AuthorizationType="JWT",
            AuthorizerId=authorizer_id,
            AuthorizationScopes=[],
        )
        snapshot.match("jwt-authorizer-remove-scopes", route)

        # Test update scopes only
        route = apigw_client.update_route(
            ApiId=api_id,
            RouteId=route["RouteId"],
            AuthorizationScopes=["email"],
        )
        snapshot.match("jwt-authorizer-scopes-only", route)

        # Test replace existing scopes
        route = apigw_client.update_route(
            ApiId=api_id,
            RouteId=route["RouteId"],
            AuthorizationScopes=["openid"],
        )
        snapshot.match("jwt-authorizer-replace-scopes", route)

        route = apigw_client.update_route(
            ApiId=api_id, RouteId=route["RouteId"], AuthorizationType="NONE", AuthorizationScopes=[]
        )
        snapshot.match("none-authorizer", route)
