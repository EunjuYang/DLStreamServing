# InferenceDL
## Env Variable
###User
* MODEL_NAME
###Broker
* MODEL_REPO_ADDR
* RESULT_REPO_ADDR: mongodb [ip:port]
* CEP_ID: target of stream-parser
* KAFKA_BK : kafka [ip:port, ip:port, ...]
* STREAM_BK : will be deprecated, but required.
* BATCH_SIZE : max batch size according to dlcep. It is always adaptive but require batch size.
* DTYPE: dtype corresponding to stream-parser.