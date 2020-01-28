FROM ubuntu:16.04
ARG Bootstrap_Servers
ARG Loop_Back_Win_Size
ARG Input_Shift_Step=1
ARG Src
ARG Dst
ARG Look_Forward_Step
ARG Look_Forward_Win_Size
ARG Is_Online_Train=False

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:fkrull/deadsnakes
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3.6 python3.6-dev python3-pip python3-setuptools python3-wheel gcc
RUN apt-get install -y git

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel
RUN pip3 install confluent-kafka

RUN git clone https://github.com/EunjuYang/DLStreamServing.git
WORKDIR /DLStreamServing/stream-parser
ENV BOOTSTRAP_SERVERS=Bootstrap_Servers
ENV LOOK_BACK_WIN_SIZE=Loop_Back_Win_Size
ENV INPUT_SHIRT_STEP=Input_Shift_Step
ENV SRC=Src
ENV DST=Dst
ENV LOOK_FORWARD_STEP=Look_Forward_Step
ENV LOOK_FORWARD_WIN_SIZE=Look_Forward_Win_Size
ENV IS_ONLINE_TRAIN=Is_Online_Train
