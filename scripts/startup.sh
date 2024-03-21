#!/bin/sh

# Start HAProxy in the background
haproxy -f /usr/local/etc/haproxy/haproxy.cfg &

# Start rsyslog in the background
rsyslogd -n &

# Wait for all background processes to complete
wait