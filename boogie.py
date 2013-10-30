from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import time
import urlparse
import os
import argparse
import base64
import socket
import json
import fnmatch

""" Boogie, one file pure Python implementation of basic HTTP server acting as remote resource.

Using Boogie server, you can test how your application behaves when some HTTP connection trouble appears.
For example, if you want to test long-time answear from remote HTTP server, you can send request to
Boogie with parameter sleep /?sleep=10 and server will respond with 10 seconds delay.

"""

class RequestWrapper(object):
    """ Handler wrapper. Adds more functions to basic BaseHTTPRequestHandler

    """
    parameters = None

    def parse_json_config(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def parse_parameters(self):
        if self.config:
            params = self.parse_json_config(self.config)
            if 'default' in params.keys():
                self.parameters = params['default']
            for path, parameters in params.iteritems():
                if fnmatch.fnmatch(self.path, path):
                    self.parameters = parameters

            print self.parameters
        else:
            """ Normalize query string into one-dimension dictionary without duplicate values """
            self.parameters = {k: v[-1] for k,v in urlparse.parse_qs(urlparse.urlparse(self.path).query).iteritems}

    def get_parameter(self, name, default):
        if not self.parameters:
            self.parse_parameters()
        if name not in self.parameters:
            return default
        return self.parameters[name]


class Handler(BaseHTTPRequestHandler, RequestWrapper):

    """ Base request handler. Handles requests accodring to params in QueryString

    """
    def do_GET(self):
        if self.observe:
            self.parse_parameters
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

def is_file(arg):
    if not os.path.exists(arg):
        raise argparse.ArgumentError("File %s does not exist"%arg)
    return arg


if __name__ == '__main__':
    arg_p = argparse.ArgumentParser()
    arg_p.add_argument("-p", "--port", help="Listen port (default 8080)", type=int, default=8080)
    arg_p.add_argument("-l", "--bind-address",  help="Bind address (default localhost)", default="localhost")
    arg_p.add_argument("-c", "--config",  help="Pre-configure response mode. Using this, you can act as a real resouce, without needing to change any URLs in your app.", type=is_file, metavar="FILE")
    arg_p.add_argument("-o", "--observe-config",  help="Parse config during every request. (--config required)", action='store_true')
    args = arg_p.parse_args()
    if args.observe_config and not args.config:
        arg_p.error("No config file specified")
    server = ThreadedHTTPServer((args.bind_address, args.port), Handler)
    server.RequestHandlerClass.config = args.config
    server.RequestHandlerClass.observe = args.observe_config
    print "Starting server on %s:%s, use <Ctrl-C> to stop"%(args.bind_address, args.port)
    server.serve_forever()
