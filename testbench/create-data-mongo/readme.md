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
    --build-arg USERNAME=$USERNAME \ 
    --build-arg PASSWORD=$PASSWORD 
    --build-arg NAME=$NAME .
```
Finally, run "docker run" to create data.
```bash
$ docker run -d --link $CONTAINER_NAME:$CONTAINER_NAME createdata:0.1 
```
## MongoDB and Data Description
Database: 'inference'   
```bash
Data: { 'amiid': 0 ~ 4, # an integer
    'pred': [value 0, value 1, ..., value N], # list and N is varying
    'true': [value 0, value 1, ..., value N], # list and N is varying
    'timestamp': value # an integer from time.time()
}
```