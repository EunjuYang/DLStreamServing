FROM ubuntu:16.04

ARG USERNAME
ARG PASSWORD
ARG KAKAO="-i http://mirror.kakao.com/pypi/simple --trusted-host mirror.kakao.com"
ARG NAME
ARG MONGO_PORT_27017_TCP_ADDR
ARG MONGO_PORT_27017_TCP_PORT=27017

RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:fkrull/deadsnakes
RUn apt-get update
RUN apt-get install -y --no-install-recommends python3.6 python3.6-dev python3-pip python3-setuptools python3-wheel gcc g++
RUN apt-get install -y git

RUN python3.6 -m pip install pip --upgrade $KAKAO
RUN python3.6 -m pip install wheel $KAKAO
RUN python3.6 -m pip install setuptools --upgrade $KAKAO
RUN python3.6 -m pip install pymongo $KAKAO
RUN python3.6 -m pip install numpy $KAKAO


RUN git clone https://$USERNAME:$PASSWORD@github.com/EunjuYang/DLStreamServing.git
WORKDIR /DLStreamServing/testbench/create-data-mongo/

ENV NAME=NAME
ENV MONGO_PORT_27017_TCP_ADDR=MONGO_PORT_27017_TCP_ADDR
ENV MONGO_PORT_27017_TCP_PORT=MONGO_PORT_27017_TCP_PORT

ENTRYPOINT ["python3.6" ,"run.py"]