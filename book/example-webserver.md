# Running a Webserver

Building upon the Hello World! example, let's run a web server from Solo that is able to display realtime telemetry to any web browser running on a device connected to Solo's network.

This can provide an alternate interface to Solo internals than just the Solo app. For example, you can create a ground control station written entirely in JavaScript and HTML, or allow a control panel for custom (or even fully autonomous) actions by Solo!

**NOTE:** To run this example, please `git clone` or download all the files in the [webserver folder](https://github.com/3drobotics/solodevguide/tree/master/examples/webserver) on Github.

## Using Flask

To run the server, we're going to use a package called Flask. The requirements we are building into this package are the following:

<div class="any-code"></div>

```
Flask>=0.10
eventlet>=0.17
Flask-SocketIO>=1.0
dronekit>=2.0.0,<=2.99999
```

This specifies that we want Flask, our webserver, DroneKit to communicate with our vehicle, and then two more packages: `eventlet` and `Flask-SocketIO` which allow us to use websockets to talk to a web browser.

In our file `server.py` we have a lot of content, but we can break it down into a few smaller sections:

<div class="any-code"></div>

```
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
```

This creates the Flask application.

<div class="any-code"></div>

```
@app.route('/')
def index():
    return render_template('index.html')
```

This creates an "endpoint" at the path "/". That means when you navigate to http://10.1.1.10:5000/ on your web broswer, it will return the contents of this function to the web browser. Here, we run the function `render_template`, which looks at the file in `templates/index.html` and renders it to the browser.

See more in [the Flask documentation](http://flask.pocoo.org/) about templates and route endpoints.

### Websockets

Finally, we have a long-lived thread in the `latlog` file which updates us about our vehicle's location. Every half-second, we run the command `socketio.emit` which tells all connected clients over websockets the contents of the packets.

<div class="any-code"></div>

```
def latlog(vehicle):
    while True:
        eventlet.sleep(.5)
        loc = vehicle.location.global_frame
        if loc:
            socketio.emit('location', {
                "altitude": loc.alt,
                "longitude": loc.lon,
                "latitude": loc.lat,
                })
        else:
            socket.emit('location', None)
````
