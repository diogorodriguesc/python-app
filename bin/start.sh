#!/usr/bin/env bash

DIR=$(dirname "$0")
cd $DIR/..

environments=(dev test prod)

if [ -z "$1" ]
  then
    echo "No argument environment supplied: ${environments[@]}"
    exit 1
fi

sh bin/stop.sh

mkdir -p var/logs && touch var/logs/docker.log

nohup docker-compose -f docker/docker-compose.yml up > var/logs/docker.log 2>&1 &
PID=$!

echo "Docker-compose was started on $PID pid..."

python3 main.py $1
