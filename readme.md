# StreamDLServing Platform

This repository contains source code to support deep learning-based stream event processing. 
It receives "registration" for a DL model as CEP-rule and its input specification.


### Dependencies

* python 3.6 >=
* grpc

For the stream cluster side  
We recomend you to use conda to manage package dependencies.


```bash
$ pip install grpcio protobuf grpcio-tools
```

```bash
$ pip install confluent-kafka
```
```bash
$ pip install pandas
```

### Our clusters
UCluster is built as follows. 
CEP cluster is coordinated by Kubernetes and all deep learning model for complex event processing is running with container.
Stream cluster manages all stream-related routing function. Especially, stream input multiplexing for deep learning inferencing is conducted in stream cluster side.
Stream cluster contains zookeeper & Kafka & Spark (not determined).

| Cluster           | CEP Cluster   | StreamCluster|
| :----------------:|:------------: |:------------:|
| Server Information| cep-node0     | stream-node0 |
|                   | cep-node1     | stream-node1 |
|                   |               | stream-node2 |

### How to install


#### DL-based CEP Service Daemon (streamDL daemon)

Install this daemon in master node of CEP service cluster. It will communicate with client (Dashboard) and Stream daemon running on stream cluster.

all program for dl-based CEP broker is written under `daemon` folder.
Please install all dependencies. Update `install.sh` file, 
especially don't forget to update the `python path` which includes `grpc`. The `python path` should be include interpreter version higher than 3.6.

It should be installed on a master node of CEP cluster.

```bash
$ ./install.sh
```

Running install shell script automatically set daemon process.
For uninstall, please execute `uninstall.sh` shell script.


#### Stream Daemon (streamBroker daemon)

all program for dl-based CEP broker is written under `daemon` folder.
Please install all dependencies. Update `install.sh` file, 
especially don't forget to update the `python path` which includes `grpc`.

It should be installed on a master node of Stream Cluster

```bash
stream-node0$ ./install.sh
```

Running install shell script automatically set daemon process.
For uninstall, please execute `uninstall.sh` shell script.
