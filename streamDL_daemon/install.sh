#!/usr/bin/env bash

python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/streamDL.proto

sudo mkdir -p /opt/streamDL /var/log/streamDL
sudo cp *.py /opt/streamDL
sudo cp streamDL.service /etc/systemd/system/


sudo systemctl daemon-reload
sudo systemctl enable streamDL.service
sudo systemctl start streamDL.service
sudo systemctl status streamDL.service

kubectl create -f ./dlstream-namespace.yaml