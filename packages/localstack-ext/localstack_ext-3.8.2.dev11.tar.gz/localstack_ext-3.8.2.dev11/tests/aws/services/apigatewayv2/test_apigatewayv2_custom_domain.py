import json
import logging
import time
from operator import itemgetter

import pytest
import requests
from botocore.exceptions import ClientError
from localstack import constants
from localstack.aws.api.lambda_ import Runtime
from localstack.testing.aws.util import is_aws_cloud
from localstack.testing.pytest import markers
from localstack.utils.strings import short_uid
from localstack.utils.sync import retry
from tests.aws.services.apigateway.apigateway_fixtures import api_invoke_url
from tests.aws.services.apigateway.conftest import LAMBDA_ECHO_EVENT, is_next_gen_api
from tests.aws.services.cloudfront.test_cloudfront import get_split_certificate

LOG = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def acm_imported_cert(aws_client):
    private_key, cert, cert_chain = get_split_certificate()
    import_certificate_result = aws_client.acm.import_certificate(
        Certificate=cert, PrivateKey=private_key, CertificateChain=cert_chain
    )
    cert_arn = import_certificate_result["CertificateArn"]
    yield cert_arn

    try:
        retry(aws_client.acm.delete_certificate, retries=10, sleep=3, CertificateArn=cert_arn)
    except Exception as e:
        LOG.debug("error cleaning up certificate %s: %s", cert_arn, e)


@pytest.fixture(scope="class")
def apigwv2_domain_with_imported_cert(aws_client, acm_imported_cert):
    domain_name = f"{short_uid()}.{constants.LOCALHOST_HOSTNAME}"
    response = aws_client.apigatewayv2.create_domain_name(
        DomainName=domain_name,
        DomainNameConfigurations=[
            {
                "CertificateArn": acm_imported_cert,
                "EndpointType": "REGIONAL",
            }
        ],
    )
    yield response

    # cleanup
    try:
        aws_client.apigatewayv2.delete_domain_name(DomainName=domain_name)
    except Exception as e:
        LOG.debug("error cleaning up domain name %s: %s", domain_name, e)


@pytest.fixture
def apigwv2_create_domain_name(aws_client):
    domains = []

    def factory(**kwargs) -> dict:
        response = aws_client.apigatewayv2.create_domain_name(**kwargs)
        domains.append(response["DomainName"])
        return response

    yield factory

    # cleanup
    for domain_name in domains:
        try:
            aws_client.apigatewayv2.delete_domain_name(DomainName=domain_name)
        except aws_client.apigatewayv2.exceptions.NotFoundException:
            pass
        except Exception as e:
            LOG.debug("error cleaning up domain name %s: %s", domain_name, e)


@pytest.fixture
def apigwv2_create_api_mapping(aws_client):
    mappings: list[tuple[str, str]] = []

    def factory(**kwargs) -> dict:
        response = aws_client.apigatewayv2.create_api_mapping(**kwargs)
        mappings.append((response["ApiMappingId"], kwargs["DomainName"]))
        return response

    yield factory

    # cleanup
    for mapping_id, domain_name in mappings:
        try:
            aws_client.apigatewayv2.delete_api_mapping(
                DomainName=domain_name, ApiMappingId=mapping_id
            )

        except aws_client.apigatewayv2.exceptions.NotFoundException:
            pass
        except Exception as e:
            LOG.debug("error cleaning up api mapping %s for %s: %s", mapping_id, domain_name, e)


@pytest.fixture
def apigwv1_create_domain(aws_client):
    domains = []

    def factory(**kwargs) -> dict:
        response = aws_client.apigateway.create_domain_name(**kwargs)
        domains.append(response["domainName"])
        return response

    yield factory

    # cleanup
    for domain_name in domains:
        try:
            aws_client.apigateway.delete_domain_name(domainName=domain_name)
        except aws_client.apigateway.exceptions.NotFoundException:
            pass
        except Exception as e:
            LOG.debug("error cleaning up domain name %s: %s", domain_name, e)


class TestApigatewayV2CustomDomain:
    @markers.snapshot.skip_snapshot_verify(
        condition=lambda: not is_next_gen_api(),
        paths=[
            "$..body",
            "$..headers",
            "$..multiValueHeaders.Connection",
            "$..multiValueHeaders.X-Amzn-Trace-Id",
            "$..multiValueHeaders.X-Forwarded-Port",
            "$..multiValueHeaders.X-Forwarded-Proto",
            "$..multiValueHeaders.x-localstack-edge",
            "$..multiValueQueryStringParameters",
            "$..pathParameters",
            "$..queryStringParameters",
            "$..rawPath",
            "$..requestContext.authorizer",
            "$..requestContext.eventType",
            "$..requestContext.extendedRequestId",
            "$..requestContext.identity",
            "$..requestContext.messageId",
            "$..requestContext.path",
            "$..requestContext.requestId",
            "$..requestContext.resourceId",
            "$..requestContext.resourcePath",
            "$..requestContext.routeKey",
            "$..requestContext.version",
            "$..stageVariables",
            "$..ApiMappingKey",
            "$..HostedZoneId",
            "$.invocation-v2-base-path-dev.requestContext.http.path",
        ],
    )
    @markers.aws.validated
    def test_custom_domains(
        self,
        aws_client,
        create_v2_api,
        create_lambda_function,
        acm_imported_cert,
        apigwv2_create_domain_name,
        apigwv2_create_api_mapping,
        snapshot,
        add_permission_for_integration_lambda,
        add_aws_proxy_snapshot_transformers,
    ):
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("ApiId"),
                snapshot.transform.key_value("ApiMappingId"),
                snapshot.transform.key_value("domainPrefix"),
                snapshot.transform.key_value("ApiGatewayDomainName"),
                snapshot.transform.key_value("HostedZoneId"),
            ]
        )

        result = create_v2_api(ProtocolType="HTTP", Name=f"{short_uid()}")
        api_id = result["ApiId"]

        # if you try to create a domain with a certificate that does not cover the domain name, you get the following
        # exception:
        #  An error occurred (BadRequestException) when calling the CreateDomainName operation: The domain name to be
        #  created is not covered by the provided certificate.
        domain_name = f"{short_uid()}.{constants.LOCALHOST_HOSTNAME}"
        response = apigwv2_create_domain_name(
            DomainName=domain_name,
            DomainNameConfigurations=[
                {
                    "CertificateArn": acm_imported_cert,
                    "EndpointType": "REGIONAL",
                }
            ],
        )

        snapshot.match("create-domain-name", response)

        lambda_name = f"auth-{short_uid()}"
        lambda_arn = create_lambda_function(
            handler_file=LAMBDA_ECHO_EVENT, func_name=lambda_name, runtime=Runtime.nodejs20_x
        )["CreateFunctionResponse"]["FunctionArn"]
        add_permission_for_integration_lambda(api_id, lambda_arn)

        integration_id_v1 = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="AWS_PROXY",
            PayloadFormatVersion="1.0",
            IntegrationMethod="ANY",
            IntegrationUri=lambda_arn,
        )["IntegrationId"]

        integration_id_v2 = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="AWS_PROXY",
            PayloadFormatVersion="2.0",
            IntegrationMethod="ANY",
            IntegrationUri=lambda_arn,
        )["IntegrationId"]

        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="NONE",
            RouteKey="POST /example/v1",
            Target=f"integrations/{integration_id_v1}",
        )
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="NONE",
            RouteKey="POST /example/v2",
            Target=f"integrations/{integration_id_v2}",
        )

        aws_client.apigatewayv2.create_stage(ApiId=api_id, StageName="$default", AutoDeploy=True)
        aws_client.apigatewayv2.create_stage(ApiId=api_id, StageName="dev", AutoDeploy=True)

        # TODO: add validation for setting the stage as (none)
        # TODO: add test for ApiMappingKey as (None)
        base_path_default = "base-path-default-stage"
        base_path_dev = "base-path-dev-stage"

        create_mapping_default_with_key = apigwv2_create_api_mapping(
            ApiId=api_id,
            DomainName=domain_name,
            Stage="$default",
            ApiMappingKey=base_path_default,
        )
        snapshot.match("create-mapping-with-key", create_mapping_default_with_key)

        create_mapping_no_key = apigwv2_create_api_mapping(
            ApiId=api_id,
            DomainName=domain_name,
            Stage="$default",
        )
        snapshot.match("create-mapping-without-key", create_mapping_no_key)

        create_mapping_dev_with_key = apigwv2_create_api_mapping(
            ApiId=api_id,
            DomainName=domain_name,
            Stage="dev",
            ApiMappingKey=base_path_dev,
        )
        snapshot.match("create-mapping-with-key-dev", create_mapping_dev_with_key)

        def _invoke(url: str, expected_status_code: int):
            headers = {
                "Host": domain_name,
                "User-Agent": "requests/test",
            }
            _resp = requests.post(url, headers=headers, verify=False)
            assert _resp.status_code == expected_status_code
            return _resp

        endpoint = api_invoke_url(api_id=api_id, path=f"{base_path_default}/example/v1")
        result = retry(_invoke, url=endpoint, expected_status_code=200)
        snapshot.match("invocation-v1-base-path-default", json.loads(result.content))

        endpoint = api_invoke_url(api_id=api_id, path=f"{base_path_default}/example/v2")
        result = retry(_invoke, url=endpoint, expected_status_code=200)
        snapshot.match("invocation-v2-base-path-default", json.loads(result.content))

        endpoint = api_invoke_url(api_id=api_id, path=f"{base_path_dev}/example/v1")
        result = retry(_invoke, url=endpoint, expected_status_code=200)
        snapshot.match("invocation-v1-base-path-dev", json.loads(result.content))

        endpoint = api_invoke_url(api_id=api_id, path=f"{base_path_dev}/example/v2")
        result = retry(_invoke, url=endpoint, expected_status_code=200)
        snapshot.match("invocation-v2-base-path-dev", json.loads(result.content))

        # check invalid endpoint
        invalid_endpoint = api_invoke_url(api_id=api_id, path="/invalid-mapping-key/example/v1")
        result = retry(_invoke, url=invalid_endpoint, expected_status_code=404)
        if is_aws_cloud() or is_next_gen_api():
            snapshot.match("invocation-response-bad-mapping-key", json.loads(result.content))

        delete_mapping = aws_client.apigatewayv2.delete_api_mapping(
            ApiMappingId=create_mapping_default_with_key["ApiMappingId"], DomainName=domain_name
        )
        snapshot.match("delete-mapping", delete_mapping)

        if not is_aws_cloud():
            from localstack.pro.core.services.apigateway.router_asf import SHARED_ROUTER

            # test that deleting the api mapping also deletes internal router mapping
            assert not SHARED_ROUTER.custom_domain_rules.get(domain_name)

    @markers.aws.only_localstack
    @pytest.mark.parametrize(
        "domain_name",
        [
            "<random>.example.com",
            f"<random>.{constants.LOCALHOST}",
        ],
    )
    def test_custom_domains_outside_of_cert(
        self,
        aws_client,
        create_v2_api,
        create_lambda_function,
        apigwv2_create_domain,
        add_permission_for_integration_lambda,
        domain_name,
    ):
        # In AWS, you cannot use a certificate that does not cover the domain name created. For now LocalStack still
        # allows it, this test is to prevent regression for this, but could be removed in favor of more parity
        used_domain_name = domain_name.replace("<random>", short_uid())
        result = create_v2_api(ProtocolType="HTTP", Name=f"{short_uid()}")
        api_id = result["ApiId"]

        apigwv2_create_domain(DomainName=used_domain_name)

        lambda_name = f"auth-{short_uid()}"
        lambda_arn = create_lambda_function(
            handler_file=LAMBDA_ECHO_EVENT, func_name=lambda_name, runtime=Runtime.nodejs20_x
        )["CreateFunctionResponse"]["FunctionArn"]
        add_permission_for_integration_lambda(api_id, lambda_arn)

        integration_id_v1 = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="AWS_PROXY",
            PayloadFormatVersion="1.0",
            IntegrationMethod="ANY",
            IntegrationUri=lambda_arn,
        )["IntegrationId"]

        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            AuthorizationType="NONE",
            RouteKey="POST /example/test",
            Target=f"integrations/{integration_id_v1}",
        )

        aws_client.apigatewayv2.create_stage(ApiId=api_id, StageName="$default", AutoDeploy=True)

        base_path = "base-path"

        aws_client.apigatewayv2.create_api_mapping(
            ApiId=api_id,
            DomainName=used_domain_name,
            Stage="$default",
            ApiMappingKey=base_path,
        )

        def _invoke(url: str, expected_status_code: int):
            headers = {
                "Host": used_domain_name,
            }
            _resp = requests.post(url, headers=headers, verify=False)
            assert _resp.status_code == expected_status_code

        endpoint = api_invoke_url(api_id=api_id, path=f"{base_path}/example/test")
        retry(_invoke, url=endpoint, expected_status_code=200)

        endpoint = api_invoke_url(api_id=api_id, path=f"{base_path}/example/bad-route")
        _invoke(url=endpoint, expected_status_code=404)


class TestApigatewayV2CustomDomainCrud:
    @pytest.fixture(autouse=True)
    def auto_cleanup_domains(self, aws_client):
        # seems like some other tests are not cleaning up, so we need to remove all of them before
        if not is_aws_cloud():
            domains = aws_client.apigatewayv2.get_domain_names()["Items"]
            for domain in domains:
                aws_client.apigatewayv2.delete_domain_name(DomainName=domain["DomainName"])

    @pytest.mark.skipif(
        condition=not is_next_gen_api() and not is_aws_cloud(),
        reason="Not properly implemented in current implementation, legacy is not raising and not sharing fully",
    )
    @markers.aws.validated
    def test_custom_domains_crud(
        self,
        aws_client,
        acm_imported_cert,
        apigwv2_create_domain_name,
        apigwv1_create_domain,
        snapshot,
    ):
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("ApiGatewayDomainName"),
                snapshot.transform.key_value("HostedZoneId"),
                snapshot.transform.key_value("distributionHostedZoneId"),
                snapshot.transform.key_value("domainName"),
                snapshot.transform.key_value("DomainName"),
                snapshot.transform.resource_name(),
            ]
        )
        domain_name_v2 = f"{short_uid()}.{constants.LOCALHOST_HOSTNAME}"
        # create v2 domain
        response = apigwv2_create_domain_name(
            DomainName=domain_name_v2,
            DomainNameConfigurations=[
                {
                    "CertificateArn": acm_imported_cert,
                    "EndpointType": "REGIONAL",
                }
            ],
        )
        snapshot.match("create-domain-name-v2", response)
        regional_domain_name = response["DomainNameConfigurations"][0]["ApiGatewayDomainName"]
        # easier to assert than regex matching the snapshot
        # format in AWS: d-wvqa7etvk3.execute-api.<region>.amazonaws.com
        assert regional_domain_name.startswith("d-")
        assert ".execute-api." in regional_domain_name

        # create V1 domain
        if is_aws_cloud():
            # AWS is rate limiting aggressively
            time.sleep(30)
        domain_name_v1 = f"{short_uid()}.{constants.LOCALHOST_HOSTNAME}"
        response_v1 = apigwv1_create_domain(
            domainName=domain_name_v1,
            certificateArn=acm_imported_cert,
        )
        snapshot.match("create-domain-name-v1", response_v1)
        edge_domain_name = response_v1["distributionDomainName"]
        # format in AWS d3oypnw407gnmj.cloudfront.net
        assert ".cloudfront." in edge_domain_name

        # let check if domain is preserved between APIs (v1, v2)
        get_domain_v2_in_v2 = aws_client.apigatewayv2.get_domain_name(DomainName=domain_name_v2)
        snapshot.match("get-domain-name-from-v2-in-v2", get_domain_v2_in_v2)
        # v1 API
        get_domain_v2_in_v1 = aws_client.apigateway.get_domain_name(domainName=domain_name_v2)
        snapshot.match("get-domain-name-from-v2-in-v1", get_domain_v2_in_v1)

        get_domain_v1_in_v2 = aws_client.apigatewayv2.get_domain_name(DomainName=domain_name_v1)
        snapshot.match("get-domain-name-from-v1-in-v2", get_domain_v1_in_v2)
        # v1 API
        get_domain_v1_in_v1 = aws_client.apigateway.get_domain_name(domainName=domain_name_v1)
        snapshot.match("get-domain-name-from-v1-in-v1", get_domain_v1_in_v1)

        list_domains_v2 = aws_client.apigatewayv2.get_domain_names()
        snapshot.match("list-domains-v2", list_domains_v2)

        list_domains = aws_client.apigateway.get_domain_names()
        snapshot.match("list-domains-v1", list_domains)

    @markers.aws.validated
    @pytest.mark.skipif(
        condition=not is_next_gen_api() and not is_aws_cloud(),
        reason="Not properly implemented in current implementation, legacy is not raising",
    )
    def test_api_mappings_crud(
        self,
        aws_client,
        create_v2_api,
        acm_imported_cert,
        apigwv2_create_domain_name,
        apigwv2_create_api_mapping,
        snapshot,
    ):
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("ApiId"),
                snapshot.transform.key_value("ApiMappingId"),
            ]
        )

        result = create_v2_api(ProtocolType="HTTP", Name=f"{short_uid()}")
        api_id = result["ApiId"]

        domain_name = f"{short_uid()}.{constants.LOCALHOST_HOSTNAME}"
        apigwv2_create_domain_name(
            DomainName=domain_name,
            DomainNameConfigurations=[
                {
                    "CertificateArn": acm_imported_cert,
                    "EndpointType": "REGIONAL",
                }
            ],
        )

        aws_client.apigatewayv2.create_stage(ApiId=api_id, StageName="$default", AutoDeploy=True)

        with pytest.raises(ClientError) as e:
            apigwv2_create_api_mapping(
                ApiId="bad-api",
                DomainName=domain_name,
                Stage="(none)",
                ApiMappingKey="base-path",
            )
        snapshot.match("create-mapping-with-bad-api", e.value.response)

        with pytest.raises(ClientError) as e:
            apigwv2_create_api_mapping(
                ApiId=api_id,
                DomainName=domain_name,
                Stage="(none)",
                ApiMappingKey="base-path",
            )
        snapshot.match("create-mapping-with-none-stage", e.value.response)

        with pytest.raises(ClientError) as e:
            apigwv2_create_api_mapping(
                ApiId=api_id,
                DomainName="bad-name",
                Stage="$default",
                ApiMappingKey="base-path",
            )
        snapshot.match("create-mapping-with-bad-domain", e.value.response)

        create_mapping_none = apigwv2_create_api_mapping(
            ApiId=api_id,
            DomainName=domain_name,
            Stage="$default",
            ApiMappingKey="(none)",
        )
        snapshot.match("create-mapping-with-none-key", create_mapping_none)

        create_mapping = apigwv2_create_api_mapping(
            ApiId=api_id,
            DomainName=domain_name,
            Stage="$default",
            ApiMappingKey="base-path",
        )
        snapshot.match("create-mapping", create_mapping)
        mapping_id = create_mapping["ApiMappingId"]

        get_mapping = aws_client.apigatewayv2.get_api_mapping(
            ApiMappingId=mapping_id, DomainName=domain_name
        )
        snapshot.match("get-mapping", get_mapping)

        get_mappings = aws_client.apigatewayv2.get_api_mappings(DomainName=domain_name)
        get_mappings["Items"].sort(key=itemgetter("ApiMappingKey"))
        snapshot.match("get-mappings", get_mappings)

        get_mappings_v1 = aws_client.apigateway.get_base_path_mappings(domainName=domain_name)
        get_mappings_v1["items"].sort(key=itemgetter("basePath"))
        snapshot.match("get-mappings-v1", get_mappings_v1)

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.get_api_mapping(
                ApiMappingId="bad-mapping-id",
                DomainName=domain_name,
            )
        snapshot.match("get-mapping-bad-mapping-id", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.get_api_mapping(
                ApiMappingId=mapping_id,
                DomainName="bad-domain-name",
            )
        snapshot.match("get-mapping-bad-domain-name", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.update_api_mapping(
                ApiId=api_id,
                ApiMappingId="bad-mapping-id",
                DomainName=domain_name,
                ApiMappingKey="base-path-updated",
            )
        snapshot.match("update-mapping-bad-mapping-id", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.update_api_mapping(
                ApiId=api_id,
                DomainName="bad-domain-name",
                ApiMappingId=mapping_id,
                ApiMappingKey="base-path-updated",
            )
        snapshot.match("update-mapping-bad-domain-name", e.value.response)

        update_mapping = aws_client.apigatewayv2.update_api_mapping(
            ApiId=api_id,
            ApiMappingId=mapping_id,
            DomainName=domain_name,
            ApiMappingKey="base-path-updated",
        )
        snapshot.match("update-mapping", update_mapping)

        delete_mapping = aws_client.apigatewayv2.delete_api_mapping(
            ApiMappingId=mapping_id,
            DomainName=domain_name,
        )
        snapshot.match("delete-mapping", delete_mapping)
