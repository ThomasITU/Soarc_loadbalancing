#!/bin/bash

# Number of clients to spawn default 50
N=${1:-50}
ADDRESS=${2:-"localhost"}
LOG_FILE="logs/curl_output_clients_$N.log"

# Use xargs to execute curl commands in parallel
seq $N | xargs -I {} -P $N python src/client.py -a $ADDRESS >> $LOG_FILE 
