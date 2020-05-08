#!/bin/bash
kubectl create -f ./dlstream-namespace.yaml
kubectl create -f ./modelrepo-deployment.yaml

python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/streamDL.proto

echo "* create /opt/streamDL/ ..."
sudo mkdir -p /opt/streamDL /var/log/streamDL
echo "* copy all files to /opt/streamDL/ ..."
sudo cp -r ../ /opt/streamDL
sudo cp streamDL.service /etc/systemd/system/
echo "* Install dependency python package for root user"
sudo -E su <<HERE
echo "   ** Install kubernetes"
pip install kubernetes
echo "   ** Install pykafka"
pip install pykafka
echo "   ** Install grpcio and grpcio-tools"
pip install grpcio grpcio-tools
HERE


sudo -E systemctl daemon-reload
sudo -E systemctl enable streamDL.service
sudo -E systemctl start streamDL.service
sudo -E systemctl status streamDL.service

