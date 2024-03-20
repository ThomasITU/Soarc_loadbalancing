import http.server
import json
from urllib.parse import urlparse, parse_qs
from socketserver import ThreadingMixIn
import threading
import random
import config


CHANCE_TO_STOP = config.chance_to_stop
MIN_SERVERS_UP = config.min_servers_up

# Create a lock for synchronizing access to servers_running
servers_running = 0 
servers_running_lock = threading.Lock()

class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query_params = parse_qs(urlparse(self.path).query)
        integer_arg = int(query_params.get('integer', [0])[0])
        
        global servers_running
        servers_running = servers_running
        if random.random() < CHANCE_TO_STOP and servers_running > MIN_SERVERS_UP:
            stop(self.server)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            "success": True,
            "integer": integer_arg*2
        }
        self.wfile.write(json.dumps(response).encode())

class ThreadingHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

class SimpleHttpServerAdapter:
    def __init__(self, port):
        self.server = ThreadingHTTPServer(("localhost", port), MyRequestHandler)
       
    def start(self, min_servers_up, chance_to_stop):
        print(f"Starting server on port {self.server.server_port}")
        thread = threading.Thread(target=self.server.serve_forever)
        
        # set global variables  
        global MIN_SERVERS_UP
        global CHANCE_TO_STOP
        MIN_SERVERS_UP = min_servers_up 
        CHANCE_TO_STOP = chance_to_stop
        thread.start()
        with servers_running_lock:
            global servers_running 
            servers_running += 1 # Increment the count of running servers

    def stop(self):
        stop(self.server)

def stop(server:ThreadingHTTPServer):
    print(f"Stopping server on port {server.server_port}")
    server.shutdown()
    server.server_close()
    with servers_running_lock:
        global servers_running 
        servers_running -= 1 # Decrement the count of running servers
