from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import time
import urlparse
import os
import argparse
import base64
import socket



""" Boogie, one file pure Python implementation of basic HTTP server acting as remote resource.

Using Boogie server, you can test how your application behaves when some HTTP connection trouble appears.
For example, if you want to test long-time answear from remote HTTP server, you can send request to
Boogie with parameter sleep /?sleep=10 and server will respond with 10 seconds delay.

"""

class RequestWrapper:
    """ Handler wrapper. Adds more functions to basic BaseHTTPRequestHandler

    """

    parameters = None

    def parse_parameters(self):
        self.parameters = urlparse.parse_qs(urlparse.urlparse(self.path).query)

    def get_parameter(self, name, default):
        if not self.parameters:
            self.parse_parameters()
        if name not in self.parameters:
            return default
        return self.parameters[name][-1]


class Handler(BaseHTTPRequestHandler, RequestWrapper):

    """ Base request handler. Handles requests accodring to params in QueryString

    """

    def do_GET(self):
        ret_code = int(self.get_parameter('code', 200))
        sleep_time = int(self.get_parameter('sleep', 0))
        time.sleep(sleep_time)
        self.send_response(ret_code)
        if self.get_parameter('slowconn', False):
            size_of_data = int(self.get_parameter('size', 10))*1024
            self.send_header('Content-Length', size_of_data)
        self.end_headers()
        if self.get_parameter('slowconn', False):
            size_of_data = int(self.get_parameter('size', 10)*1024)
            transfer_in_kbps = int(self.get_parameter('rate', 1))
            data_transfered = 0
            interval = 0.1
            while data_transfered < size_of_data:
                size_to_gen = int(transfer_in_kbps*1024*interval)
                data = os.urandom(int(transfer_in_kbps*1024*interval))
                self.wfile.write(data + '0\r\n\r\n')
                data_transfered += len(data)
                print data_transfered
                time.sleep(interval)
        elif self.get_parameter('ret_data', False):
            message =  threading.currentThread().getName()
            self.wfile.write("<html><body>Default return data for GET on %s with HTTP return code: %s</body></html>"%(self.path, ret_code))
            self.wfile.write('\n')
        return

    def do_POST(self):
        ret_code = int(self.get_parameter('code', 200))
        sleep_time = int(self.get_parameter('sleep', 0))
        time.sleep(sleep_time)
        self.send_response(ret_code)
        self.end_headers()
        if self.get_parameter('ret_data', False):
            message =  threading.currentThread().getName()
            self.wfile.write("<html><body>Default return data for POST on %s with HTTP return code: %s</body></html>"%(self.path, ret_code))
            self.wfile.write('\n')
        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    arg_p = argparse.ArgumentParser()
    arg_p.add_argument("-p", "--port", help="Listen port (default 8080)", type=int, default=8080)
    arg_p.add_argument("-l", "--bind-address",  help="Bind address (default localhost)", default="localhost")
    args = arg_p.parse_args()
    server = ThreadedHTTPServer((args.bind_address, args.port), Handler)
    print "Starting server on %s:%s, use <Ctrl-C> to stop"%(args.bind_address, args.port)
    server.serve_forever()
