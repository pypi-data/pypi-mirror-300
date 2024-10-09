from __future__ import print_function

import logging
import os

import boto3
from crhelper import CfnResource

logger = logging.getLogger(__name__)
is_local = os.getenv("IS_LOCAL", "false")
ssl_verify = False if is_local == "true" else True
helper = CfnResource(
    json_logging=False, log_level="DEBUG", boto_level="CRITICAL", ssl_verify=ssl_verify
)


def _client(event, client_type):
    aws_default_region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    return boto3.client(client_type, region_name=aws_default_region)


@helper.create
def create(event, context):
    logger.info("Creating resource with event: %s", event)
    ca_arn = event["ResourceProperties"]["CAArn"]

    acm_pca = _client(event, "acm-pca")
    logger.info("Getting certificate authority CSR for CA %s", ca_arn)
    csr = acm_pca.get_certificate_authority_csr(CertificateAuthorityArn=ca_arn)["Csr"]
    logger.info("Issuing certificate for CA %s", ca_arn)
    certificate_arn = acm_pca.issue_certificate(
        CertificateAuthorityArn=ca_arn,
        Csr=csr,
        SigningAlgorithm="SHA256WITHRSA",
        Validity={"Value": 3650, "Type": "DAYS"},
        TemplateArn="arn:aws:acm-pca:::template/RootCACertificate/V1",
    )["CertificateArn"]

    helper.Data.update({"CertificateArn": certificate_arn})

    return


@helper.delete
def delete(event, context):
    logger.info("Deleting resource with event: %s", event)
    acm_pca = _client(event, "acm-pca")
    ca_arn = event["ResourceProperties"]["CAArn"]

    logger.info("Disabling CA %s", ca_arn)
    acm_pca.update_certificate_authority(CertificateAuthorityArn=ca_arn, Status="DISABLED")
    acm_pca.delete_certificate_authority(
        CertificateAuthorityArn=ca_arn, PermanentDeletionTimeInDays=7
    )


@helper.poll_create
def poll_create(event, context):
    logger.info("Polling for certificate issuance")

    ca_arn = event["ResourceProperties"]["CAArn"]
    certificate_arn = event["CrHelperData"]["CertificateArn"]

    acm_pca = _client(event, "acm-pca")

    logger.info("Waiting for certificate to be issued for CA %s", ca_arn)

    try:
        logger.info("Retrieving certificate for CA %s", ca_arn)
        certificate = acm_pca.get_certificate(
            CertificateAuthorityArn=ca_arn, CertificateArn=certificate_arn
        )["Certificate"]

        logger.info("Importing certificate for CA %s", ca_arn)
        acm_pca.import_certificate_authority_certificate(
            CertificateAuthorityArn=ca_arn, Certificate=certificate
        )
        return True
    except Exception as e:
        logger.info("Certificate not yet issued for CA %s: %s", ca_arn, e)
        return False


def handler(event, context):
    helper(event, context)
