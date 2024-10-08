from http.server import SimpleHTTPRequestHandler, HTTPServer
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time
import socketserver
import os

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    routes = {}

    def do_GET(self):
        if self.path in self.routes:
            file_path = os.path.join(self.root_directory, self.routes[self.path])

            if os.path.exists(file_path):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_error(404, "File not found")
        else:
            self.send_error(404, "Path not found")

class MomwhyareyouhereWebsite:
    def __init__(self, port, root_directory):
        self.port = port
        self.root_directory = root_directory
        self.httpd = None

    def add_route(self, path, file_path):
        CustomHTTPRequestHandler.routes[path] = file_path

    def start_server(self):
        handler = CustomHTTPRequestHandler
        handler.root_directory = self.root_directory
        server_address = ('', self.port)
        self.httpd = HTTPServer(server_address, handler)
        print(f"Starting server on port {self.port}...")
        self.httpd.serve_forever()

    def stop_server(self):
        print("Stopping server...")
        if self.httpd:
            self.httpd.shutdown()