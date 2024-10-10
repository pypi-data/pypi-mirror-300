import json
import time
from operator import itemgetter

import pytest
import requests
from botocore.exceptions import ClientError
from localstack import config
from localstack.constants import LOCALHOST_HOSTNAME
from localstack.testing.aws.util import is_aws_cloud
from localstack.testing.pytest import markers
from localstack.utils import testutil
from localstack.utils.aws import arns
from localstack.utils.strings import short_uid
from localstack.utils.urls import localstack_host

from tests.aws.services.apigateway.apigateway_fixtures import UrlType, api_invoke_url
from tests.aws.services.apigateway.conftest import LAMBDA_REQUEST_AUTH, is_next_gen_api


class TestApigatewayCustomDomain:
    # This test uses hard coded values for host pointing to localstack
    # And does not properly clean its resources
    @markers.aws.needs_fixing
    def test_invoke_custom_domain(
        self, create_lambda_function, create_rest_apigw, aws_client, region_name
    ):
        api_name = f"api-{short_uid()}"
        api_id, _, root_resource_eu_id = create_rest_apigw(name=api_name)

        # endpoints: (domain, method, base path, resource path, stage)
        endpoints = [
            {
                "domain": "foo",
                "method": "GET",
                "base_path": "base1",
                "resource_path": "/res1",
                "stage": "stage1",
            },
            {
                "domain": "bar",
                "method": "POST",
                "base_path": "my/base2",
                "resource_path": "/res2",
                "stage": "stage2",
            },
        ]

        # create lambda authorizer
        lambda_name = f"auth-{short_uid()}"
        lambda_code = LAMBDA_REQUEST_AUTH % "1.0"
        zip_file = testutil.create_lambda_archive(lambda_code, get_content=True)
        lambda_arn = create_lambda_function(func_name=lambda_name, zip_file=zip_file)[
            "CreateFunctionResponse"
        ]["FunctionArn"]

        auth_url = arns.apigateway_invocations_arn(lambda_arn, region_name)
        authorizer_id = aws_client.apigateway.create_authorizer(
            restApiId=api_id,
            name=f"auth-{short_uid()}",
            type="REQUEST",
            identitySource="method.request.header.X-User",
            authorizerUri=auth_url,
        )["id"]
        # create resources, methods, integrations
        for endpoint in endpoints:
            res_id = aws_client.apigateway.create_resource(
                restApiId=api_id,
                parentId=root_resource_eu_id,
                pathPart=endpoint["resource_path"].strip("/"),
            )["id"]
            aws_client.apigateway.put_method(
                restApiId=api_id,
                resourceId=res_id,
                httpMethod=endpoint["method"],
                authorizationType="CUSTOM",
                authorizerId=authorizer_id,
            )
            aws_client.apigateway.put_method_response(
                restApiId=api_id,
                resourceId=res_id,
                httpMethod=endpoint["method"],
                statusCode="200",
            )
            aws_client.apigateway.put_integration(
                restApiId=api_id,
                resourceId=res_id,
                httpMethod=endpoint["method"],
                type="MOCK",
                requestTemplates={"application/json": '{"statusCode": 200}'},
            )
            aws_client.apigateway.put_integration_response(
                restApiId=api_id,
                resourceId=res_id,
                httpMethod=endpoint["method"],
                statusCode="200",
                selectionPattern="",
                responseTemplates={
                    "application/json": json.dumps({"statusCode": 200, "message": "OK"})
                },
            )

        depl_id = aws_client.apigateway.create_deployment(restApiId=api_id)["id"]

        for endpoint in endpoints:
            aws_client.apigateway.create_stage(
                restApiId=api_id, stageName=endpoint["stage"], deploymentId=depl_id
            )
            domain_name = f"{endpoint['domain']}.{LOCALHOST_HOSTNAME}"
            aws_client.apigateway.create_domain_name(domainName=domain_name)
            if not is_next_gen_api():
                aws_client.apigateway.create_base_path_mapping(
                    domainName=domain_name,
                    basePath=endpoint["base_path"],
                    restApiId=api_id,
                    stage=endpoint["stage"],
                )
            else:
                aws_client.apigatewayv2.create_api_mapping(
                    DomainName=domain_name,
                    ApiId=api_id,
                    ApiMappingKey=endpoint["base_path"],
                    Stage=endpoint["stage"],
                )
            # TODO: validate this in AWS
            aws_client.apigatewayv2.get_domain_name(DomainName=domain_name)

        # invoke endpoints
        valid_headers = {"X-User": "valid-user"}
        # TODO: remove this when validating the test against AWS again

        not_found_status_code = 403 if is_next_gen_api() else 404
        for endpoint in endpoints:
            domain = endpoint["domain"]  # 0
            method = endpoint["method"]  # 1
            base_path = endpoint["base_path"]  # 2
            resource_path = endpoint["resource_path"]  # 3

            host = f"{domain}.{localstack_host().host}"
            url = f"{config.external_service_url(host=host)}/{base_path}{resource_path}"
            result = requests.request(method=method, url=url, headers=valid_headers)
            assert result.ok

            # invoke with invalid method
            result = requests.request(method="PUT", url=url)
            assert result.status_code == not_found_status_code
            # invoke with invalid base path
            result = requests.request(method=method, url=f"{url}/invalid")
            assert result.status_code == not_found_status_code
            # invoke with invalid resource path
            result = requests.request(
                method="GET", url=url.replace(resource_path, f"{resource_path}-invalid")
            )
            assert result.status_code == not_found_status_code

            # invoke with host header, but against the default URL
            # LocalStack only?
            host_header = {"Host": f"{domain}.{localstack_host().host}"}
            host_header.update(valid_headers)
            # TODO: remove this hardcoded value as we move along with updating testing
            host = f"{api_id}.execute-api.{localstack_host().host}"
            url = f"{config.external_service_url(host=host, protocol='https')}/{base_path}{resource_path}"
            result = requests.request(url=url, method=method, headers=host_header)
            assert result.ok

    @markers.aws.validated
    def test_delete_domain_name_deletes_mapping(
        self, aws_client, create_rest_apigw, apigwv2_create_domain, snapshot
    ):
        snapshot.add_transformer(snapshot.transform.key_value("ApiId", "apiId"))
        snapshot.add_transformer(snapshot.transform.key_value("ApiMappingId", "apiMappingId"))
        api_name = f"api-{short_uid()}"
        api_id, _, root_resource_id = create_rest_apigw(name=api_name)
        domain_name = apigwv2_create_domain()["DomainName"]
        aws_client.apigateway.put_method(
            restApiId=api_id,
            resourceId=root_resource_id,
            httpMethod="GET",
            authorizationType="NONE",
        )
        aws_client.apigateway.put_integration(
            restApiId=api_id, resourceId=root_resource_id, type="MOCK", httpMethod="GET"
        )
        aws_client.apigateway.create_deployment(restApiId=api_id, stageName="test")
        result = aws_client.apigatewayv2.create_api_mapping(
            ApiId=api_id, DomainName=domain_name, ApiMappingKey="v1/orders", Stage="test"
        )
        snapshot.match("api-mapping", result)
        mapping_id = result["ApiMappingId"]

        aws_client.apigatewayv2.delete_domain_name(DomainName=domain_name)
        with pytest.raises(ClientError) as exc:
            aws_client.apigatewayv2.get_api_mapping(ApiMappingId=mapping_id, DomainName=domain_name)
        snapshot.match("get-mapping-error", exc.value.response)

        if not is_aws_cloud():
            from localstack.pro.core.services.apigateway.models import apigatewayv2_stores
            from localstack.pro.core.services.apigateway.router_asf import SHARED_ROUTER

            # make sure we properly clean everything when we delete a domain
            for _, _, store in apigatewayv2_stores.iter_stores():
                if domain_details := store.domain_names.get(domain_name):
                    assert not domain_details.api_mappings.get(mapping_id)

            assert not SHARED_ROUTER.custom_domain_rules.get(domain_name)

    @markers.aws.validated
    @pytest.mark.skipif(
        condition=not is_next_gen_api() and not is_aws_cloud(),
        reason="Behavior not implemented in legacy implementation",
    )
    def test_update_base_path_mappings_apigw_v1(
        self, aws_client, create_rest_apigw, apigwv2_create_domain, snapshot
    ):
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("restApiId"),
                snapshot.transform.key_value("ApiMappingId"),
            ]
        )
        api_name = f"api-1-base-path-{short_uid()}"
        api_name_2 = f"api-2-base-path-{short_uid()}"
        api_id, _, root_resource_id = create_rest_apigw(name=api_name)
        api_id_2, _, root_resource_id_2 = create_rest_apigw(name=api_name_2)
        domain_name = apigwv2_create_domain()["DomainName"]
        stage_name = "test"
        stage_name_2 = "dev"
        base_path = "ordersv1"
        base_path_2 = "ordersv2"
        base_path_3 = "ordersv3"

        for _api_id, _root_resource_id in [
            (api_id, root_resource_id),
            (api_id_2, root_resource_id_2),
        ]:
            aws_client.apigateway.put_method(
                restApiId=_api_id,
                resourceId=_root_resource_id,
                httpMethod="GET",
                authorizationType="NONE",
            )
            aws_client.apigateway.put_integration(
                restApiId=_api_id, resourceId=_root_resource_id, type="MOCK", httpMethod="GET"
            )

            # create 2 deployments, one for each stage
            aws_client.apigateway.create_deployment(restApiId=_api_id, stageName=stage_name)

        if is_aws_cloud():
            # to avoid rate limiting
            time.sleep(10)
        aws_client.apigateway.create_deployment(restApiId=api_id_2, stageName=stage_name_2)

        with pytest.raises(ClientError) as e:
            aws_client.apigateway.create_base_path_mapping(
                domainName=domain_name,
                restApiId=api_id,
                basePath="nested/base/path",
                stage=stage_name,
            )
        snapshot.match("nested-base-path", e.value.response)

        result = aws_client.apigateway.create_base_path_mapping(
            domainName=domain_name,
            restApiId=api_id,
            basePath=base_path,
            stage=stage_name,
        )
        snapshot.match("create-base-path-mapping-api-1", result)

        with pytest.raises(ClientError) as e:
            aws_client.apigateway.create_base_path_mapping(
                domainName=domain_name,
                restApiId=api_id_2,
                basePath=base_path,
                stage=stage_name,
            )
        snapshot.match("create-base-path-mapping-api-2-identical", e.value.response)

        result = aws_client.apigateway.create_base_path_mapping(
            domainName=domain_name,
            restApiId=api_id,
            basePath=base_path_3,
            stage=stage_name,
        )
        snapshot.match("create-base-path-mapping-api-3", result)

        get_mappings = aws_client.apigateway.get_base_path_mappings(domainName=domain_name)
        get_mappings["items"].sort(key=itemgetter("basePath"))
        snapshot.match("get-mappings-before-update", get_mappings)

        get_mappings_v2 = aws_client.apigatewayv2.get_api_mappings(DomainName=domain_name)
        snapshot.match("get-mappings-in-v2", get_mappings_v2)

        # update the base path mapping to target another API
        update_api_id = aws_client.apigateway.update_base_path_mapping(
            domainName=domain_name,
            basePath=base_path,
            patchOperations=[{"op": "replace", "path": "/restapiId", "value": api_id_2}],
        )
        snapshot.match("update-api-id", update_api_id)

        # update the base path mapping to target another stage
        update_stage = aws_client.apigateway.update_base_path_mapping(
            domainName=domain_name,
            basePath=base_path,
            patchOperations=[{"op": "replace", "path": "/stage", "value": stage_name_2}],
        )
        snapshot.match("update-stage", update_stage)

        # update the base path mapping to target a new base path
        update_base_path = aws_client.apigateway.update_base_path_mapping(
            domainName=domain_name,
            basePath=base_path,
            patchOperations=[{"op": "replace", "path": "/basePath", "value": base_path_2}],
        )
        snapshot.match("update-base-path", update_base_path)

        result = aws_client.apigateway.update_base_path_mapping(
            domainName=domain_name,
            basePath=base_path_2,
            patchOperations=[
                {"op": "replace", "path": "/basePath", "value": base_path_3},
            ],
        )
        snapshot.match("overwrite-exists-base-path-mapping", result)

        get_mappings = aws_client.apigateway.get_base_path_mappings(domainName=domain_name)
        snapshot.match("get-mappings", get_mappings)

        # negative testing
        with pytest.raises(ClientError) as e:
            aws_client.apigateway.update_base_path_mapping(
                domainName=domain_name,
                basePath="badpath",
                patchOperations=[
                    {"op": "replace", "path": "/basePath", "value": "v2/orders"},
                ],
            )
        snapshot.match("wrong-base-path", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.apigateway.update_base_path_mapping(
                domainName=domain_name,
                basePath=base_path_3,
                patchOperations=[
                    {"op": "add", "path": "/basePath", "value": "v3/orders"},
                ],
            )
        snapshot.match("wrong-operation", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.apigateway.update_base_path_mapping(
                domainName=domain_name,
                basePath=base_path_3,
                patchOperations=[
                    {"op": "remove", "path": "/basePath", "value": "v3/orders"},
                ],
            )
        snapshot.match("wrong-operation-remove", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.apigateway.update_base_path_mapping(
                domainName=domain_name,
                basePath=base_path_3,
                patchOperations=[
                    {"op": "replace", "path": "/restapiId", "value": "abcdef"},
                ],
            )
        snapshot.match("non-existent-api-replace", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.apigateway.update_base_path_mapping(
                domainName=domain_name,
                basePath=base_path_3,
                patchOperations=[
                    {"op": "replace", "path": "/stage", "value": "wrongstage"},
                ],
            )
        snapshot.match("non-existent-stage-replace", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.apigateway.update_base_path_mapping(
                domainName=domain_name,
                basePath=base_path_3,
                patchOperations=[
                    {"op": "replace", "path": "/restapiid", "value": api_id},
                ],
            )
        snapshot.match("bad-path", e.value.response)

    @markers.aws.only_localstack
    @pytest.mark.skipif(condition=not config.use_custom_dns(), reason="Test requires DNS server")
    def test_custom_domain_dns_resolution(
        self, aws_client, create_rest_apigw, apigwv2_create_domain
    ):
        api_name = f"api-{short_uid()}"
        api_id, _, root_resource_eu_id = create_rest_apigw(name=api_name)
        path = "res"

        res_id = aws_client.apigateway.create_resource(
            restApiId=api_id,
            parentId=root_resource_eu_id,
            pathPart=path,
        )["id"]
        aws_client.apigateway.put_method(
            restApiId=api_id,
            resourceId=res_id,
            httpMethod="GET",
            authorizationType="NONE",
        )
        aws_client.apigateway.put_method_response(
            restApiId=api_id,
            resourceId=res_id,
            httpMethod="GET",
            statusCode="200",
            responseParameters={"method.response.header.Content-Type": False},
            responseModels={"application/json": "Empty"},
        )
        aws_client.apigateway.put_integration(
            restApiId=api_id,
            resourceId=res_id,
            httpMethod="GET",
            type="MOCK",
            requestTemplates={"application/json": '{"statusCode": 200}'},
        )
        aws_client.apigateway.put_integration_response(
            restApiId=api_id,
            resourceId=res_id,
            httpMethod="GET",
            statusCode="200",
            responseTemplates={"application/json": json.dumps({"message": "Hello world"})},
        )

        domain_name = apigwv2_create_domain()["DomainName"]

        depl_id = aws_client.apigateway.create_deployment(restApiId=api_id)["id"]

        stage_name = "prod"
        aws_client.apigateway.create_stage(
            restApiId=api_id, stageName=stage_name, deploymentId=depl_id
        )

        aws_client.apigateway.create_base_path_mapping(
            domainName=domain_name,
            restApiId=api_id,
            stage=stage_name,
        )

        def assert_valid_response(url: str, extra_headers: dict | None = None):
            headers = {"Accept": "application/json"}
            if extra_headers:
                headers.update(**extra_headers)
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            assert response.json() == {"message": "Hello world"}

        # invoke the API via the autogenerated domain
        autogenerated_url = api_invoke_url(
            api_id=api_id, stage="prod", path="/res", url_type=UrlType.HOST_BASED
        )
        assert_valid_response(autogenerated_url)

        # invoke the custom domain name via host header
        default_url = f"http://localhost:4566/{path}"
        assert_valid_response(default_url, extra_headers={"Host": domain_name})

        # invoke the custom domain name via DNS
        url = f"http://{domain_name}:4566/{path}"
        assert_valid_response(url)
