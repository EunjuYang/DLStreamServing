# StreamDLServing Platform


### <img src="https://github.com/EunjuYang/DLStreamServing/blob/master/img/dlstreamServing_icon.png" alt="drawing" width="50"/>   StreamDLServing 



StreamDLServing platform provides serving environment to deploy deep learning models processing stream data. This platform can work with stream processing big-data platform, Apache Kafka. It supports trained model to be deployed supporting continual inference coming from kafka broker. Conceptual architecture is as follows.



<img align="center" src="https://github.com/EunjuYang/DLStreamServing/blob/master/img/dlstream_platform_overview.png"> 



## Pre-requisite

### Install Kubernetes

Our StreamDLServing splatform works on the kubernetes cluster. Firstly, build the kubernetes cluster on your environment. About building k8s cluster, please refers to [HERE](https://github.com/KAIST-NCL/Accelerator-K8S/wiki/How-to-make-a-k8s-cluster).



## Installation



### Setting system parameters

Please clone your repository to ${StreamDL_Home}

```
$ git clone https://github.com/EunjuYang/DLStreamServing.git
```

Edit `environment.conf` file to specify your configuration.

```
KAFKA_BK="{Your Kafka Broker Endpoint, IP:PORTNUM}"
STREAM_PREFIX="{Your Kafka Topic Prefix to be used for StreamDL Serving}"
PYTHONPATH=$PYTHONPATH:/opt/streamDL
```

Please edit `preset.sh` to satisfy your environment.

```
#!/bin/bash

export StreamDL_Home={Your StreamDL_Home DIR}
export KAFKA_BK={Your Kafka Broker Endpoint, IP:PORTNUM}
export STREAM_PREFIX={Your Kafka Topic Prefix to be used for StreamDL Serving}
export PYTHONPATH=$StreamDL_Home
export PATH=$PATH:$StreamDL_Home/streamDL_pyclient

```

Export the preset environment variables with the following command

```
$ chmod +x preset.sh
$ source preset.sh
```



### Install Platform

Please run this installation process on master node of kubernetes cluster, and your root should can call `kubectl` .

For installation, you can follow this command.

```
$ cd $StreamDL_Home/streamDL_daemon
$ chmod +x install.sh
$ ./install.sh
```



The installation process install following dependencies in root account

- kubernetes (python client library)
- pykafka (python client library)
- grpcio, grpcio-tools (python client library)



### Installation Test

To test the installation, you can use `streamDLctl` commandline client interface.

```
$ streamDLctl gert --streams

+--------------+-------------------------------------+
|  Name Space  |             Data Name               |
+--------------+-------------------------------------+
|   dlstream   |                 ami0                |
|   dlstream   |                 ami1                |
+--------------+-------------------------------------+
```



## Example Usage

streamDLServing platform provides two kindes of end-client: command line interface and dashboard. 



### Commandline Interface (streamDLctl)

#### get stream data information in Kafka

This command gets topics in Kafka, which are managable by this streamDLserving platform. It only searches topics with prefix that is predefined in the installation step. 

```
$ streamDLctl get --streams

+--------------+-------------------------------------+
|  Name Space  |             Data Name               |
+--------------+-------------------------------------+
|   dlstream   |                 ami0                |
|   dlstream   |                 ami1                |
+--------------+-------------------------------------+
```



#### get deployed model list

This command gets deployed model in this platform. For more information, you can use another option.

```bash
$ streamDLctl get --models
+--------------+-------------------------------------+-------+-----------------+
|     Name     |             Streams                 | Train |   Deployed At   |
+--------------+-------------------------------------+-------+-----------------+
+--------------+-------------------------------------+-------+-----------------+
```



#### Deploy trained model using stream data with online trainer

```bash
$ streamDLctl deploy --model_file /tmp/hello_model.h5 \
										 --model_name hello-test --amis ami0,ami1 \
										 --is_adaptive True --is_online_train True \
										 --look_back_win_size 3 --input_shift_step 1 \
										 --look_forward_step 1 --look_forward_win_size 1 \
										 --online_method cont --batch_size 32 --memory_method cossim \
										 --episodic_mem_size 100 --is_schedule True

$ streamDLctl get --models

+--------------+-------------------------------------+-------+-----------------+
|     Name     |             Streams                 | Train |   Deployed At   |
+--------------+-------------------------------------+-------+-----------------+
|  hello-test  |              ami0,ami1              |  True | 2020-05-08 22:27|
+--------------+-------------------------------------+-------+-----------------+
```

