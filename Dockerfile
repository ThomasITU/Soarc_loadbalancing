# get image for loadbalancer
FROM haproxy:2.4-alpine
COPY conf/haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
COPY conf/haproxy.conf /etc/rsyslog.d/haproxy.conf
# copy source code and startup script
COPY src/ /usr/local/src/
COPY scripts/startup.sh /usr/local/bin/startup.sh

# Switch to root user to run apk commands 
USER root

# install python and syslog, Configure rsyslog to start at boot, Make the startup script executable
RUN apk update && apk add --no-cache python3 rsyslog openrc && \
    rc-update add rsyslog default && \
    chmod +x /usr/local/bin/startup.sh

# Set the startup script as the entry point
ENTRYPOINT ["/usr/local/bin/startup.sh"]