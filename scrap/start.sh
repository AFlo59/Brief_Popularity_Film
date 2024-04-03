#!/bin/bash
clear
#sed -n p front/.env api/.env > .env
docker compose down
docker compose up --build --remove-orphans