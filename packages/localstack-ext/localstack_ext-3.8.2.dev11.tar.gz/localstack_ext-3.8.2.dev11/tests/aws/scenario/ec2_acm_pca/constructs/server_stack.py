import os

import aws_cdk as cdk
from localstack.pro.core import config as ext_config
from localstack.testing.aws.util import is_aws_cloud
from localstack.utils.files import load_file


class ServerStack(cdk.Stack):
    def __init__(
        self,
        scope: cdk.App,
        id: str,
        key_pair_name: str,
        ami_id: str,
    ):
        super().__init__(scope, id)

        executor = "aws_cloud" if is_aws_cloud() else ext_config.EC2_VM_MANAGER

        proxy_user_data_path = os.path.join(
            os.path.dirname(__file__), f"../userdata/{executor}/proxy_user_data.sh"
        )
        server_user_data_path = os.path.join(
            os.path.dirname(__file__), f"../userdata/{executor}/server_user_data.sh"
        )

        proxy_user_data_content = load_file(proxy_user_data_path)
        server_user_data_content = load_file(server_user_data_path)

        vpc = cdk.aws_ec2.Vpc(
            self,
            "Vpc",
            subnet_configuration=[
                {
                    "subnetType": cdk.aws_ec2.SubnetType.PUBLIC,
                    "name": "public",
                    "cidrMask": 24,
                },
                {
                    "subnetType": cdk.aws_ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    "name": "private",
                    "cidrMask": 24,
                },
            ],
            restrict_default_security_group=False,
        )

        private_hosted_zone = cdk.aws_route53.PrivateHostedZone(
            self,
            "PrivateHostedZone",
            vpc=vpc,
            zone_name="localstack.test.internal",
        )

        proxy_sg = cdk.aws_ec2.SecurityGroup(
            self,
            "ProxySecurityGroup",
            vpc=vpc,
            description="security group for proxy instance",
            allow_all_outbound=True,
        )
        proxy_sg.add_ingress_rule(
            cdk.aws_ec2.Peer.any_ipv4(), cdk.aws_ec2.Port.tcp(22), "allow ssh"
        )
        proxy_sg.add_ingress_rule(
            cdk.aws_ec2.Peer.any_ipv4(), cdk.aws_ec2.Port.tcp(8443), "allow https"
        )

        server_sg = cdk.aws_ec2.SecurityGroup(
            self,
            "ServerSecurityGroup",
            vpc=vpc,
            description="security group for server instance",
            allow_all_outbound=True,
        )
        server_sg.add_ingress_rule(proxy_sg, cdk.aws_ec2.Port.tcp(8443), "allow https access")
        server_sg.add_ingress_rule(
            proxy_sg, cdk.aws_ec2.Port.icmp_ping(), "allow pinging from public instance"
        )
        server_sg.add_ingress_rule(proxy_sg, cdk.aws_ec2.Port.tcp(22), "allow ssh access")

        pk = cdk.aws_ec2.KeyPair.from_key_pair_name(self, "SshKeyPair", key_pair_name)

        ssm_parameter = cdk.aws_ssm.StringParameter(
            self,
            "CustomParameter",
            description="Test parameter to access from the EC2 instance",
            parameter_name="/sample/scires/ec2-test-param",
            string_value="param123",
        )

        if is_aws_cloud():
            machine_image = cdk.aws_ec2.MachineImage.latest_amazon_linux2023()
        else:
            machine_image = cdk.aws_ec2.MachineImage.generic_linux({"us-east-1": ami_id})

        # proxy instance
        proxy_instance = cdk.aws_ec2.Instance(
            self,
            "ProxyInstance",
            vpc=vpc,
            instance_type=cdk.aws_ec2.InstanceType.of(
                instance_class=cdk.aws_ec2.InstanceClass.T3A,
                instance_size=cdk.aws_ec2.InstanceSize.MICRO,
            ),
            machine_image=machine_image,
            security_group=proxy_sg,
            vpc_subnets=cdk.aws_ec2.SubnetSelection(subnet_type=cdk.aws_ec2.SubnetType.PUBLIC),
            key_name=pk.key_pair_name,
            user_data_causes_replacement=True,
        )
        ssm_parameter.grant_read(proxy_instance)
        proxy_instance.role.add_managed_policy(
            cdk.aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ReadOnlyAccess")
        )
        proxy_instance.role.add_managed_policy(
            cdk.aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "AWSCertificateManagerPrivateCAFullAccess"
            )
        )
        proxy_instance.role.add_managed_policy(
            cdk.aws_iam.ManagedPolicy.from_aws_managed_policy_name("AWSPrivateCAUser")
        )
        proxy_instance.role.add_managed_policy(
            cdk.aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMReadOnlyAccess")
        )
        proxy_instance.add_user_data(proxy_user_data_content)

        # server instance
        server_instance = cdk.aws_ec2.Instance(
            self,
            "ServerInstance",
            vpc=vpc,
            instance_type=cdk.aws_ec2.InstanceType.of(
                instance_class=cdk.aws_ec2.InstanceClass.T3A,
                instance_size=cdk.aws_ec2.InstanceSize.MICRO,
            ),
            machine_image=machine_image,
            security_group=proxy_sg,
            vpc_subnets=cdk.aws_ec2.SubnetSelection(subnet_type=cdk.aws_ec2.SubnetType.PUBLIC),
            key_name=pk.key_pair_name,
            user_data_causes_replacement=True,
        )
        server_instance.role.add_managed_policy(
            cdk.aws_iam.ManagedPolicy.from_aws_managed_policy_name("AWSPrivateCAUser")
        )
        server_instance.role.add_managed_policy(
            cdk.aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ReadOnlyAccess")
        )
        server_instance.role.add_managed_policy(
            cdk.aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "AWSCertificateManagerPrivateCAFullAccess"
            )
        )
        server_instance.role.add_managed_policy(
            cdk.aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMReadOnlyAccess")
        )
        server_instance.role.add_managed_policy(
            cdk.aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
        )
        server_instance.add_user_data(server_user_data_content)

        cdk.aws_route53.ARecord(
            self,
            "record",
            zone=private_hosted_zone,
            record_name="server.localstack.test.internal",
            target=cdk.aws_route53.RecordTarget.from_ip_addresses(
                server_instance.instance_private_ip
                if is_aws_cloud()
                else server_instance.instance_public_ip
            ),
        )

        cdk.aws_ssm.StringParameter(
            self,
            "ProxyIpParam",
            description="IP of the proxy",
            parameter_name="/sample/scires/ec2-proxy-ip",
            string_value=proxy_instance.instance_private_ip,
        )

        cdk.aws_ssm.StringParameter(
            self,
            "ServerIpParam",
            description="IP of the server",
            parameter_name="/sample/scires/ec2-server-ip",
            string_value=server_instance.instance_private_ip
            if is_aws_cloud()
            else server_instance.instance_public_ip,
        )

        cdk.CfnOutput(
            self,
            "PublicDnsName",
            value=proxy_instance.instance_public_dns_name,
        )
        cdk.CfnOutput(self, "ProxyIp", value=proxy_instance.instance_private_ip)
        cdk.CfnOutput(self, "ProxyPublicIp", value=proxy_instance.instance_public_ip)
        cdk.CfnOutput(self, "ProxyInstanceId", value=proxy_instance.instance_id)
        cdk.CfnOutput(self, "ServerIp", value=server_instance.instance_private_ip)
        cdk.CfnOutput(self, "ServerInstanceId", value=server_instance.instance_id)
