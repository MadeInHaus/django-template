#!/bin/bash

pids=""

function ctrl_c() {
    echo "** Trapped CTRL-C"
    docker-compose -f docker-compose.dev.yml stop || true

    if [ -n "$pids" ]
    then
        kill -- $pids
    fi

    pkill -f docker-osx-dev

    exit $?
}

CURRENT_DIR=${PWD##*/}
dockerName=${CURRENT_DIR//[^a-zA-Z0-9]/}
webContainerName="${dockerName}_web"

WEB_CONTAINER=""

function getWebContainer(){
    WEB_CONTAINER=$(docker ps -a | grep -Eo "$webContainerName[^ ]+") || true
}

function install_notification_server() {
    hash terminal-notifier &> /dev/null
    if [ $? -eq 1 ]; then
        echo "terminal-notifier not installed, installing now"
        brew install terminal-notifier
    fi

    hash notify-send-server &> /dev/null
    if [ $? -eq 1 ]; then
        echo "notify-send-server not installed, installing now"
        curl -L https://github.com/fgrehm/notify-send-http/releases/download/v0.2.0/server-darwin_amd64 > /usr/local/bin/notify-send-server
        chmod +x /usr/local/bin/notify-send-server
    fi
}

USE_BOOT2DOCKER=false

while [[ $# > 0 ]]
do
key="$1"

case $key in
    -b|--boot2docker)
    USE_BOOT2DOCKER=true
    ;;
    *)
            # unknown option
    ;;
esac
shift # past argument or value
done

if [ "$USE_BOOT2DOCKER" = true ]; then
    boot2docker up
    eval "$(boot2docker shellinit)"

else
    docker-machine start default || true
    eval "$(docker-machine env default)"
fi

# Skip Dependencies isn't supported in older versions
install_notification_server
docker-osx-dev install --skip-dependencies || docker-osx-dev install
pkill -f docker-osx-dev || true

docker-compose  -p "$dockerName" -f docker-compose.dev.yml stop || true

docker-compose -p "$dockerName" -f docker-compose.dev.yml build web

trap ctrl_c SIGINT SIGTERM INT TERM ERR

docker-osx-dev sync-only -c docker-compose.dev.yml || true

docker-osx-dev -c docker-compose.dev.yml | sed "s/$/$(printf '\r')/" &
pids="$pids $!"

PORT=12345 notify-send-server &
pids="$pids $!"

docker-compose -p "$dockerName" -f docker-compose.dev.yml run --rm --service-ports web

ctrl_c
