#!/bin/bash

CURRENT_DIR=${PWD##*/} dockerName=${CURRENT_DIR//[^a-zA-Z0-9]/}
containerId=$(docker ps -a | grep "${dockerName}_web" | awk '{ print $1 }')

echo "Running \`python ./manage.py $*\` on backend container [${containerId}] for $dockerName"
eval "docker exec -it $containerId ./wait-for-it.sh db:5432 -- python ./manage.py $*"
