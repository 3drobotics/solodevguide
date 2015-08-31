# Stillframe Photo API

<aside class="note">
To run this example, run `solo-utils video-splice` first to get camera access.
</aside>

<aside class="alert">
This example is being rewritten to use MJPEG streaming for purely in-memory image access and Flask.
</aside>

This example provides a RESTful API on port :8080 that can be accessed from Solo. When the HTTP endpoint is hit, it uses `gstreamer` to grab a frame from the video feed and provide it as a response. We also include an example app that runs on port :80 that allows you to grab a frame in your web browser.

TODO: We're gonna move this into a git repository, no worries.

TODO: Also it doesn't provide a restful API, so hold up.

```py
#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer
from subprocess import Popen
import os

os.chdir(os.path.join(os.path.dirname(__file__), 'static'))

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/index.html':
            args = ['gst-launch', 'tvsrc', 'device=/dev/video2',
                    'num-buffers=1', '!', 'mfw_ipucsc', '!',
                    'jpegenc', '!', 'filesink', 'location=test.jpg']
        Popen(args).communicate()
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0', 80), Handler)

import socket
server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.serve_forever()
```
