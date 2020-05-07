FROM ubuntu:16.04

ARG MODEL_NAME
ARG MODEL_REPO_ADDR
ARG RESULT_REPO_ADDR
ARG USERNAME
ARG PASSWORD

RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:fkrull/deadsnakes
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3.6 python3.6-dev python3-pip python3-setuptools python3-wheel gcc g++
RUN apt-get install -y git

# python package for online_serving
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel
RUN python3.6 -m pip install setuptools --upgrade
RUN python3.6 -m pip install tensorflow==2.1.0 -i http://mirror.kakao.com/pypi/simple --trusted-host mirror.kakao.com
RUN python3.6 -m pip install confluent-kafka -i http://mirror.kakao.com/pypi/simple --trusted-host mirror.kakao.com
RUN python3.6 -m pip install kafka
RUN python3.6 -m pip install pymongo

RUN git clone https://$USERNAME:$PASSWORD@github.com/iop851/DLStreamServing.git
WORKDIR /DLStreamServing/inference-dl
ENV PYTHONPATH=/DLStreamServing:/DLStreamServing/online-dl

ENV MODEL_NAME=MODEL_NAME
ENV MODEL_REPO_ADDR=MODEL_REPO_ADDR
ENV RESULT_REPO_ADDR=RESULT_REPO_ADDR