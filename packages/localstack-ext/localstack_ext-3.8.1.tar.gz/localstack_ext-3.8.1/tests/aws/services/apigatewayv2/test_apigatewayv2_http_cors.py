import json
import time
from urllib.parse import urlencode

import pytest
import requests
from botocore.exceptions import ClientError
from localstack.http import Response
from localstack.pro.core.aws.api.apigatewayv2 import Cors
from localstack.testing.aws.util import is_aws_cloud
from localstack.testing.pytest import markers
from localstack.testing.pytest.fixtures import PUBLIC_HTTP_ECHO_SERVER_URL
from localstack.utils.json import json_safe, try_json
from localstack.utils.sync import poll_condition, retry
from pytest_httpserver import HTTPServer
from rolo import Request
from tests.aws.services.apigateway.conftest import is_next_gen_api

PUBLIC_HTTP_NO_CORS_SERVER = "https://postman-echo.com"


@pytest.fixture
def apigw_cors_http_proxy_integration_get(httpserver: HTTPServer):
    def _get_uri(cors_headers_to_return: dict = None) -> str:
        """
        Returns an HTTP server URL for CORS requests that work both locally and for parity tests (against real AWS)
        """
        query_string = f"?{urlencode(cors_headers_to_return)}" if cors_headers_to_return else ""

        if is_aws_cloud():
            # we cannot use httpbin.org here because they return CORS headers by default, and you cannot override them
            # we can use https://postman-echo.com/response-headers by Postman instead
            # see https://www.postman.com/postman/published-postman-templates/documentation/ae2ja6x/postman-echo
            return f"{PUBLIC_HTTP_NO_CORS_SERVER}/response-headers{query_string}"

        def _echo(request: Request) -> Response:
            response_body = json.dumps(json_safe(request.args))
            return Response(response_body, status=200, headers=request.args)

        httpserver.expect_request("", method="GET").respond_with_handler(_echo)
        http_endpoint = httpserver.url_for("/")

        return f"{http_endpoint}{query_string}"

    return _get_uri


@pytest.fixture
def apigw_cors_http_proxy_integration_options(httpserver: HTTPServer):
    def _get_uri(with_cors_headers: bool = False) -> str:
        """
        Returns an HTTP server URL for CORS requests that work both locally and for parity tests (against real AWS)
        This is for OPTIONS requests, we need a specific fixture because services available online differs in setup
        """

        if is_aws_cloud():
            if with_cors_headers:
                # httpbin.org returns full CORS headers by default
                return f"{PUBLIC_HTTP_ECHO_SERVER_URL}/response-headers"
            else:
                # postman-echo.com does not return any CORS headers for OPTIONS requests
                return f"{PUBLIC_HTTP_NO_CORS_SERVER}/response-headers"

        def _echo(request: Request) -> Response:
            if with_cors_headers:
                # these are the headers returned by httpbin.org by default
                origin = request.headers.get("Origin") or "*"
                headers = {
                    "Access-Control-Allow-Origin": origin,
                    "Access-Control-Allow-Credentials": "true",
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
                    "Access-Control-Max-Age": "3600",
                }
                body = b""
            else:
                headers = {}
                body = b"DELETE,GET,HEAD,PATCH,POST,PUT"

            return Response(response=body, status=200, headers=headers)

        httpserver.expect_request("", method="OPTIONS").respond_with_handler(_echo)
        http_endpoint = httpserver.url_for("/")

        return http_endpoint

    return _get_uri


@pytest.fixture
def apigwv2_snapshot_transform(snapshot):
    snapshot.add_transformers_list(
        [
            snapshot.transform.key_value("Name"),
            snapshot.transform.key_value("ApiEndpoint"),
            snapshot.transform.key_value("ApiId"),
        ]
    )


@pytest.mark.skipif(
    not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in legacy"
)
class TestApigatewayV2CorsCrud:
    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        # TODO: AWS adds the empty dict Tags field after a call to UpdateApi
        paths=["$..Tags"],
    )
    def test_apigwv2_cors_crud_lifecycle(
        self, aws_client, create_v2_api, snapshot, apigwv2_snapshot_transform
    ):
        create_api = create_v2_api(
            ProtocolType="HTTP",
            CorsConfiguration={
                "AllowOrigins": ["http://localhost:3000"],
                "AllowMethods": ["POST", "GET"],
                "AllowHeaders": ["testHeader"],
                "AllowCredentials": True,
                "ExposeHeaders": ["exposedHeader"],
                "MaxAge": 10,
            },
        )
        snapshot.match("create-api", create_api)
        api_id = create_api["ApiId"]

        get_api = aws_client.apigatewayv2.get_api(ApiId=api_id)
        snapshot.match("get-api", get_api)

        update_api = aws_client.apigatewayv2.update_api(
            ApiId=api_id,
            CorsConfiguration={
                "AllowMethods": ["PATCH"],
            },
        )
        snapshot.match("update-api", update_api)

        get_api_after_update = aws_client.apigatewayv2.get_api(ApiId=api_id)
        snapshot.match("get-api-after-update", get_api_after_update)

        delete_cors = aws_client.apigatewayv2.delete_cors_configuration(ApiId=api_id)
        snapshot.match("delete-cors", delete_cors)

        get_api_after_delete = aws_client.apigatewayv2.get_api(ApiId=api_id)
        snapshot.match("get-api-after-delete", get_api_after_delete)

        create_api_default = create_v2_api(
            ProtocolType="HTTP",
            CorsConfiguration={
                "AllowOrigins": ["http://localhost:3000"],
            },
        )
        snapshot.match("create-api-default-cors", create_api_default)

    @markers.aws.validated
    def test_apigwv2_cors_crud_validation(
        self, aws_client, create_v2_api, snapshot, apigwv2_snapshot_transform
    ):
        # TODO: add more validation
        with pytest.raises(ClientError) as e:
            create_v2_api(
                ProtocolType="HTTP",
                CorsConfiguration={
                    "AllowOrigins": ["https://*.domain.com"],
                },
            )
        snapshot.match("no-partial-wildcard", e.value.response)

        with pytest.raises(ClientError) as e:
            create_v2_api(
                ProtocolType="HTTP",
                CorsConfiguration={
                    "AllowOrigins": ["https:/"],
                },
            )
        snapshot.match("no-partial-origin", e.value.response)

        with pytest.raises(ClientError) as e:
            create_v2_api(
                ProtocolType="HTTP",
                CorsConfiguration={
                    "AllowOrigins": ["http://localhost:3000", "*"],
                    "AllowCredentials": True,
                },
            )

        snapshot.match("no-credentials-with-wildcard", e.value.response)

        with pytest.raises(ClientError) as e:
            create_v2_api(
                ProtocolType="HTTP",
                CorsConfiguration={"AllowMethods": ["BAD"]},
            )

        snapshot.match("bad-allowed-methods", e.value.response)

        # create an API with only a wildcard origin
        create_api = create_v2_api(
            ProtocolType="HTTP",
            CorsConfiguration={
                "AllowOrigins": ["*"],
            },
        )
        snapshot.match("create-api-with-wildcard", create_api)
        api_id = create_api["ApiId"]

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.update_api(
                ApiId=api_id,
                CorsConfiguration={"AllowCredentials": True},
            )

        snapshot.match("update-credentials-with-wilcard", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.update_api(
                ApiId=api_id,
                CorsConfiguration={"AllowMethods": ["BAD"]},
            )

        snapshot.match("update-bad-method", e.value.response)


@pytest.mark.skipif(
    not is_next_gen_api() and not is_aws_cloud(),
    reason="Not implemented the full way in legacy",
)
@markers.snapshot.skip_snapshot_verify(
    # TODO: AWS adds the empty dict Tags field after a call to UpdateApi
    paths=["$..Tags"],
)
class TestApigatewayV2Cors:
    @pytest.fixture
    def create_v2_api_with_cors(self, aws_client, create_v2_api):
        def _create_api(get_uri: str, options_uri: str, cors_configuration: Cors = None):
            kwargs = {}
            if cors_configuration:
                kwargs["CorsConfiguration"] = cors_configuration
            create_api = create_v2_api(
                ProtocolType="HTTP",
                Target=get_uri,
                RouteKey="GET /get-cors",
                **kwargs,
            )
            api_id = create_api["ApiId"]

            options_integration = aws_client.apigatewayv2.create_integration(
                ApiId=api_id,
                IntegrationType="HTTP_PROXY",
                IntegrationUri=options_uri,
                IntegrationMethod="OPTIONS",
                PayloadFormatVersion="1.0",
            )
            aws_client.apigatewayv2.create_route(
                ApiId=api_id,
                RouteKey="OPTIONS /options-cors",
                Target=f"integrations/{options_integration['IntegrationId']}",
                AuthorizationType="NONE",
            )

            return create_api

        return _create_api

    @staticmethod
    def filter_and_lowercase_headers(
        headers: requests.models.CaseInsensitiveDict,
    ) -> dict[str, str]:
        removed_headers = {
            "allow",
            "connection",
            "content-length",
            "content-type",
            "date",
            "etag",
            "server",
            "set-cookie",
        }
        return {
            header.lower(): v
            for header, v in headers.items()
            if header.lower() not in removed_headers
        }

    def transform_response(self, response: requests.Response) -> dict:
        content = try_json(response.text) if response.text else ""
        if isinstance(content, str):
            # it seems `httpbin.org` returns a body for OPTIONS with the allowed methods like the `Allow` header
            # but it is randomized
            content = ",".join(sorted(content.split(",")))
        return {
            "statusCode": response.status_code,
            "headers": self.filter_and_lowercase_headers(response.headers),
            "content": content,
        }

    @markers.aws.validated
    def test_no_cors_config_with_no_cors_integration(
        self,
        aws_client,
        create_v2_api_with_cors,
        snapshot,
        apigw_cors_http_proxy_integration_options,
        apigw_cors_http_proxy_integration_get,
        apigwv2_snapshot_transform,
    ):
        snapshot.add_transformer(snapshot.transform.key_value("apigw-requestid"))
        get_uri_no_cors = apigw_cors_http_proxy_integration_get(cors_headers_to_return={})
        options_uri_no_cors = apigw_cors_http_proxy_integration_options(with_cors_headers=False)
        # create an API with no CORS configuration
        create_api = create_v2_api_with_cors(
            get_uri=get_uri_no_cors,
            options_uri=options_uri_no_cors,
        )
        snapshot.match("create-api", create_api)
        endpoint_url = create_api["ApiEndpoint"]

        def _get_first_req():
            resp = requests.get(f"{endpoint_url}/get-cors")
            assert resp.ok
            return resp

        get_request_no_cors = retry(_get_first_req, retries=3, sleep=3 if is_aws_cloud() else 0.1)
        snapshot.match("get-req-no-cors", self.transform_response(get_request_no_cors))

        get_request_cors = requests.get(
            f"{endpoint_url}/get-cors", headers={"Origin": "http://localhost:3000"}
        )
        snapshot.match("get-req-cors", self.transform_response(get_request_cors))

        options_request_no_cors_on_get = requests.options(
            f"{endpoint_url}/get-cors",
        )
        snapshot.match(
            "options-req-no-cors-on-get", self.transform_response(options_request_no_cors_on_get)
        )

        options_request_cors_on_get = requests.options(
            f"{endpoint_url}/get-cors",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        # assert 404
        snapshot.match(
            "options-req-cors-on-get", self.transform_response(options_request_cors_on_get)
        )

        options_request_no_cors = requests.options(
            f"{endpoint_url}/options-cors",
        )
        # assert 404
        snapshot.match("options-req-no-cors", self.transform_response(options_request_no_cors))

        options_request_cors = requests.options(
            f"{endpoint_url}/options-cors",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        snapshot.match("options-req-cors", self.transform_response(options_request_cors))

    @markers.aws.validated
    def test_no_cors_config_with_cors_integration(
        self,
        aws_client,
        create_v2_api_with_cors,
        snapshot,
        apigw_cors_http_proxy_integration_options,
        apigw_cors_http_proxy_integration_get,
        apigwv2_snapshot_transform,
    ):
        snapshot.add_transformer(snapshot.transform.key_value("apigw-requestid"))
        # we always return CORS headers, even if we don't send out the Origin, because it is hardcoded
        get_uri_cors = apigw_cors_http_proxy_integration_get(
            cors_headers_to_return={
                "Access-Control-Allow-Origin": "https://localhost:3000",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Expose-Headers": "X-My-Custom-Header, X-Another-Custom-Header",
            }
        )
        options_uri_cors = apigw_cors_http_proxy_integration_options(with_cors_headers=True)

        # create an API with no CORS configuration
        create_api = create_v2_api_with_cors(
            get_uri=get_uri_cors,
            options_uri=options_uri_cors,
        )
        snapshot.match("create-api", create_api)
        endpoint_url = create_api["ApiEndpoint"]

        def _get_first_req():
            resp = requests.get(f"{endpoint_url}/get-cors")
            assert resp.ok
            return resp

        get_request_no_cors = retry(_get_first_req, retries=3, sleep=3 if is_aws_cloud() else 0.1)
        snapshot.match("get-req-no-cors", self.transform_response(get_request_no_cors))

        get_request_cors = requests.get(
            f"{endpoint_url}/get-cors", headers={"Origin": "http://localhost:3000"}
        )
        snapshot.match("get-req-cors", self.transform_response(get_request_cors))

        options_request_no_cors_on_get = requests.options(
            f"{endpoint_url}/get-cors",
        )
        snapshot.match(
            "options-req-no-cors-on-get", self.transform_response(options_request_no_cors_on_get)
        )

        options_request_cors_on_get = requests.options(
            f"{endpoint_url}/get-cors",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        # This returns 404 because we did not configure an OPTIONS method for this Route
        snapshot.match(
            "options-req-cors-on-get", self.transform_response(options_request_cors_on_get)
        )

        options_request_no_cors = requests.options(
            f"{endpoint_url}/options-cors",
        )
        snapshot.match("options-req-no-cors", self.transform_response(options_request_no_cors))

        options_request_cors = requests.options(
            f"{endpoint_url}/options-cors",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        snapshot.match("options-req-cors", self.transform_response(options_request_cors))

    @markers.aws.validated
    def test_cors_config_with_no_cors_integration(
        self,
        aws_client,
        create_v2_api_with_cors,
        snapshot,
        apigw_cors_http_proxy_integration_options,
        apigw_cors_http_proxy_integration_get,
        apigwv2_snapshot_transform,
    ):
        snapshot.add_transformer(snapshot.transform.key_value("apigw-requestid"))
        # we always return CORS headers, even if we don't send out the Origin, because it is hardcoded
        get_uri_cors = apigw_cors_http_proxy_integration_get()
        options_uri_cors = apigw_cors_http_proxy_integration_options(with_cors_headers=False)

        # create an API with CORS configuration
        create_api = create_v2_api_with_cors(
            get_uri=get_uri_cors,
            options_uri=options_uri_cors,
            cors_configuration={
                "AllowOrigins": ["http://localhost:4000"],
                "AllowMethods": ["POST", "GET"],
                "AllowHeaders": ["testHeader"],
                "AllowCredentials": True,
                "ExposeHeaders": ["exposedHeader"],
                "MaxAge": 10,
            },
        )
        snapshot.match("create-api", create_api)
        endpoint_url = create_api["ApiEndpoint"]

        def _get_first_req():
            resp = requests.get(f"{endpoint_url}/get-cors")
            assert resp.ok
            return resp

        get_request_no_cors = retry(_get_first_req, retries=3, sleep=3 if is_aws_cloud() else 0.1)
        snapshot.match("get-req-no-cors", self.transform_response(get_request_no_cors))

        get_request_cors_ok = requests.get(
            f"{endpoint_url}/get-cors", headers={"Origin": "http://localhost:4000"}
        )
        snapshot.match("get-req-cors-ok", self.transform_response(get_request_cors_ok))

        get_request_cors_not_ok = requests.get(
            f"{endpoint_url}/get-cors", headers={"Origin": "http://localhost:3000"}
        )
        snapshot.match("get-req-cors-not-ok", self.transform_response(get_request_cors_not_ok))

        # we do not have an OPTIONS method configured for the GET /get-cors route, but APIGW automatically responds
        options_request_no_cors_on_get_no_origin = requests.options(
            f"{endpoint_url}/get-cors",
        )
        snapshot.match(
            "options-req-no-cors-on-get-no-origin",
            self.transform_response(options_request_no_cors_on_get_no_origin),
        )

        options_request_cors_on_get_origin = requests.options(
            f"{endpoint_url}/get-cors",
            headers={"Origin": "http://localhost:4000"},
        )
        snapshot.match(
            "options-req-cors-on-get-origin-no-methods",
            self.transform_response(options_request_cors_on_get_origin),
        )

        options_request_cors_on_get_origin_method = requests.options(
            f"{endpoint_url}/get-cors",
            headers={
                "Origin": "http://localhost:4000",
                "Access-Control-Request-Method": "GET",
            },
        )
        snapshot.match(
            "options-req-cors-on-get-origin-methods",
            self.transform_response(options_request_cors_on_get_origin_method),
        )

        options_request_no_cors = requests.options(
            f"{endpoint_url}/options-cors",
        )
        snapshot.match("options-req-no-cors", self.transform_response(options_request_no_cors))

        options_request_cors_not_ok = requests.options(
            f"{endpoint_url}/options-cors",
            headers={"Origin": "http://localhost:3000"},
        )
        snapshot.match(
            "options-req-cors-not-ok", self.transform_response(options_request_cors_not_ok)
        )

        options_request_cors_ok = requests.options(
            f"{endpoint_url}/options-cors",
            headers={
                "Origin": "http://localhost:4000",
                "Access-Control-Request-Method": "GET",
            },
        )
        snapshot.match("options-req-cors-ok", self.transform_response(options_request_cors_ok))

    @markers.aws.validated
    def test_cors_config_with_cors_integration(
        self,
        aws_client,
        create_v2_api_with_cors,
        snapshot,
        apigw_cors_http_proxy_integration_options,
        apigw_cors_http_proxy_integration_get,
        apigwv2_snapshot_transform,
    ):
        snapshot.add_transformer(snapshot.transform.key_value("apigw-requestid"))
        # we always return CORS headers, even if we don't send out the Origin, because it is hardcoded
        get_uri_cors = apigw_cors_http_proxy_integration_get(
            cors_headers_to_return={
                "Access-Control-Allow-Origin": "https://localhost:3000",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Expose-Headers": "X-My-Custom-Header, X-Another-Custom-Header",
            }
        )
        options_uri_cors = apigw_cors_http_proxy_integration_options(with_cors_headers=True)

        # create an API with CORS configuration
        create_api = create_v2_api_with_cors(
            get_uri=get_uri_cors,
            options_uri=options_uri_cors,
            cors_configuration={
                "AllowOrigins": ["http://localhost:4000"],
                "AllowMethods": ["POST", "GET"],
                "AllowHeaders": ["testHeader"],
                "AllowCredentials": True,
                "ExposeHeaders": ["exposedHeader"],
                "MaxAge": 10,
            },
        )
        snapshot.match("create-api", create_api)
        endpoint_url = create_api["ApiEndpoint"]

        def _get_first_req():
            resp = requests.get(f"{endpoint_url}/get-cors")
            assert resp.ok
            return resp

        get_request_no_cors = retry(_get_first_req, retries=3, sleep=3 if is_aws_cloud() else 0.1)
        snapshot.match("get-req-no-cors", self.transform_response(get_request_no_cors))

        get_request_cors_ok = requests.get(
            f"{endpoint_url}/get-cors", headers={"Origin": "http://localhost:4000"}
        )
        snapshot.match("get-req-cors-ok", self.transform_response(get_request_cors_ok))

        get_request_cors_not_ok = requests.get(
            f"{endpoint_url}/get-cors", headers={"Origin": "http://localhost:3000"}
        )
        snapshot.match("get-req-cors-not-ok", self.transform_response(get_request_cors_not_ok))

        # we do not have an OPTIONS method configured for the GET /get-cors route, but APIGW automatically responds
        options_request_no_cors_on_get_no_origin = requests.options(
            f"{endpoint_url}/get-cors",
        )
        snapshot.match(
            "options-req-no-cors-on-get-no-origin",
            self.transform_response(options_request_no_cors_on_get_no_origin),
        )

        options_request_cors_on_get_origin = requests.options(
            f"{endpoint_url}/get-cors",
            headers={"Origin": "http://localhost:4000"},
        )
        snapshot.match(
            "options-req-cors-on-get-origin-no-methods",
            self.transform_response(options_request_cors_on_get_origin),
        )

        options_request_cors_on_get_origin_method = requests.options(
            f"{endpoint_url}/get-cors",
            headers={
                "Origin": "http://localhost:4000",
                "Access-Control-Request-Method": "GET",
            },
        )
        snapshot.match(
            "options-req-cors-on-get-origin-methods",
            self.transform_response(options_request_cors_on_get_origin_method),
        )

        options_request_no_cors = requests.options(
            f"{endpoint_url}/options-cors",
        )
        snapshot.match("options-req-no-cors", self.transform_response(options_request_no_cors))

        options_request_cors_not_ok = requests.options(
            f"{endpoint_url}/options-cors",
            headers={"Origin": "http://localhost:3000"},
        )
        snapshot.match(
            "options-req-cors-not-ok", self.transform_response(options_request_cors_not_ok)
        )

        options_request_cors_ok = requests.options(
            f"{endpoint_url}/options-cors",
            headers={
                "Origin": "http://localhost:4000",
                "Access-Control-Request-Method": "GET",
            },
        )
        snapshot.match("options-req-cors-ok", self.transform_response(options_request_cors_ok))

    @markers.aws.validated
    def test_cors_updated_on_non_updated_deployment(
        self,
        aws_client,
        create_v2_api,
        snapshot,
        apigw_cors_http_proxy_integration_options,
        apigwv2_snapshot_transform,
    ):
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("apigw-requestid"),
                snapshot.transform.key_value("DeploymentId"),
            ]
        )
        int_uri_options_no_cors = apigw_cors_http_proxy_integration_options(with_cors_headers=False)

        # we do not want an API with $default stage and AutoDeploy
        create_api = create_v2_api(ProtocolType="HTTP")
        api_id = create_api["ApiId"]
        api_url = create_api["ApiEndpoint"]

        options_integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            IntegrationUri=int_uri_options_no_cors,
            IntegrationMethod="OPTIONS",
            PayloadFormatVersion="1.0",
        )
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="OPTIONS /options-cors",
            Target=f"integrations/{options_integration['IntegrationId']}",
            AuthorizationType="NONE",
        )

        deployments = aws_client.apigatewayv2.get_deployments(ApiId=api_id)
        snapshot.match("get-deployments", deployments)

        stage_name = "dev"
        aws_client.apigatewayv2.create_stage(ApiId=api_id, StageName=stage_name)
        create_deployment = aws_client.apigatewayv2.create_deployment(
            ApiId=api_id, StageName=stage_name
        )
        deployment_id = create_deployment["DeploymentId"]
        endpoint_url = f"{api_url}/{stage_name}"

        def poll_deployment_id(_deployment_id: str) -> bool:
            return (
                aws_client.apigatewayv2.get_deployment(ApiId=api_id, DeploymentId=_deployment_id)[
                    "DeploymentStatus"
                ]
                == "DEPLOYED"
            )

        if is_aws_cloud():
            poll_condition(
                lambda: poll_deployment_id(deployment_id),
                timeout=10,
                interval=1,
            )

        def _send_options_req() -> requests.Response:
            resp = requests.options(
                f"{endpoint_url}/options-cors",
                headers={
                    "Origin": "http://localhost:4000",
                    "Access-Control-Request-Method": "GET",
                },
            )
            assert resp.ok
            return resp

        get_request_cors = retry(_send_options_req, retries=3, sleep=3 if is_aws_cloud() else 0.1)
        snapshot.match(
            "options-req-cors-ok-not-configured", self.transform_response(get_request_cors)
        )

        update_cors = aws_client.apigatewayv2.update_api(
            ApiId=api_id,
            CorsConfiguration={
                "AllowOrigins": ["http://localhost:4000"],
                "AllowMethods": ["POST", "GET", "PATCH"],
                "AllowHeaders": ["testHeader", "X-Test-Header", "Another-Header"],
            },
        )
        snapshot.match("update-cors", update_cors)

        if is_aws_cloud():
            # just to be sure we're properly waiting, and that AWS really does not update the API
            time.sleep(10)

        options_request_cors_ok_configured = _send_options_req()
        snapshot.match(
            "options-req-cors-ok-configured",
            self.transform_response(options_request_cors_ok_configured),
        )

        create_deployment = aws_client.apigatewayv2.create_deployment(
            ApiId=api_id, StageName=stage_name
        )
        deployment_id = create_deployment["DeploymentId"]
        if is_aws_cloud():
            poll_condition(
                lambda: poll_deployment_id(deployment_id),
                timeout=10,
                interval=1,
            )

        options_request_cors_ok_configured = _send_options_req()
        snapshot.match(
            "options-req-cors-ok-deployed",
            self.transform_response(options_request_cors_ok_configured),
        )

        aws_client.apigatewayv2.delete_cors_configuration(ApiId=api_id)
        if is_aws_cloud():
            # just to be sure we're properly waiting, and that AWS really does not update the API
            time.sleep(10)

        options_request_cors_ok_deleted = _send_options_req()
        snapshot.match(
            "options-req-cors-ok-deleted", self.transform_response(options_request_cors_ok_deleted)
        )

        create_deployment = aws_client.apigatewayv2.create_deployment(
            ApiId=api_id, StageName=stage_name
        )
        deployment_id = create_deployment["DeploymentId"]
        if is_aws_cloud():
            poll_condition(
                lambda: poll_deployment_id(deployment_id),
                timeout=10,
                interval=1,
            )

        options_request_cors_ok_deleted = _send_options_req()
        snapshot.match(
            "options-req-cors-ok-now-deleted",
            self.transform_response(options_request_cors_ok_deleted),
        )

    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            # it seems LocalStack cannot return empty headers, it just removes them, but AWS does
            "$.options-req-cors-with-methods.headers.access-control-allow-headers",
        ]
    )
    def test_partial_cors_config_never_matches(
        self,
        aws_client,
        create_v2_api,
        snapshot,
        apigw_cors_http_proxy_integration_options,
        apigwv2_snapshot_transform,
    ):
        snapshot.add_transformer(snapshot.transform.key_value("apigw-requestid"))
        int_uri_options_no_cors = apigw_cors_http_proxy_integration_options(with_cors_headers=False)
        create_api = create_v2_api(
            ProtocolType="HTTP",
            Target=int_uri_options_no_cors,
            RouteKey="OPTIONS /cors",
            # if you don't specify AllowMethods and AllowHeaders to be either values or *, you can't match a request
            CorsConfiguration={"AllowOrigins": ["http://localhost:4000"]},
        )
        api_id = create_api["ApiId"]
        endpoint_url = create_api["ApiEndpoint"]

        def _send_options_req() -> requests.Response:
            resp = requests.options(
                f"{endpoint_url}/cors",
                headers={
                    "Origin": "http://localhost:4000",
                    "Access-Control-Request-Method": "GET",
                },
            )
            assert resp.ok
            return resp

        get_request_cors = retry(_send_options_req, retries=3, sleep=3 if is_aws_cloud() else 0.1)
        snapshot.match("options-req-cors-ok", self.transform_response(get_request_cors))

        aws_client.apigatewayv2.update_api(
            ApiId=api_id,
            CorsConfiguration={
                "AllowOrigins": ["http://localhost:4000"],
                "AllowMethods": ["*"],
            },
        )
        if is_aws_cloud():
            time.sleep(10)

        get_request_cors_with_methods = _send_options_req()
        snapshot.match(
            "options-req-cors-with-methods", self.transform_response(get_request_cors_with_methods)
        )

        with_methods_miss_header = requests.options(
            f"{endpoint_url}/cors",
            headers={
                "Origin": "http://localhost:4000",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "test,test2",
            },
        )
        snapshot.match(
            "options-req-cors-with-methods-miss-header",
            self.transform_response(with_methods_miss_header),
        )

        aws_client.apigatewayv2.update_api(
            ApiId=api_id,
            CorsConfiguration={
                "AllowOrigins": ["http://localhost:4000"],
                "AllowMethods": ["*"],
                "AllowHeaders": ["*"],
            },
        )
        if is_aws_cloud():
            time.sleep(10)

        get_request_cors_with_methods_and_headers = _send_options_req()
        snapshot.match(
            "options-req-cors-with-methods-and-headers",
            self.transform_response(get_request_cors_with_methods_and_headers),
        )

        with_methods_with_header = requests.options(
            f"{endpoint_url}/cors",
            headers={
                "Origin": "http://localhost:4000",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "test,test2",
            },
        )
        snapshot.match(
            "options-req-cors-with-methods-with-header",
            self.transform_response(with_methods_with_header),
        )

    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            # it seems LocalStack cannot return empty headers, it just removes them, but AWS does
            "$..access-control-allow-headers",
        ]
    )
    def test_wildcard_origin(
        self,
        aws_client,
        create_v2_api,
        snapshot,
        apigw_cors_http_proxy_integration_options,
        apigwv2_snapshot_transform,
    ):
        snapshot.add_transformer(snapshot.transform.key_value("apigw-requestid"))
        int_uri_options_no_cors = apigw_cors_http_proxy_integration_options(with_cors_headers=False)
        create_api = create_v2_api(
            ProtocolType="HTTP",
            Target=int_uri_options_no_cors,
            RouteKey="OPTIONS /cors",
            # if you don't specify AllowMethods and AllowHeaders to be either values or *, you can't match a request
            CorsConfiguration={
                "AllowOrigins": ["http://*"],
                "AllowMethods": ["*"],
            },
        )
        api_id = create_api["ApiId"]
        endpoint_url = create_api["ApiEndpoint"]

        def _send_options_req() -> requests.Response:
            resp = requests.options(
                f"{endpoint_url}/cors",
                headers={
                    "Origin": "http://localhost:4000",
                    "Access-Control-Request-Method": "GET",
                },
            )
            assert resp.ok
            return resp

        get_request_cors = retry(_send_options_req, retries=3, sleep=3 if is_aws_cloud() else 0.1)
        snapshot.match("options-req-cors-ok-http", self.transform_response(get_request_cors))

        aws_client.apigatewayv2.update_api(
            ApiId=api_id,
            CorsConfiguration={
                "AllowOrigins": ["https://*"],
            },
        )
        if is_aws_cloud():
            time.sleep(10)

        get_request_cors_with_methods = _send_options_req()
        snapshot.match(
            "options-req-cors-fail-https", self.transform_response(get_request_cors_with_methods)
        )

        https_origin = requests.options(
            f"{endpoint_url}/cors",
            headers={
                "Origin": "https://localhost:4000",
                "Access-Control-Request-Method": "GET",
            },
        )
        snapshot.match(
            "options-req-cors-ok-https",
            self.transform_response(https_origin),
        )

        get_request_cors_http = retry(
            _send_options_req, retries=3, sleep=3 if is_aws_cloud() else 0.1
        )
        snapshot.match("options-req-cors-fail-http", self.transform_response(get_request_cors_http))

        aws_client.apigatewayv2.update_api(
            ApiId=api_id,
            CorsConfiguration={
                "AllowOrigins": ["*"],
            },
        )
        if is_aws_cloud():
            time.sleep(10)

        get_request_cors_wildcard = retry(
            _send_options_req, retries=3, sleep=3 if is_aws_cloud() else 0.1
        )
        snapshot.match(
            "options-req-cors-ok-wilcard", self.transform_response(get_request_cors_wildcard)
        )

    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            # it seems LocalStack cannot return empty headers, it just removes them, but AWS does
            "$..access-control-allow-headers",
        ]
    )
    def test_origin_casing(
        self,
        aws_client,
        create_v2_api,
        snapshot,
        apigw_cors_http_proxy_integration_options,
        apigwv2_snapshot_transform,
    ):
        snapshot.add_transformer(snapshot.transform.key_value("apigw-requestid"))
        int_uri_options_no_cors = apigw_cors_http_proxy_integration_options(with_cors_headers=False)
        create_api = create_v2_api(
            ProtocolType="HTTP",
            Target=int_uri_options_no_cors,
            RouteKey="OPTIONS /cors",
            # if you don't specify AllowMethods and AllowHeaders to be either values or *, you can't match a request
            CorsConfiguration={
                "AllowOrigins": ["http://MyORIGIN.com"],
                "AllowMethods": ["*"],
            },
        )
        endpoint_url = create_api["ApiEndpoint"]
        snapshot.match("create-api-cors-casing", create_api)

        def _send_options_req(origin: str) -> requests.Response:
            resp = requests.options(
                f"{endpoint_url}/cors",
                headers={
                    "Origin": origin,
                    "Access-Control-Request-Method": "GET",
                },
            )
            assert resp.ok
            return resp

        get_request_cors = retry(
            _send_options_req,
            retries=3,
            sleep=3 if is_aws_cloud() else 0.1,
            origin="http://myorigin.com",
        )
        snapshot.match("options-req-cors-ok-http", self.transform_response(get_request_cors))
