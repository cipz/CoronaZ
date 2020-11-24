# CoronaZ project as part of Distributed Systems 2020 at Helsinki University

## Instructions to start the project

The first step is to create a docker network with the command:

```
docker network create --gateway 172.16.1.1 --subnet 172.16.1.0/24 app_subnet
```

Then the next step is to build and start the containers with the command
```
docker-compose up --build
```
