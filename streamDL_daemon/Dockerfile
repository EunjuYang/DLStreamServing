FROM ubuntu:16.04

ARG USERNAME
ARG PASSWORD

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:fkrull/deadsnakes
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3.6 python3.6-dev python3-pip python3-setuptools python3-wheel gcc g++
RUN apt-get install -y git

# python package for online_serving
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel
RUN python3.6 -m pip install pykafka
RUN python3.6 -m pip install kubernetes
RUN python3.6 -m pip install grpcio grpcio-tools

RUN git clone https://$USERNAME:$PASSWORD@github.com/EunjuYang/DLStreamServing.git
WORKDIR /DLStreamServing/streamDL_daemon
ENV PYTHONPATH=/DLStreamServing/:/DLStreamServing/online-dl
ENV STREAMDL_MODE="POD"

ENTRYPOINT ["python3.6" ,"server.py"]