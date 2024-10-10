import aws_cdk as cdk


class CaStack(cdk.Stack):
    root_ca: cdk.aws_acmpca.CfnCertificateAuthority

    def __init__(self, scope: cdk.App, id: str):
        super().__init__(scope, id)

        self.root_ca = cdk.aws_acmpca.CfnCertificateAuthority(
            self,
            "RootCA",
            type="ROOT",
            key_algorithm="RSA_2048",
            signing_algorithm="SHA256WITHRSA",
            usage_mode="SHORT_LIVED_CERTIFICATE",
            subject={
                "country": "US",
                "organization": "ExampleOrg",
                "organizational_unit": "ExampleRootCA",
                "distinguished_name_qualifier": "RootCA",
                "state": "CA",
            },
        )

        cdk.aws_ssm.StringParameter(
            self,
            "RootCAParameter",
            string_value=self.root_ca.attr_arn,
            parameter_name="/sample/scires/ca-arn",
        )

        cdk.CfnOutput(self, "RootCaArn", value=self.root_ca.attr_arn)
