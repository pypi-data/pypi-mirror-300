import aws_cdk as cdk


class TrailStack(cdk.Stack):
    def __init__(self, scope: cdk.App, id: str):
        super().__init__(scope, id)

        trail_bucket = cdk.aws_s3.Bucket(
            self,
            "TrailBucket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        cdk.aws_cloudtrail.Trail(
            self,
            "Trail",
            bucket=trail_bucket,
            management_events=cdk.aws_cloudtrail.ReadWriteType.ALL,
            is_multi_region_trail=False,
        )

        cdk.aws_ssm.StringParameter(
            self,
            "LogBucketParameter",
            string_value=trail_bucket.bucket_name,
            parameter_name="/sample/scires/cloudtrail-log-bucket",
        )

        cdk.CfnOutput(self, "TrailBucketName", value=trail_bucket.bucket_name)
