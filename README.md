Web front-end, REST api and (hopefully) GraphQL api for Keras. It will provide ability to build, train and monitor deep learning models (more at once due possibility to run multiple Keras "nodes").
It is still on POC stage so most of Keras functionalities are not covered and web ui is not extremely useful yet.  

# ow to run 
recommended way to run is to use docker containers.
first think to do is to set flask_host in config.yaml to current machie ip.
After that:
* mkdir -p data <- directory that will be use by MongoDb
* docker build -t deep_node -f DockerfileNode . (do it from main project directory)
* docker build -t deep_api -f DockerfileApi .  (do it from main project directory)
* docker build -t deep_dashboard . (do it from dashboard project directory)
* docker pull mongo && docker run -d -p 27017:27017 --name mongo_db -v data:/data/db mongo
* docker pull nats && docker run -d -p 4222:4222 -p 8222:8222 --name nats -V
* docker run -d -p 4001:4001 -e logs_port=4001 --name node deep_node <- it is possible to run multiple nods
* docker run -d -p 5000:5000 -p 4002:4002 -e logs_port=4002 --name api deep_api
* docker run -d -p 3000:3000 --name dashboard deep_dashboard

It wil run:
* Keras node (with logs available  on 4001 port)
* Rest api on port 5000 (with logs available  on 4002 port)
* Web font-end on port 3000
* MongoDB base on port 27017
* NATS message broker on port 4222 and monitoring on port 8222