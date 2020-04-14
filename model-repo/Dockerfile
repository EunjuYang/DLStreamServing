FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:fkrull/deadsnakes
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3.6 python3.6-dev python3-pip python3-setuptools python3-wheel gcc
RUN apt-get install -y git

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel
RUN sudo python3.6 -m pip install grpcio
RUN python3.6 -m pip install grpcio-tools

RUN git clone https://github.com/EunjuYang/DLStreamServing.git
WORKDIR /DLStreamServing/model-repo
RUN python3.6 -m grpc_tools.protoc -I. --python_out=./lib/ --grpc_python_out=./lib/ ./chunk.proto