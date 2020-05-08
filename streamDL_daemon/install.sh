#!/bin/bash
#kubectl create -f ./dlstream-namespace.yaml
#kubectl create -f ./modelrepo-deployment.yaml

python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/streamDL.proto

echo "* create /opt/streamDL/ ..."
sudo mkdir -p /opt/streamDL /var/log/streamDL
echo "* copy all files to /opt/streamDL/ ..."
sudo cp -r ../ /opt/streamDL
sudo cp streamDL.service /etc/systemd/system/
echo "* Install dependency python package for root user"
sudo su <<HERE
echo "   ** Install kubernetes"
pip install kubernetes
echo "   ** Install pykafka"
pip install pykafka
HERE


sudo systemctl daemon-reload
sudo systemctl enable streamDL.service
sudo systemctl start streamDL.service
sudo systemctl status streamDL.service

