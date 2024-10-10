import os

import pytest
import requests
from botocore.exceptions import ClientError
from localstack.testing.aws.util import is_aws_cloud
from localstack.testing.pytest import markers
from localstack.utils.docker_utils import DOCKER_CLIENT
from localstack.utils.strings import short_uid
from localstack.utils.sync import retry
from localstack.utils.threads import start_worker_thread
from tests.aws.services.apigateway.apigateway_fixtures import api_invoke_url
from tests.aws.services.apigateway.conftest import is_next_gen_api


class TestHttpApiServiceDiscoveryPrivateIntegration:
    @markers.skip_offline
    @markers.aws.only_localstack
    def test_servicediscovery_ecs_integration(
        self, deploy_cfn_template, cleanup_changesets, cleanup_stacks, aws_client
    ):
        # TODO: write a simpler test for ServiceDiscovery integration, that is runnable against AWS
        #  this test spawns a lot of resources that are not used, like a DynamoDB table

        # start pulling Docker image in the background
        start_worker_thread(lambda *args: DOCKER_CLIENT.pull_image("nginx"))
        # deploy API Gateway ECS sample app
        result = deploy_cfn_template(
            template_path=os.path.join(
                os.path.dirname(__file__), "../../templates/apigateway.ecs.servicediscovery.yml"
            )
        )

        # check ECS deployment
        cluster_id = result.outputs["ECSClusterID"]
        task_arns = aws_client.ecs.list_tasks(cluster=cluster_id)["taskArns"]
        tasks = aws_client.ecs.describe_tasks(cluster=cluster_id, tasks=task_arns)["tasks"]
        # assert that host ports are defined for the deployed containers
        for task in tasks:
            assert task["containers"][0]["networkBindings"][0]["hostPort"]

        # check ServiceDiscovery deployment
        service1 = aws_client.servicediscovery.get_service(
            Id=result.outputs["ServiceDiscoveryServiceFoodstoreFoodsID"]
        )
        service2 = aws_client.servicediscovery.get_service(
            Id=result.outputs["ServiceDiscoveryServicePetstorePetsID"]
        )
        instances1 = aws_client.servicediscovery.list_instances(
            ServiceId=service1["Service"]["Id"]
        )["Instances"]
        instances2 = aws_client.servicediscovery.list_instances(
            ServiceId=service2["Service"]["Id"]
        )["Instances"]

        assert len(instances1) == 3
        assert len(instances2) == 3

        # invoke services via API Gateway
        api_id = result.outputs["APIId"]
        base_url = api_invoke_url(api_id=api_id)

        def _invoke():
            response = requests.get(f"{base_url}foodstore/foods/test")
            assert "nginx" in response.text

            response = requests.get(f"{base_url}petstore/pets/test")
            assert "nginx" in response.text

            response = requests.get(f"{base_url}invalid-path")
            assert not response.ok
            assert "nginx" not in response.text
            assert "Not Found" in response.text

        retry(_invoke, retries=15, sleep=1)


class TestApigatewayV2PrivateIntegration:
    @pytest.fixture
    def create_vpc_and_vpc_link(
        self, create_v2_vpc_link, ec2_create_security_group_with_vpc, create_vpc
    ):
        vpc, subnets = create_vpc()
        sg_name = f"apigwv2-sg-{short_uid()}"
        security_group = ec2_create_security_group_with_vpc(
            VpcId=vpc["VpcId"],
            GroupName=sg_name,
            Description="Security group for APIGW V2",
            ports=[80],
        )

        vpc_link = create_v2_vpc_link(
            SubnetIds=subnets,
            SecurityGroupIds=[security_group["GroupId"]],
        )
        return vpc_link

    @pytest.mark.skipif(
        condition=not is_next_gen_api() and not is_aws_cloud(),
        reason="Not properly implemented",
    )
    @markers.aws.validated
    def test_apigatewayv2_servicediscovery_validation(
        self,
        create_v2_api,
        create_vpc_and_vpc_link,
        aws_client,
        snapshot,
        account_id,
        region_name,
    ):
        result = create_v2_api(ProtocolType="HTTP", Name=f"{short_uid()}")
        api_id = result["ApiId"]

        service_discovery_arn = (
            f"arn:aws:servicediscovery:{region_name}:{account_id}:service/srv-id"
        )

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.create_integration(
                ApiId=api_id,
                IntegrationType="HTTP_PROXY",
                PayloadFormatVersion="1.0",
                IntegrationMethod="ANY",
                IntegrationUri=service_discovery_arn,
            )
        snapshot.match("no-conn-with-service-discovery", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.create_integration(
                ApiId=api_id,
                IntegrationType="HTTP_PROXY",
                PayloadFormatVersion="1.0",
                IntegrationMethod="ANY",
                ConnectionType="VPC_LINK",
                IntegrationUri=service_discovery_arn,
            )
        snapshot.match("no-conn-id-with-service-discovery", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.create_integration(
                ApiId=api_id,
                IntegrationType="HTTP_PROXY",
                PayloadFormatVersion="1.0",
                IntegrationMethod="ANY",
                ConnectionType="VPC_LINK",
                ConnectionId=create_vpc_and_vpc_link["VpcLinkId"],
                IntegrationUri=service_discovery_arn,
            )
        snapshot.match("no-conn-id-with-bad-service-discovery", e.value.response)

        # TODO: add tests with a valid ServiceDiscovery ARN, and maybe deletion + invocation after

    @pytest.mark.skipif(
        condition=not is_next_gen_api() and not is_aws_cloud(),
        reason="Not properly implemented",
    )
    @markers.aws.validated
    def test_apigatewayv2_elb_validation(
        self,
        create_v2_api,
        create_vpc_and_vpc_link,
        aws_client,
        snapshot,
        account_id,
        region_name,
    ):
        result = create_v2_api(ProtocolType="HTTP", Name=f"{short_uid()}")
        api_id = result["ApiId"]

        elb_arn = f"arn:aws:elasticloadbalancing:{region_name}:{account_id}:listener/app/my-load-balancer/50dc6c495c0c9188/0467ef3c8400ae65"

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.create_integration(
                ApiId=api_id,
                IntegrationType="HTTP_PROXY",
                PayloadFormatVersion="1.0",
                IntegrationMethod="ANY",
                ConnectionType="VPC_LINK",
                ConnectionId=create_vpc_and_vpc_link["VpcLinkId"],
                IntegrationUri=elb_arn,
            )
        snapshot.match("no-conn-id-with-bad-elb-arn", e.value.response)

        # TODO: add tests with a valid ELB ARN, and maybe deletion + invocation after
