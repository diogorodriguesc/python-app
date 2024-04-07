#!/usr/bin/env bash

DIR=$(dirname "$0")
cd $DIR/..

until nc -z -v -w30 database 5432 > /dev/null
do
  echo "Waiting for database connection..."

  sleep 5
done

echo "Running Migrations..."
python3 console.py run_migrations
