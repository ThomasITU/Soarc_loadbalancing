# Load balancer Prototype

Simple load balancer to be used for prototyping 
- Setup using Docker image HAProxy and python http server

## Prerequisites

- Docker

## Quickstart with 4 servers

```cmd
quickstart.sh 4
```

## Start Loadbalancer

build the Docker image

```pwsh
docker build -t my-haproxy .
```

Check the configuration file

```pwsh
docker run -it --rm --name haproxy-syntax-check my-haproxy haproxy -c -f /usr/local/etc/haproxy/haproxy.cfg
```

Run the Docker cotaniner starts the loadbalancer

```pwsh
docker run -d -p 8080:80 --name my-running-haproxy --sysctl net.ipv4.ip_unprivileged_port_start=0 my-haproxy
```

Access loadbalancer stats doesn't work yet

<localhost:8080/haproxy?stats>

### Start servers

From terminal

```pwsh
docker exec -it my-running-haproxy sh -c "python /usr/local/src/main.py -s <number of servers>"
```

From inside the docker container ensure in the right directory.

```sh
cd /usr/local/src/
```

```sh
python main.py -s               <#no of servers>
python main.py                  # starts 1 server
python main.py -s 4             # starts 4 servers
```

### Spawn multiple clients WORK in progress


Endpoint is a accessible on <http://localhost:8080/?integer=42>

```pwsh
curl <http://localhost:8080/?integer=42>
```

### Access metrics WORK in progress
