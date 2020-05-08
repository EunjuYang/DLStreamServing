FROM ubuntu:16.04

ARG USERNAME
ARG PASSWORD

RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:fkrull/deadsnakes
RUn apt-get update
RUN apt-get install -y --no-install-recommends python3.6 python3.6-dev python3-pip python3-setuptools python3-wheel gcc g++
RUN apt-get install -y git

RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel
RUN python3.6 -m pip install setuptools --upgrade
RUN python3.6 -m pip install pymongo



RUN git clone https://$USERNAME:$PASSWORD@github.com/iop851/DLStreamServing.git
WORKDIR /DLStreamServing/testbench/create-data-mongo/