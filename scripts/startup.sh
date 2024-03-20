#!/bin/sh

# Start rsyslog in the background
rsyslogd -n &

# Start HAProxy in the background
haproxy -f /usr/local/etc/haproxy/haproxy.cfg &

# Wait for all background processes to complete
wait


# restart syslog
# rc-service rsyslog stop
# rm -f /var/run/rsyslogd.pid
# rsyslogd -n &
