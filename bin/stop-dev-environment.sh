#!/usr/bin/env bash

DIR=$(dirname "$0")
cd $DIR/..

docker-compose -f docker/docker-compose.yml down
