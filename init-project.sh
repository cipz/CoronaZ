#!/bin/bash

echo "Creating docker network ... "
docker network create --gateway 172.16.1.1 --subnet 172.16.1.0/24 app_subnet

echo "Building coronaz-zombie image ... "
docker build coronaz-zombie --tag coronaz_node:latest

echo "Getting everything up and running in detached mode ... "
docker-compose up --build -d

node_count=0

end=false
while ! $end
do
    echo "Menu:"
    echo "1) Add 1 node"
    echo "2) Add X nodes"
    echo "0) Exit"

    echo "What option do you want to execute? "

    read input
    case $input in
        1) echo "Adding 1 node"
            ((node_count+=1))
            echo $node_count
            docker run -d --net=host --name=coronaz_node_$node_count coronaz_node:latest 
            ;;
        2) echo "How many nodes do you want to add?"
            read num_nodes
            for i in $(seq 1 $num_nodes)
            do
                ((node_count+=1))
                docker run -d --net=host --name=coronaz_node_$node_count coronaz_node:latest 
            done
            ;;
        0) echo "Exiting ... "
            end=true
            ;;
        *) echo "Not a valid input. Try again."
            continue
            ;;
    esac
done

echo "Stopping everything ... "
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker-compose down -v