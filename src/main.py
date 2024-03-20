from server import SimpleHttpServerAdapter
import argparse

# define port range and number of servers
PORT_START = 8000
NUMBER_OF_SERVERS = 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process optional flag for amount of servers.')
    parser.add_argument('-s', type=int, help='An optional integer for amount of servers', dest='server')
    args = parser.parse_args()
    
    if args.server is not None:
        NUMBER_OF_SERVERS = args.server

    servers = [SimpleHttpServerAdapter(port) for port in range(PORT_START, PORT_START+NUMBER_OF_SERVERS)]
    for server in servers:
        server.start()

    print(f"servers are running: type anything to shut down")
    wait = input()
    for server in servers:
        server.stop()
    print("shutdown servers")
