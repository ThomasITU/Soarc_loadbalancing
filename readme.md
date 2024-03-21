# Load balancer Prototype

Simple load balancer to be used for prototyping

- Setup using Docker image HAProxy and python http server

## Prerequisites

- Docker

## Quickstart

builds, starts the container and spawns 4 servers, minimum 1 server available and a 1% crash probability

```cmd
quickstart.sh 4 1 0.01
```

## Start Loadbalancer

build the Docker image

```pwsh
docker build -t my-haproxy .
```

Validate the configuration file

```pwsh
docker run -it --rm --name haproxy-syntax-check my-haproxy haproxy -c -f /usr/local/etc/haproxy/haproxy.cfg
```

Run the Docker cotaniner starts the loadbalancer

```pwsh
docker run -d -p 8080:80 -p 8404:8404 --name my-running-haproxy --sysctl net.ipv4.ip_unprivileged_port_start=0 my-haproxy
```

### Start servers

From terminal

```pwsh
docker exec -it my-running-haproxy sh -c "python /usr/local/src/main.py -s <#no of servers> -m <minimum #no of servers to keep alive> -p <chance of server shutting down>"
docker exec -it my-running-haproxy sh -c "python /usr/local/src/main.py -s 10 -m 5 -p 0.01"

```

From inside the Docker container.

```sh
cd /usr/local/src/
```

```sh
python main.py -s -m -p         # <#no of servers> <minimum #no of servers to keep alive> <chance of server shutting down>
python main.py                  # default starts 1 server, minimum servers 1, probability of failure 0.01
python main.py -s 4             # starts 4 servers
```

### Spawn multiple clients

Spawn N simple clients accessing the endpoint <http://localhost:8080/?integer=42> with curl in asynchronous threads and writing to ***"logs/curl_output_clients_N.log"*** .

```pwsh
.\scripts\spawnClients.sh <N:default=100>
```

Spawn pythonClients accessing the endpoint <http://localhost:8080/?integer=21> with a resilient client, doing 3 retries, and writing to ***"logs/curl_output_clients_N.log"*** .

```pwsh
.\scripts\spawnPythonClients.sh <N:default=50>
```

### Access metrics WORK in progress

Logs are available in the Docker container /var/log/haproxy-traffic.log, maybe mount as volume?

More about the HAProxy logging and logging format [here](https://www.haproxy.com/blog/introduction-to-haproxy-logging).


Access loadbalancer stats from url <http://localhost:8404/> this can be exported to csv. - See the total column for # of succes/errors response ![Display of stats](imgs/Stats.png)

Explore more info about the HAProxy stats page [here](https://www.haproxy.com/blog/exploring-the-haproxy-stats-page).
