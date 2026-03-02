#!/bin/bash

# run.sh

export $(grep -v '^#' .env | xargs)
envsubst < frontend/public/config.template.json > frontend/public/config.json

docker compose up --build
