# get image for loadbalancer
FROM haproxy:2.4-alpine
COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
# copy source code
COPY src/ /usr/local/src/

# Switch to root user to run apk commands 
USER root
# install python and pip
RUN apk update && apk add --no-cache python3 py3-pip