# get image for loadbalancer
FROM haproxy:2.4-alpine

# copy source code
COPY conf/haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
COPY src/ /usr/local/src/
COPY scripts/startup.sh /usr/local/bin/startup.sh
COPY conf/haproxy.conf /etc/rsyslog.d/haproxy.conf

# Switch to root user to run apk commands 
USER root

# install python and syslog, Configure rsyslog to start at boot,
RUN apk update && apk add --no-cache bash python3 rsyslog openrc socat && \
    rc-update add rsyslog default

#  Make the startup script executable
RUN chmod +x /usr/local/bin/startup.sh

# Set the startup script as the entry point
ENTRYPOINT [ "/usr/local/bin/startup.sh" ]
# CMD ["/bin/bash" "-c" "/usr/local/bin/startup.sh"]
