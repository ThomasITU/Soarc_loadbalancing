import http.server
import json
from urllib.parse import urlparse, parse_qs
from socketserver import ThreadingMixIn
import threading

class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query_params = parse_qs(urlparse(self.path).query)
        integer_arg = int(query_params.get('integer', [0])[0])
        
        # add random chance to stop server 
        # if random number < 0.95: stop
        # log server port stopped


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
        print(f"Stopping server on port {self.server.server_port}")
        self.server.shutdown()
        self.server.server_close()
