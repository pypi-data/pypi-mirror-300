#!/bin/bash
sudo yum update -y
sudo yum install -y python3 python3-boto3 awscli

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

# Create systemd service
cat << EOF > /etc/systemd/system/python-server.service
[Unit]
Description=Python HTTP Server
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/ec2-user/server.py
Restart=on-failure
User=ec2-user

[Install]
WantedBy=multi-user.target
EOF

cd /home/ec2-user

CA_ARN=$(aws --region us-east-1 ssm get-parameter --name '/sample/scires/ca-arn' --query 'Parameter.Value' --output text)

aws --region us-east-1 acm-pca get-certificate-authority-certificate --certificate-authority-arn $CA_ARN --output text > ca_root.crt
sudo cp ca_root.crt /etc/pki/ca-trust/source/anchors/
sudo update-ca-trust

chown ec2-user:ec2-user *

# Reload systemd to pick up the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable python-server.service

# Start the Python server service immediately
sudo systemctl start python-server.service

# Retry mechanism to start the Python server with 5 attempts
attempt=0
max_attempts=5

while [ $attempt -lt $max_attempts ]; do
    sleep 5
    if [ $(sudo systemctl is-active python-server.service) == "active" ]; then
        echo "Service is active."
        break
    fi

    attempt=$((attempt + 1))
    echo "Attempt $attempt failed... retrying in 5 seconds."
    sudo systemctl start python-server.service
done

if [ $attempt -ge $max_attempts ]; then
    echo "Service failed to start after $max_attempts attempts."
fi
