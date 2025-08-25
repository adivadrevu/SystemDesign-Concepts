import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client
import itertools
import time

# Define backend server ports and responses
BACKEND_PORTS = [8001, 8002]
BACKEND_RESPONSES = [
    "<h1 style='color:red;'>Red Server - Server 1</h1>",
    "<h1 style='color:blue;'>Blue Server - Server 2</h1>"
]

# Factory function to create a custom handler for each backend
def create_backend_handler(response_body):
    class CustomBackendHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response_body.encode())

        def log_message(self, format, *args):
            # Silence backend logging for clarity
            return
    return CustomBackendHandler

# Start backend servers in threads
def start_backend_server(port, response_body):
    handler_class = create_backend_handler(response_body)
    server = HTTPServer(('localhost', port), handler_class)
    print(f"[Backend] Server started at http://localhost:{port}")
    server.serve_forever()

# Backend addresses for load balancer
BACKENDS = [("localhost", port) for port in BACKEND_PORTS]
backend_iterator = itertools.cycle(BACKENDS)

# Load Balancer handler
class LoadBalancerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Filter favicon.ico to avoid confusion
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        # Pick backend in round-robin
        target_host, target_port = next(backend_iterator)
        print(f"[LoadBalancer] Routing path '{self.path}' to http://{target_host}:{target_port}")

        try:
            conn = http.client.HTTPConnection(target_host, target_port)
            conn.request("GET", self.path)
            response = conn.getresponse()

            self.send_response(response.status)
            for header, value in response.getheaders():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response.read())
            conn.close()
        except Exception as e:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(f"Bad Gateway: {e}".encode())

    def log_message(self, format, *args):
        # Silence load balancer access logs for clarity
        return

# Start the load balancer
def start_load_balancer(port=9000):
    server = HTTPServer(('localhost', port), LoadBalancerHandler)
    print(f"[LoadBalancer] Running at http://localhost:{port}")
    server.serve_forever()

# Run everything
if __name__ == "__main__":
    # Start backend servers
    for port, content in zip(BACKEND_PORTS, BACKEND_RESPONSES):
        t = threading.Thread(target=start_backend_server, args=(port, content), daemon=True)
        t.start()
        time.sleep(0.5)  # Stagger startup

    # Start load balancer
    start_load_balancer()
