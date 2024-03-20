from server import SimpleHttpServerAdapter
import argparse
import config

# define port range
PORT_START = 8000

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process optional flag for amount of servers.')
    parser.add_argument('-s', type=int, help='An optional for amount of servers default = 1', dest='servers')
    parser.add_argument('-m', type=int, help='An optional for minimum amount of servers default = 1', dest='min_servers')
    parser.add_argument('-p', type=float, help='Probability of server shutdown as float default = 0.01', dest='probability')

    args = parser.parse_args()
    
    if args.servers is not None:
        config.number_of_servers = args.servers
    if args.min_servers is not None:
        config.min_servers_up = args.min_servers
    if args.probability is not None:
        config.chance_to_stop = args.probability


    servers = [SimpleHttpServerAdapter(port) for port in range(PORT_START, PORT_START+config.number_of_servers)]
    for server in servers:
        server.start()

    print(f"servers are running: type anything to shut down")
    wait = input()
    for server in servers:
        server.stop()
    print("shutdown servers")
