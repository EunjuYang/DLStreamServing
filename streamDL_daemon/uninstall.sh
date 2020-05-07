#!/usr/bin/env bash

sudo systemctl stop streamDL.service
sudo systemctl disable streamDL.service
sudo rm /etc/systemd/system/streamDL.service
sudo rm -rf /opt/streamDL /var/log/streamDL

kubectl delete -f ./modelrepo-deployment.yaml
kubectl delete -f ./dlstream-namespace.yaml