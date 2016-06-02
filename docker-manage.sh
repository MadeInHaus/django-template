#!/bin/bash

CURRENT_DIR=${PWD##*/}
dockerName=${CURRENT_DIR//[^a-zA-Z0-9]/}

echo "Running \`python ./manage.py $*\` on web container for $dockerName"
eval "$(docker-machine env default)"
eval "docker-compose -p $dockerName -f docker-compose.dev.yml run web python ./manage.py $*"
