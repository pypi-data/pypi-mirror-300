import json
import os.path
from typing import Optional
from uuid import uuid4

import paramiko
import pytest
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from localstack.pro.core import config as ext_config
from localstack.pro.core.services.ec2.vmmanager.docker import DockerVmManager
from localstack.testing.aws.util import is_aws_cloud
from localstack.testing.pytest import markers
from localstack.testing.scenario.cdk_lambda_helper import load_python_lambda_to_s3
from localstack.utils.common import is_linux
from localstack.utils.container_utils.container_client import NoSuchImage
from localstack.utils.docker_utils import DOCKER_CLIENT
from localstack.utils.files import new_tmp_dir, rm_rf, save_file
from localstack.utils.sync import retry
from paramiko.client import SSHClient
from paramiko.rsakey import RSAKey

from tests.aws.scenario.ec2_acm_pca.constructs.ca_stack import CaStack
from tests.aws.scenario.ec2_acm_pca.constructs.register_ca_stack import RegisterCAStack
from tests.aws.scenario.ec2_acm_pca.constructs.server_stack import ServerStack
from tests.aws.scenario.ec2_acm_pca.constructs.trail_stack import TrailStack


@markers.acceptance_test
@pytest.mark.skipif(
    condition=ext_config.EC2_VM_MANAGER != "docker", reason="Only docker executor is supported"
)
@pytest.mark.skipif(condition=not is_linux(), reason="Only linux is supported for this test")
class TestEC2ACMPCA:
    # Stack names
    STACK_NAME_CA = "EC2ACMPCACaStack"
    STACK_NAME_REGISTER_CA = "EC2ACMPCARegisterCAStack"
    STACK_NAME_SERVER = "EC2ACMPCAServerStack"
    STACK_NAME_TRAIL = "EC2ACMPCATrailStack"

    # Bucket keys
    LAMBDA_BUCKET = f"lambda-bucket-{uuid4().hex}"
    REGISTER_CA_LAMBDA_KEY = "register_ca.zip"

    # SSH Setup
    TMP_DIR = new_tmp_dir()
    EC2_KEY_PAIR_NAME = "ACMPCAEC2KeyPair"
    PRIVATE_KEY_PATH = f"{TMP_DIR}/{EC2_KEY_PAIR_NAME}.pem"
    PUBLIC_KEY_PATH = f"{TMP_DIR}/{EC2_KEY_PAIR_NAME}.public"

    # AMI
    AMAZONLINUX_2023_AMI = ("ami-024f768332f0", "amazonlinux-2023")
    AMAZONLINUX_2023_DOCKER_IMAGE = "localstack/ami-amazonlinux:2023"

    @pytest.fixture(scope="class")
    def create_keys(self, aws_client):
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )
        public_key_material = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.OpenSSH, format=serialization.PublicFormat.OpenSSH
        )

        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )

        save_file(self.PRIVATE_KEY_PATH, content=pem, permissions=0o600)
        save_file(self.PUBLIC_KEY_PATH, content=public_key_material)

        aws_client.ec2.import_key_pair(
            KeyName=self.EC2_KEY_PAIR_NAME,
            PublicKeyMaterial=public_key_material.decode("utf-8"),
        )

        yield pem, public_key_material

        rm_rf(self.TMP_DIR)
        aws_client.ec2.delete_key_pair(KeyName=self.EC2_KEY_PAIR_NAME)

    @pytest.fixture(scope="function")
    def ssh_client(self):
        client: Optional[SSHClient] = None

        def _create(ip, private_key_path):
            nonlocal client
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            private_key = RSAKey(filename=private_key_path)
            client.connect(
                ip,
                username="ec2-user" if is_aws_cloud() else "root",
                pkey=private_key,
            )
            return client

        yield _create

        if client:
            client.close()

    @pytest.fixture(scope="class")
    def setup_ami(self):
        """
        Setups up the AMI for the test
        """
        ami_id, ami_name = self.AMAZONLINUX_2023_AMI
        docker_image = self.AMAZONLINUX_2023_DOCKER_IMAGE

        target_image = f"{DockerVmManager.image_name_from_ami_name(ami_name=ami_name)}:{ami_id}"

        try:
            DOCKER_CLIENT.inspect_image(docker_image, pull=False)
        except NoSuchImage:
            DOCKER_CLIENT.pull_image(docker_image)

        DOCKER_CLIENT.tag_image(source_ref=docker_image, target_name=target_image)

    @pytest.fixture(scope="class", autouse=True)
    def infrastructure(self, aws_client, setup_ami, create_keys, infrastructure_setup):
        infra = infrastructure_setup(namespace="EC2ACMPCA", force_synth=True)

        register_ca_fn_path = os.path.join(
            os.path.dirname(__file__), "functions/cfn/register_ca.py"
        )

        # Custom setup provisioning steps
        infra.add_custom_setup_provisioning_step(
            lambda: load_python_lambda_to_s3(
                aws_client.s3,
                bucket_name=infra.get_asset_bucket(),
                key_name=self.REGISTER_CA_LAMBDA_KEY,
                code_path=register_ca_fn_path,
                additional_python_packages=["crhelper"],
            )
        )

        stack_ca = CaStack(infra.cdk_app, self.STACK_NAME_CA)
        RegisterCAStack(
            infra.cdk_app,
            self.STACK_NAME_REGISTER_CA,
            ca_arn=stack_ca.root_ca.attr_arn,
            register_ca_lambda_key=self.REGISTER_CA_LAMBDA_KEY,
        )
        ServerStack(
            infra.cdk_app,
            self.STACK_NAME_SERVER,
            key_pair_name=self.EC2_KEY_PAIR_NAME,
            ami_id=self.AMAZONLINUX_2023_AMI[0],
        )
        TrailStack(infra.cdk_app, self.STACK_NAME_TRAIL)

        with infra.provisioner() as prov:
            yield prov

    @markers.aws.validated
    def test_curl_from_client(self, aws_client, infrastructure, ssh_client):
        server_stack_output = infrastructure.get_stack_outputs(self.STACK_NAME_SERVER)
        proxy_instance_id = server_stack_output["ProxyInstanceId"]
        proxy_public_ip = server_stack_output["ProxyPublicIp"]

        def _check_proxy_server_instance_status():
            instance_status = aws_client.ec2.describe_instance_status(
                InstanceIds=[proxy_instance_id]
            )
            assert instance_status["InstanceStatuses"][0]["InstanceStatus"]["Status"] == "ok"

        def _check_proxy_server_system_status():
            instance_status = aws_client.ec2.describe_instance_status(
                InstanceIds=[proxy_instance_id]
            )
            assert instance_status["InstanceStatuses"][0]["SystemStatus"]["Status"] == "ok"

        # waiting for instance status and system status to be ok
        retry(_check_proxy_server_instance_status, retries=300, sleep=1)
        retry(_check_proxy_server_system_status, retries=300, sleep=1)

        client = ssh_client(ip=proxy_public_ip, private_key_path=self.PRIVATE_KEY_PATH)

        def _check_cloudtrail_health():
            nonlocal client
            stdin, stdout, stderr = client.exec_command(
                "curl https://server.localstack.test.internal:8443", timeout=5
            )
            response = stdout.read().decode("utf-8")
            response_json = json.loads(response)
            assert response_json["message"] == "Hello from the server instance!"

        # wait for 5 min  in (cloud init can take 5 min to complete)
        retry(_check_cloudtrail_health, retries=300, sleep=1)

        def _check_cloudtrail_logs():
            nonlocal client
            stdin, stdout, stderr = client.exec_command(
                "curl https://server.localstack.test.internal:8443/logs", timeout=5
            )
            response = stdout.read().decode("utf-8")
            response_json = json.loads(response)
            assert len(response_json["items"]) > 2

        # wait for 900 sec (cloudtrail logs can take 5-10 min to appear)
        retry(_check_cloudtrail_logs, retries=900 if is_aws_cloud() else 10, sleep=1)
