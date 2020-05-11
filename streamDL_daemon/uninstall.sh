#!/bin/bash

echo "* stop streamDL.service..."
sudo systemctl stop streamDL.service
echo "* disable streamDL.service..."
sudo systemctl disable streamDL.service
echo "* delete streamDL systemd..."
sudo rm /etc/systemd/system/streamDL.service
echo "* delete /opt/streamDL /var/log/streamDL..."
sudo rm -rf /opt/streamDL /var/log/streamDL

sudo su <<HERE
echo "   ** Install kubernetes"
pip uninstall -y kubernetes
echo "   ** Install pykafka"
pip uninstall -y pykafka
echo "   ** Install grpcio and grpcio-tools"
pip uninstall -y grpcio grpcio-tools
HERE

#kubectl delete -f ./modelrepo-deployment.yaml
#kubectl delete -f ./dlstream-namespace.yaml
#kubectl delete -f ./result-repo-deployment.yaml
