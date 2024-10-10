import aws_cdk as cdk
from localstack.testing.aws.util import is_aws_cloud
from localstack.testing.scenario.provisioning import InfraProvisioner


class RegisterCAStack(cdk.Stack):
    def __init__(
        self,
        scope: cdk.App,
        id: str,
        ca_arn: str,
        register_ca_lambda_key: str,
    ):
        super().__init__(scope, id)

        bucket = cdk.aws_s3.Bucket.from_bucket_name(
            self,
            "AssetBucket",
            bucket_name=InfraProvisioner.get_asset_bucket_cdk(self),
        )

        register_ca_lambda = cdk.aws_lambda.Function(
            self,
            "RegisterCAFunction",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_11,
            handler="index.handler",
            code=cdk.aws_lambda.S3Code(
                bucket=bucket,
                key=register_ca_lambda_key,
            ),
        )

        if not is_aws_cloud():
            register_ca_lambda.add_environment("IS_LOCAL", "true")

        register_ca_lambda.add_to_role_policy(
            statement=cdk.aws_iam.PolicyStatement(
                actions=["events:*"], resources=["*"], effect=cdk.aws_iam.Effect.ALLOW
            )
        )
        register_ca_lambda.add_to_role_policy(
            statement=cdk.aws_iam.PolicyStatement(
                actions=["lambda:*"], resources=["*"], effect=cdk.aws_iam.Effect.ALLOW
            )
        )
        register_ca_lambda.add_to_role_policy(
            statement=cdk.aws_iam.PolicyStatement(
                actions=["acm-pca:*"], resources=["*"], effect=cdk.aws_iam.Effect.ALLOW
            )
        )

        cdk.CustomResource(
            self,
            "RegisterCACustomResource",
            service_token=register_ca_lambda.function_arn,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            properties={
                "CAArn": ca_arn,
            },
        )
