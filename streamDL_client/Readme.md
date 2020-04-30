# StreamDL client

streamDL broker에 전달하기 위한 client 프로그램.

## Install

### gRPC (c++)

- Setup

설치 위치는 $HOME/local로 지정

```bash
$ export MY_INSTALL_DIR=$HOME/local
```

폴더 생성

```bash
$ mkdir -p $MY_INSTALL_DIR
```

해당 설치 directory 밑의 bin 폴더를 환경변수에 포함.

```bash
$ export PATH="$PATH:$MY_INSTALL_DIR/bin"
```



- cmake 설치 (cmake 버전은 3.13 이상)

```bash
$ export PATH="$PATH:$MY_INSTALL_DIR/bin"
```

- gRPC 기본 툴 설치

```sh
$ sudo apt install -y build-essential autoconf libtool pkg-config
```

- gRPC repo 복제

```bash
$ git clone --recurse-submodules -b v1.28.1 https://github.com/grpc/grpc
$ cd grpc
```

- gRPC 빌드 & 설치

```bash
$ mkdir -p cmake/build
$ pushd cmake/build
$ cmake -DgRPC_INSTALL=ON \
      -DgRPC_BUILD_TESTS=OFF \
      -DCMAKE_INSTALL_PREFIX=$MY_INSTALL_DIR \
      ../..
$ make -j
$ make install
$ popd
```

