#!/bin/bash

# Number of clients to spawn default 100
N=${1:-100}

# Endpoint URL
URL="http://localhost:8080/?integer=42"

# PARENT_DIR=$(dirname "$PWD")
LOG_FILE="logs/curl_output_clients_$N.log"

# Use xargs to execute curl commands in parallel
seq $N | xargs -I {} -P $N curl -s -w "\n" $URL >> $LOG_FILE
