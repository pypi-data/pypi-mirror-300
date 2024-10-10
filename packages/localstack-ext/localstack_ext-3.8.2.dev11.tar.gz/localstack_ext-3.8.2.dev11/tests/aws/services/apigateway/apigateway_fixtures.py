from enum import Enum

from localstack.services.apigateway.helpers import host_based_url, path_based_url
from localstack.testing.aws.util import is_aws_cloud
from localstack.utils.aws import aws_stack


class UrlType(Enum):
    HOST_BASED = 0
    PATH_BASED = 1


# TODO: remove aws_stack.get_boto3_region(), even though this is only used in tests
def api_invoke_url(
    api_id: str, stage: str = "", path: str = "/", url_type: UrlType = UrlType.HOST_BASED
) -> str:
    path = f"/{path}" if not path.startswith("/") else path
    if is_aws_cloud():
        stage = f"/{stage}" if stage else ""
        return f"https://{api_id}.execute-api.{aws_stack.get_boto3_region()}.amazonaws.com{stage}{path}"
    if url_type == UrlType.HOST_BASED:
        return host_based_url(api_id, stage_name=stage, path=path)
    return path_based_url(api_id, stage_name=stage, path=path)
