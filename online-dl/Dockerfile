FROM ubuntu:16.04
# for both incremental and continual
ARG MODEL_NAME
ARG ONLINE_METHOD
ARG FRAMEWORK=keras
ARG SAVEWEIGHT=False

# only for continual
ARG MEM_METHOD=cossim
ARG NUM_AMI
ARG EPISODIC_MEM_SIZE=100
ARG IS_SCHEDULE=True

# for stream
ARG CEP_ID
ARG KAFKA_BK
ARG STREAM_BK
ARG BATCH_SIZE
ARG DTYPE
ARG IS_ADAPTIVE=False

# for model repo
ARG MODEL_REPO_ADDR

ARG USERNAME
ARG PASSWORD

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:fkrull/deadsnakes
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3.6 python3.6-dev python3-pip python3-setuptools python3-wheel gcc
RUN apt-get install -y git

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

#RUN git clone https://github.com/EunjuYang/DLStreamServing.git
RUN git clone https://$USERNAME:$PASSWORD@github.com/EunjuYang/DLStreamServing.git
WORKDIR /DLStreamServing/onlined-dl
RUN git checkout feature-model-repo
ENV PYTHONPATH=/DLStreamServing/stream_dl_api

ENV MODEL_NAME=MODEL_NAME
ENV ONLINE_METHOD=ONLINE_METHOD
ENV FRAMEWORK=FRAMEWORK
ENV SAVEWEIGHT=SAVEWEIGHT
ENV MEM_METHOD=MEM_METHOD
ENV NUM_AMI=NUM_AMI
ENV EPISODIC_MEM_SIZE=EPISODIC_MEM_SIZE
ENV IS_SCHEDULE=IS_SCHEDULE

ENV CEP_ID=CEP_ID
ENV KAFKA_BK=KAFKA_BK
ENV STREAM_BK=STREAM_BK
ENV BATCH_SIZE=BATCH_SIZE
ENV DTYPE=DTYPE
ENV IS_ADAPTIVE=IS_ADAPTIVE
ENV MODEL_REPO_ADDR=MODEL_REPO_ADDR

