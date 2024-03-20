import http.server
import json
from urllib.parse import urlparse, parse_qs
from socketserver import BaseServer, ThreadingMixIn
import threading
import random

CHANCE_TO_STOP = 0.1 # 10%

class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query_params = parse_qs(urlparse(self.path).query)
        integer_arg = int(query_params.get('integer', [0])[0])
        
        if random.random() < CHANCE_TO_STOP: 
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
       

    def start(self):
        print(f"Starting server on port {self.server.server_port}")
        thread = threading.Thread(target=self.server.serve_forever)
        thread.start()

    def stop(self):
        stop(self.server)

def stop(server:ThreadingHTTPServer):
    print(f"Stopping server on port {server.server_port}")
    server.shutdown()
    server.server_close()
