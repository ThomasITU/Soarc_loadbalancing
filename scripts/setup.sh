# Create a Docker network
docker network create haproxy-net

# Run InfluxDB container
docker run -d --name=influxdb --network=haproxy-net -p 8086:8086 influxdb

# Run Telegraf container (assuming you have a custom Telegraf configuration file)
docker run -d --name=telegraf --network=haproxy-net telegraf
docker cp conf/telegraf.conf telegraf:/etc/telegraf/telegraf.conf

docker network inspect haproxy-net 