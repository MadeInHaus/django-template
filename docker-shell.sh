#!/bin/bash

CURRENT_DIR=${PWD##*/}
dockerName=${CURRENT_DIR//[^a-zA-Z0-9]/}
containerId=$(docker ps -a | grep "${dockerName}_web" | awk '{ print $1 }')

if [ -n "$containerId" ]; then
    eval "docker exec -it $containerId /bin/bash"
else
    echo "No $container container found."
fi
