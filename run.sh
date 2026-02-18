#!/bin/bash

# run.sh

SERVICE_API_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
export SERVICE_API_KEY

docker compose up --build
