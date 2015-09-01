import urllib 

# gst-launch-1.0 avfvideosrc ! jpegenc ! tcpserversink port=5000 sync=false

jpg = ''

def mjpeg_thread():
    global jpg
    while True:
        try:
            stream=urllib.urlopen('http://localhost:5000/')
            bytes=''
            while True:
                bytes += stream.read(1024)
                a = bytes.find('\xff\xd8')
                b = bytes.find('\xff\xd9')
                if a!=-1 and b!=-1:
                    jpg = bytes[a:b+2]
                    bytes= bytes[b+2:]
        except:
            try:
                stream.close()
            except:
                pass

from threading import Thread 

Thread(target=mjpeg_thread).start()

#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer
from subprocess import Popen
import os

# os.chdir(os.path.join(os.path.dirname(__file__), 'static'))

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'image/jpeg')
        self.end_headers()

        self.wfile.write(jpg)
        self.wfile.close()
        # return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0', 8080), Handler)

import socket
server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.serve_forever()