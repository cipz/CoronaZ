#!/bin/bash
 
clear

cat banner.txt

printf "\n"
printf "\nEdit run parameters parameters? [Y/n] "
read -r edit
arr=("y","n")

while [[ ! ${arr[*]} =~ ${edit,,} ]] 
do
    printf "\n"
    printf "\nNot a valid answer, please repeat."
    printf "\nEdit run parameters? [Y/n] "
    read -r edit
done

arr=("y")
if [[ ${arr[*]} =~ ${edit,,} ]]
then

    # Set all the params in both files
    # Get parameters in input

    printf "\n"
    printf "\nEditing run parameters "
    printf "\nfield_width (default 100): "
    read -r field_width
    printf "field_height (default 100): "
    read -r field_height
    printf "scale_factor (default 5): "
    read -r scale_factor
    printf "zombie_lifetime (default 120): "
    read -r zombie_lifetime
    printf "infection_radius (default 2): "
    read -r infection_radius
    printf "infection_cooldown (default 15): "
    read -r infection_cooldown

    # Setting default variables if the user didn't give anything in input
    field_width=${field_width:-100}
    field_height=${field_height:-100}
    scale_factor=${scale_factor:-5}
    zombie_lifetime=${zombie_lifetime:-120}
    infection_radius=${infection_radius:-2}
    infection_cooldown=${infection_cooldown:-15}
    
    jq  --arg key0 'field_width' \
        --argjson value0 $field_width \
        --arg key1 'field_height' \
        --argjson value1 $field_height \
        --arg key2 'scale_factor' \
        --argjson value2 $scale_factor \
        --arg key3 'zombie_lifetime' \
        --argjson value3 $zombie_lifetime \
        --arg key4 'infection_radius' \
        --argjson value4 $infection_radius \
        --arg key5 'infection_cooldown' \
        --argjson value5 $infection_cooldown \
        '. | .[$key0]=$value0 | .[$key1]=$value1 | .[$key2]=$value2 | .[$key3]=$value3 | .[$key4]=$value4 | .[$key5]=$value5' \
        <<<'{}'s \
        > tmp_config.json 2>/dev/null

        # cat tmp_config.json

        cp tmp_config.json coronaz-zombie/config.json
        cp tmp_config.json coronaz-frontend/config.json

        rm tmp_config.json

else

    # copy the default params in the params file

    printf "\n"
    printf "\nUsing default run parameters"
    printf "\n"
    cp default_config.json coronaz-zombie/config.json
    cp default_config.json coronaz-frontend/config.json

fi

printf "\nCreating docker network ... \n"
docker network create --gateway 172.16.1.1 --subnet 172.16.1.0/24 app_subnet

printf "\nBuilding coronaz-zombie image ... \n"
docker build coronaz-zombie --tag coronaz_node:latest

printf "\nGetting everything up and running in detached mode ... \n"
docker-compose up --build -d

infected_node_count=0
safe_node_count=0
total_node_count=0

printf "\n"
printf "\n"
printf "\nDatabase URL: http://localhost:8081/"
printf "\nFrontend app URL: http://localhost:3300/"
printf "\n"

end=false
while [ $end == "false" ]
do
    printf "\n"
    printf "\nMenu:"
    printf "\n1) Add 1 non-infected node"
    printf "\n2) Add 1 infected node"
    printf "\n3) Add X nodes"
    printf "\n0) Exit / Stop simulation"
    printf "\n"
    printf "\nWhat option do you want to execute? "
    read -r input

    case $input in
        1) printf "\nAdding 1 non-infected node\n"
            ((safe_node_count+=1))
            ((total_node_count+=1))
            docker run -d --net=host --name=coronaz_node_$total_node_count\_safe_$safe_node_count coronaz_node:latest
            ;;
        2) printf "\nAdd 1 infected node\n"
            ((infected_node_count+=1))
            ((total_node_count+=1))
            docker run -d --net=host -e RUN_ARGS="-i" --name=coronaz_node_$total_node_count\_infected_$infected_node_count coronaz_node:latest
            ;;
        3) printf "\nHow many non-infected nodes do you want to add? "
            read -r num_nodes
            for i in $(seq 1 $num_nodes)
            do
                ((safe_node_count+=1))
                ((total_node_count+=1))
                docker run -d --net=host --name=coronaz_node_$total_node_count\_safe_$safe_node_count coronaz_node:latest
            done
            printf "\n"
            printf "\nHow many infected nodes do you want to add? "
            read -r num_nodes
            for i in $(seq 1 $num_nodes)
            do
                ((infected_node_count+=1))
                ((total_node_count+=1))
                docker run -d --net=host -e RUN_ARGS="-i" --name=coronaz_node_$total_node_count\_infected_$infected_node_count coronaz_node:latest
            done
            ;;
        0) printf "\nExiting ... \n"
            end=true
            ;;
        *) printf "\nNot a valid input. Try again.\n"
            ;;
    esac
    sleep 1s
done

sleep 1s

printf "\n"
printf "\nStopping and removing the node containers ... \n"
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
printf "\n"
printf "\nStopping the docker-compose containers ... \n"
docker-compose down -v

exit 0