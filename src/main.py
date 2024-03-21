from server import SimpleHttpServerAdapter
import argparse
import config

def main():

    servers = [create_server(port) for port in range(config.start_port, config.start_port+config.number_of_servers)]
    for server in servers:
        if server:
            server.start(config.min_servers_up, config.chance_to_stop)

    _ = input()
    for server in servers:
        if server:
            server.stop()
    print("shutdown servers")
# Ease creating servers when servers are already running 
def create_server(port):
        try:
            return SimpleHttpServerAdapter(port)
        except Exception as e: # Catch any exception that might occur
            print(f"Error creating server on port {port}: {e}")
            return None # Return None or any other value to indicate failure

if __name__ == "__main__":

    # parse optional args
    parser = argparse.ArgumentParser(description='Process optional arguments for creating the servers.')
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

    main()




    
