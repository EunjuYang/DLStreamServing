#!/bin/bash

export StreamDLHome=~/DEV/StreamDLServing
export KAFKA_BK="143.248.146.115:9092,143.248.146.116:9092,143.248.146.117:9092"
export STREAM_PREFIX="dlstream.ami"
export PYTHONPATH=$StreamDLHome
export PATH=$PATH:$StreamDLHome/streamDL_pyclient


