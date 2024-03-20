#!/bin/bash
SERVERS=${1:-4}

# Build the Docker image
docker build -t my-haproxy .

# Run the HAProxy container
docker run -d -p 8080:80 -p 8404:8404 --name my-running-haproxy --sysctl net.ipv4.ip_unprivileged_port_start=0 my-haproxy

# Execute a command in a running container
docker exec -it my-running-haproxy sh -c "python /usr/local/src/main.py -s $SERVERS"
