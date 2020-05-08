#!/bin/bash

export StreamDL_Home={Your StreamDL_Home DIR}
export KAFKA_BK={Your Kafka Broker Endpoint, IP:PORTNUM}
export STREAM_PREFIX={Your Kafka Topic Prefix to be used for StreamDL Serving}
export PYTHONPATH=$StreamDL_Home
export PATH=$PATH:$StreamDL_Home/streamDL_pyclient

