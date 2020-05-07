#!/usr/bin/env bash
export KAFKA_BK="143.248.146.115:9092,143.248.146.116:9092,143.248.146.117:9092"
export STREAM_PREFIX="dlstream.ami"

kubectl create -f ./dlstream-namespace.yaml
kubectl create -f ./modelrepo-deployment.yaml

python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/streamDL.proto

sudo mkdir -p /opt/streamDL /var/log/streamDL
sudo cp *.py /opt/streamDL
sudo cp streamDL.service /etc/systemd/system/


sudo systemctl daemon-reload
sudo systemctl enable streamDL.service
sudo systemctl start streamDL.service
sudo systemctl status streamDL.service

