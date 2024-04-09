#!/usr/bin/env bash

DIR=$(dirname "$0")
cd $DIR

environments=(dev test)

if [ -z "$1" ]
then
    echo "No argument environment supplied. Choose one of: ${environments[@]}"
    exit 1
fi

if ! printf '%s\0' "${environments[@]}" | grep -Fxqz -- $1 ; then
    echo "Invalid environment supplied. Choose one of: ${environments[@]}"
    exit 1
fi

sh stop-dev-environment.sh

file="$(date '+%Y-%m-%d_%H-%M').log"
logFileRelPath="docker/var/logs/$file"
mkdir -p docker/var/logs && touch $logFileRelPath

nohup docker-compose -f docker/docker-compose.yml up --build > $logFileRelPath 2>&1 &
PID=$!
echo "Docker-compose was started on $PID pid..."
