#!/bin/bash

export StreamDLHome={YOUR StreamDL Home}
export KAFKA_BK="{your-kafka-node}"
export STREAM_PREFIX="dlstream.ami"
export PYTHONPATH=$StreamDLHome
export PATH=$PATH:$StreamDLHome/streamDL_pyclient
export STREAMDL_MODE="SYSDAEMON"

