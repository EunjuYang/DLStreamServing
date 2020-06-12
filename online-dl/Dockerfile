FROM ubuntu:16.04
ARG MIRROR="-i http://mirror.kakao.com/pypi/simple --trusted-host mirror.kakao.com"

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
ARG BATCH_SIZE=32
ARG DTYPE
ARG IS_ADAPTIVE=False
ARG LB_SIZE=36
ARG LF_SIZE=1

# for model repo
ARG MODEL_REPO_ADDR
ARG USERNAME
ARG PASSWORD


RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list




RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:fkrull/deadsnakes
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3.6 python3.6-dev python3-pip python3-setuptools python3-wheel gcc g++
RUN apt-get install -y git

# python package for online_train
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel
RUN python3.6 -m pip install setuptools --upgrade
RUN python3.6 -m pip install tensorflow==2.1.0 $MIRROR
RUN python3.6 -m pip install quadprog
RUN python3.6 -m pip install scikit-learn
RUN python3.6 -m pip install confluent-kafka $MIRROR
RUN python3.6 -m pip install kafka
RUN python3.6 -m pip install pymongo $MIRROR

#RUN git clone https://github.com/EunjuYang/DLStreamServing.git
RUN git clone https://$USERNAME:$PASSWORD@github.com/EunjuYang/DLStreamServing.git
WORKDIR /DLStreamServing/online-dl
ENV PYTHONPATH=/DLStreamServing


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
ENV LB_SIZE=LB_SIZE
ENV LF_SIZE=LF_SIZE

ENV MODEL_REPO_ADDR=MODEL_REPO_ADDR
ENTRYPOINT ["python3.6" ,"online_trainer.py"]
