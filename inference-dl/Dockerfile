FROM ubuntu:16.04

ARG MODEL_NAME
ARG MODEL_REPO_ADDR
ARG RESULT_ADDR

ARG CEP_ID
ARG KAFKA_BK
ARG STREAM_BK
ARG BATCH_SIZE=1
ARG DTYPE
ARG LB_SIZE

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

RUN git clone https://$USERNAME:$PASSWORD@github.com/EunjuYang/DLStreamServing.git
RUN mkdir -p /tmp/inference/
WORKDIR /DLStreamServing/inference-dl
ENV PYTHONPATH=/DLStreamServing:/DLStreamServing/online-dl

ENV MODEL_NAME=MODEL_NAME
ENV MODEL_REPO_ADDR=MODEL_REPO_ADDR
ENV RESULT_ADDR=RESULT_ADDR

ENV CEP_ID=CEP_ID
ENV KAFKA_BK=KAFKA_BK
ENV STREAM_BK=STREAM_BK
ENV BATCH_SIZE=BATCH_SIZE
ENV DTYPE=DTYPE
ENV LB_SIZE=LB_SIZE

ENTRYPOINT ["python3.6" ,"online_serving.py"]