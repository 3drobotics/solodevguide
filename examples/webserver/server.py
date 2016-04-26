from flask import Flask, render_template
from flask_socketio import SocketIO
import dronekit
import sys
import socket
import threading
import time
import signal

# Allow us to reuse sockets after the are bound.
# http://stackoverflow.com/questions/25535975/release-python-flask-port-when-script-is-terminated
socket.socket._bind = socket.socket.bind
def my_socket_bind(self, *args, **kwargs):
    self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return socket.socket._bind(self, *args, **kwargs)
socket.socket.bind = my_socket_bind
# okay, now that that's done...

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def latlog(vehicle):
    while True:
        time.sleep(.5)
        loc = vehicle.location.global_frame
        if loc:
            socketio.emit('location', {
                "altitude": loc.alt,
                "longitude": loc.lon,
                "latitude": loc.lat,
                })
        else:
            socket.emit('location', None)

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) >= 2 else '127.0.0.1:14550'
    print 'Connecting to ' + target + '...'
    vehicle = dronekit.connect(target)
    vehiclethread = threading.Thread(target=latlog, args=(vehicle,))
    vehiclethread.start()
    socketio.run(app, host="0.0.0.0", port=8080)
