#!/usr/bin/env python

import urllib
import atexit
import os
import socket
from threading import Thread
from subprocess import Popen
from flask import render_template
from flask import Flask, Response

# Allow us to reuse sockets after the are bound.
# http://stackoverflow.com/questions/25535975/release-python-flask-port-when-script-is-terminated
socket.socket._bind = socket.socket.bind
def my_socket_bind(self, *args, **kwargs):
    self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return socket.socket._bind(self, *args, **kwargs)
socket.socket.bind = my_socket_bind

def launch_mjpegserver():
    """
    Start gstreamer pipeline to launch mjpeg server.
    """
    mjpegserver = Popen(['gst-launch', 'v4l2src', 'device=/dev/video0', '!',
        'jpegenc', '!',
        'tcpserversink', 'port=5000', 'sync=false'])
    def mjpegserver_cleanup():
        mjpegserver.kill()
    atexit.register(mjpegserver_cleanup)

jpg = ''

def mjpegthread():
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

def launch_mjpegclient():
    """
    Launches a client for the mjpeg server that caches one
    jpeg at a time, globally.
    """
    t = Thread(target=mjpegthread)
    t.daemon = True
    t.start()

def launch_app():
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return render_template('index.html')

    @app.route("/jpeg")
    def jpeg_endpoint():
        return Response(jpg, mimetype='image/jpeg')

    print('Navigate to http://10.1.1.10:8080/');
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    launch_mjpegserver()
    launch_mjpegclient()
    launch_app()
