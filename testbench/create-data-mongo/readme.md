# test-mongo
## Description
Using Dockerfile, it continuously create data in mongodb, which will be read in Dashboard.   

## Prerequisite
First you need to run mongo docker image like below.
```bash
$ docker run -d --name mongo mongo:4.2
```
Check mongo image is running like below   
Then you need to run "docker build" to create data.
```bash
$ docker build -t createdata:0.1 
```