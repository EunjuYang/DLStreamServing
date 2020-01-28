# Stream-Parser

Stream parser is automatically deployed by Stream Broker Daemon.
The stream parser is run as container.
To run this stream-parser manually, please use command below.

```bash
$ docker build -t dlstream/stream-parser:v01 \
               --build-arg Stream_Parser={KafkaNode0:portnum},{KafkaNode1:portnum},... \
                ${StreamDLServing}/stream-parser/ 

$ docker run \
                -e LOOP_BACK_WIN_SIZE=3 \
                -e INPUT_SHIFT_STEP=1 \
                -e SRC="f02G0fdGffW1" \
                -e DST="CEP_01" \
                -e LOK_FORWARD_STEP=1 \
                -e LOOK_FORWARD_WIN_SIZE=1 \
                -e IS_ONLINE_TRAIN=True \
                -e BOOTSTRAP_SERVERS="{kafkanode0:portnum},..." \
           dlstream/stream-parser:v01 \
           python3.6 stream-parser.py
    
```

