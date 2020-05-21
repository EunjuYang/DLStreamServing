# Online-DL
To support the function of online deep learning with using common deep learning library, we provide an online-dl module.
Online-DL instance will be launched when serving container is deployed.

## Dependency
* Python >= 3.6
* Tensorflow >= 2.1.x
* quadprog >= 0.1.7
* numpy
* scikit-learn >= 0.22.2

## Run Example
```bash
$ docker build -t onlinedl/trainer:v01 \
               --build-arg MODEL_NAME=test ... \
                ${StreamDLServing}/online-dl/
$ docker run \
        -e MODEL_NAME=test \
        -e ONLINE_METHOD=cont \ 
        -e FRAMEWORK=keras  \
        -e SAVEWEIGHT=false \ 
        -e MEM_METHOD=cossim \ 
        -e NUM_AMI=1 \ 
        -e EPISODIC_MEM_SIZE=100 \
        -e IS_SCHEDULE=true \
        -e MODEL_REPO_ADDR={repoaddr:port} \
        -e RESULT_ADDR={resultaddr:port} \
        -e CEP_ID=cep_test \
        -e KAFKA_BK={kafkanode0:portnum},... \
        -e STREAM_BK={kafkanode0},... #  나중에 지우면 됩니다.
        -e BATCH_SIZE=32 \
        -e DTYPE=float32 \
        -e LB_SIZE=36 \
        -e LF_SIZE=1 \
        -e PREFIX=dlstream.ami \
        -e IS_ADAPTIVE=false \
    onlinedl/trainer:v01 \
    python3.6 online_trainer.py
```

## Required envrionment variable
#### ContinualDL with CossimMemory
```bash
$ docker run \
        -e MODEL_NAME={defined name by you}
        -e ONLINE_METHOD=cont
        -e MEM_METHOD=cossim
        -e NUM_AMI={number}
        -e EPISODIC_MEM_SIZE={number}
        -e IS_SCHEDULE=false or true
        -e MODEL_REPO_ADDR={address:port}
        -e RESULT_ADDR={resultaddr:port}
        -e CEP_ID={cep id from stream-parser}
        -e KAFKA_BK={address:port, ...}
        -e STREAM_BK={address, ...} # 나중에 지우면 됩니다.
        -e BATCH_SIZE={number}
        -e DTYPE={float32 or float64 or other else}
        -e LB_SIZE=36 \
        -e LF_SIZE=1 \
        -e PREFIX=dlstream.ami \
        (optional) -e FRAMEWORK=keras(developed) or tf(not yet developed)
        (optional) -e SAVEWEIGHT=false or true
        (optional) -e IS_ADAPTVIE=false or true
```

#### ContinualDL with ringbuffer
```bash
$ docker run \ 
        -e MODEL_NAME={defined name by you}
        -e ONLINE_METHOD=cont
        -e MEM_METHOD=ringbuffer
        -e MODEL_REPO_ADDR={address:port}
        -e RESULT_ADDR={resultaddr:port}
        -e KAFKA_BK={address:port, ...}
        -e STREAM_BK={address, ...} # 나중에 지우면 됩니다.
        -e BATCH_SIZE={number}
        -e DTYPE={float32 or float64 or other else}
        -e LB_SIZE=36 \
        -e LF_SIZE=1 \
        -e PREFIX=dlstream.ami \
        (optional) -e FRAMEWORK=keras(developed) or tf(not yet developed)
        (optional) -e SAVEWEIGHT=false or true
        (optional) -e IS_ADAPTVIE=false or true
```

#### IncrementalDL
```bash
$ docker run \
        -e MODEL_NAME={defined name by you}
        -e ONLINE_METHOD=inc
        -e MODEL_REPO_ADDR={address:port}
        -e RESULT_ADDR={resultaddr:port}
        -e CEP_ID={cep id from stream-parser}
        -e KAFKA_BK={address:port, ...}
        -e STREAM_BK={address, ...} # 나중에 지우면 됩니다.
        -e BATCH_SIZE={number} # TODO: this should be deprecated at IncrementalDL
        -e DTYPE={float32 or float64 or other else}
        -e LB_SIZE=36 \
        -e LF_SIZE=1 \
        -e PREFIX=dlstream.ami \
        (optional) -e FRAMEWORK=keras(developed) or tf(not yet developed)
        (optional) -e SAVEWEIGHT=false or true
```