#!/bin/bash

# FOR LOCALSTACK ONLY
export AWS_ENDPOINT_URL=http://localhost.localstack.cloud:4566
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test

yum update -y
yum install -y python3 python3-pip python3-boto3 openssl awscli
pip install requests

mkdir -p /home/ec2-user

echo "from http.server import SimpleHTTPRequestHandler, HTTPServer
import ssl
import requests


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # call the server instance and return the response
        response = requests.get(f'https://server.localstack.test.internal:8443{self.path}')
        self.send_response(response.status_code)
        self.send_header('Content-type',response.headers['Content-Type'])
        self.end_headers()
        self.wfile.write(response.content)


if __name__ == '__main__':
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, Handler)
    print('Running server on port 8080...')
    httpd.serve_forever()
" > /home/ec2-user/server.py

cd /home/ec2-user

CA_ARN=$(aws --region us-east-1 ssm get-parameter --name '/sample/scires/ca-arn' --query 'Parameter.Value' --output text)

aws --region us-east-1 acm-pca get-certificate-authority-certificate --certificate-authority-arn $CA_ARN --output text > ca_root.crt
cp ca_root.crt /etc/pki/ca-trust/source/anchors/
update-ca-trust

python3 server.py &
