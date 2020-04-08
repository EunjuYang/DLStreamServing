FROM ubuntu:16.04
ARG MODEL_NAME
ARG NUM_AMI
ARG CEP_ID
ARG KAFKA_BK
ARG STREAM_BK
ARG BATCH_SIZE
ARG DTYPE
ARG MEM_METHOD

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:fkrull/deadsnakes
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3.6 python3.6-dev python3-pip python3-setuptools python3-wheel gcc
RUN apt-get install -y git

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

RUN git clone https://github.com/EunjuYang/DLStreamServing.git
WORKDIR /DLStreamServing/onlined-dl
ENV MODEL_NAME=MODEL_NAME
ENV NUM_AMI=NUM_AMI
ENV CEP_ID=CEP_ID
ENV KAFKA_BK=KAFKA_BK
ENV STREAM_BK=STREAM_BK
ENV BATCH_SIZE=BATCH_SIZE
ENV DTYPE=DTYPE
ENV MEM_METHOD=MEM_METHOD
