#!/bin/bash

# FOR LOCALSTACK ONLY
export AWS_ENDPOINT_URL=http://localhost.localstack.cloud:4566
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test

yum update -y
yum install -y python3 python3-boto3 openssl awscli

mkdir -p /home/ec2-user

echo "from http.server import SimpleHTTPRequestHandler, HTTPServer
import ssl
import boto3
import json

ssm_client = boto3.client('ssm', region_name='us-east-1')
s3_client = boto3.client('s3', region_name='us-east-1')
bucket_name = ssm_client.get_parameter(Name='/sample/scires/cloudtrail-log-bucket')['Parameter']['Value']


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        response_content = {}
        if self.path.startswith('/logs'):
            objs = s3_client.get_paginator('list_objects_v2').paginate(Bucket=bucket_name).build_full_result()
            response_list = []
            for obj in objs['Contents']:
                response_list.append(obj['Key'])
            response_content['items'] = response_list
        else:
            response_content['message'] = 'Hello from the server instance!'

        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_content).encode('utf-8'))


if __name__ == '__main__':

    with open('/home/ec2-user/localstack_test_internal.crt') as fd:
        parts = fd.read().split('\t')
        for i, part  in enumerate(parts):
            with open(f'/home/ec2-user/localstack_test_internal.{i}.crt', 'w+') as f:
                f.write(part)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        certfile='/home/ec2-user/localstack_test_internal.0.crt',
        keyfile='/home/ec2-user/localstack_test_internal.pem'
    )
    server_address = ('', 8443)
    httpd = HTTPServer(server_address, Handler)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    print('Running server on port 8443...')
    httpd.serve_forever()
" > /home/ec2-user/server.py

cd /home/ec2-user

CA_ARN=$(aws --region us-east-1 ssm get-parameter --name '/sample/scires/ca-arn' --query 'Parameter.Value' --output text)

# Generate a private key and CSR
openssl genrsa -out localstack_test_internal.pem 2048
openssl req -new -key localstack_test_internal.pem -out localstack_test_internal.csr -subj "/CN=server.localstack.test.internal"

aws --region us-east-1 acm-pca issue-certificate \
    --certificate-authority-arn "${CA_ARN}" \
    --csr fileb://localstack_test_internal.csr \
    --signing-algorithm SHA256WITHRSA \
    --validity Value=7,Type=DAYS \
    --template-arn arn:aws:acm-pca:::template/EndEntityCertificate/V1 \
    --output text > certificate_arn.txt

# get new cert
aws --region us-east-1 acm-pca get-certificate \
    --certificate-authority-arn "${CA_ARN}" \
    --certificate-arn $(cat certificate_arn.txt) \
    --output text > localstack_test_internal.crt

cd /home/ec2-user

python3 server.py &
