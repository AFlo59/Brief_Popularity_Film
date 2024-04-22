#!/bin/bash

component=""
if [ -n $1 ]
then
component=$1
fi

clear
#sed -n p front/.env api/.env > .env
docker compose down
docker compose up $component --build --remove-orphans