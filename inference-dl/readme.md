# InferenceDL
## Required Env Variable
###User Defined
* MODEL_NAME
* LB_SIZE
* LF_SIZE
###Broker
* MODEL_REPO_ADDR
* RESULT_ADDR: mongodb [ip:port]
* CEP_ID: target of stream-parser
* KAFKA_BK : kafka [ip:port, ip:port, ...]
* STREAM_BK : will be deprecated, but required.
* BATCH_SIZE : It is always adaptive but require batch size.
* DTYPE: dtype corresponding to stream-parser.
* PREFIX: CEP_ID prefix.
###RUN EXAMPLE
First, build Dockerfile.
```bash
.../inference-dl$ docker build -t dlstream/inferencedl:v01 . 
```
Then, run the built docker container.
```bash
$ docker run -d \
    -e MODEL_NAME=test \
    -e MODEL_REPO_ADDR=$ADDR:$PORT \ # Repository Server
    -e RESULT_ADDR=$ADDR:$PORT \ # mongo DB
    -e CEP_ID=dlstream.ami0 \
    -e KAFKA_BK=143.248.146.115:9092, ... \
    -e STREAM_BK=-1 \ # it will be deprecated.
    -e BATCH_SIZE=-1 \ # inference is always adaptive.
    -e DTYPE=float32 \
    -e LB_SIZE=36 \
    -e LF_SIZE=1 \
    -e PREFIX=dlstream.ami \
    dlstream/inferencedl:v01
```