#!/bin/bash

component=""
if [ -n $1 ]
then
component=$1
fi

clear
docker compose -f compose.prod.yml down
docker compose -f compose.prod.yml up $component --build 