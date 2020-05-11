# test-mongo
## Description
Using Dockerfile, it continuously create data in mongodb, which will be read in Dashboard.   

## RUN EXAMPLE
First you need to run mongo docker image like below. ($CONTAINER_NAME is a user-defined var)
```bash
$ docker run -d --name $CONTAINER_NAME mongo:4.2
```   
Then you need to run "docker build" to make generator-image.
```bash
$ docker build -t createdata:0.1 \
    --build-arg USERNAME=${GITHUB_USERNAME} \ 
    --build-arg PASSWORD=${GITHUB_PASSWORD} \ 
    --build-arg NAME=${MODEL_NAME} \
    --build-arg MONGO_PORT_27017_TCP_ADDR=$MONGO_PORT_27017_TCP_ADDR \
    --build-arg MONGO_PORT_27017_TCP_PORT=$MONGO_PORT_27017_TCP_PORT .
(example)
$ docker build -t createdata:0.1 \
    --build-arg USERNAME=iop851 \
    --build-arg PASSWORD=... \
    --build-arg NAME=prediction_model1 \
    --build-arg MONGO_PORT_27017_TCP_ADDR=192.168.54.129 \
    --build-arg MONGO_PORT_27017_TCP_PORT=27017 .
```
Finally, run "docker run" to create data.
```bash
$ docker run -d createdata:0.1 
```
## MongoDB and Data Description
Database: 'inference'   
Collection: ${MODEL_NAME} defined at 'docker build'
```bash
Data: { 'amiid': 0 ~ 4, # an integer
    'pred': [value 0, value 1, ..., value N], # list and N is varying
    'true': [value 0, value 1, ..., value N], # list and N is varying
    'timestamp': value # an integer from time.time()
}
```