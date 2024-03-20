# get image for loadbalancer
FROM haproxy:2.4-alpine

# Switch to root user to run apk commands 
USER root
COPY conf/haproxy.conf /etc/rsyslog.d/haproxy.conf
RUN apk update && apk add python3 rsyslog openrc && \
    rc-update add rsyslog default

# install python and syslog, Configure rsyslog to start at boot, Make the startup script executable
COPY scripts/startup.sh /usr/local/bin/startup.sh
RUN chmod +x /usr/local/bin/startup.sh

# copy source code
COPY conf/haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
COPY src/ /usr/local/src/

# Set the startup script as the entry point
ENTRYPOINT ["/usr/local/bin/startup.sh"]