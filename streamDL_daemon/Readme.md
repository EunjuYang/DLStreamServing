# Daemon



## Pre-requisites

### Install Kubernetes

쿠버네티스 마스터 노드에 설치한다고 가정합니다.



## Installation

### gRPC

gRPC should installed in global 

```bash
sudo pip install grpc
```





### Kubernetes Python Client

python client 라이브러리 설치. 

```bash
pip install kubernetes
```

Python client 사용 예제 [[git](https://github.com/kubernetes-client/python/tree/master/examples)]



## Daemon Server-Client Interface

gRPC로 interface API를 제공합니다. 자세한 interface는 [streamDL.proto](https://github.com/EunjuYang/DLStreamServing/tree/master/streamDL_daemon/proto/streamDL.proto)를 참고해주세용 :)



|               Function Prototype                |                   Description                   |
| :---------------------------------------------: | :---------------------------------------------: |
|  deploy_model(stream Model) returns (Reply) {}  |           모델 배포, 파일 stream 전달           |
| is_deployed_model(ModelName) returns (Reply) {} | 동일한 모델 이름을 가지는 배포 있는지 여부 확인 |
|   set_input_fmt(ModelInfo) returns (Reply) {}   |                    입력 모델                    |
| get_stream_list(null) returns (KafkaTopics) {}  |         Kafka broker topic 리스트 조회          |

```
    rpc deploy_model(stream Model) returns (Reply) {}
    rpc is_deployed_model(ModelName) returns (Reply) {}
    rpc set_input(ModelInfo) returns (Reply) {}
    rpc get_stream_list(null) returns (KafkaTopics) {}
```



#### Deploy with onlineDL



**(COMMON) Deploy witohout onlineDL**

* 모델 파일 업로드
* [string] model_name

- [bool] is_adaptive

- [list] amis

- input format

  ```
  int32 look_back_win_size
  int32 input_shift_step 
  ```

  -------------------------------------

  **Online DL 용 parameter**

- input format

  ```bash
  (online training) int32 look_forward_step 
  (online training) int32 look_forward_win_size 
  ```

  [선택] online_method (cont / inc)

- batch_size

- [선택] (only for cont) memory_method (ring buffer / cossim)

- [int] (only for cont) episodic_mem_size

- [bool] (onlyb for cont) is_schedule

