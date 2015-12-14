# Hello World (from above)!

*[DroneKit](http://dronekit.io/)* is a library that can be used to monitor and control a connected vehicle. Solo uses [DroneKit-Python v1.1](http://python.dronekit.io/) internally to develop its [Smart Shots](concept-smartshot.html). 

This example shows how to install the *latest* version of DroneKit into a virtual environment and run a basic script to retrieve vehicle information including position, speed, battery life, current flight mode etc.

**NOTE:** To run this example, please `git clone` or download all the files in the [helloworld folder](https://github.com/3drobotics/solodevguide/tree/master/examples/helloworld) on Github.

## Installing DroneKit on Solo

The process for bundling the example (including DroneKit) is described below in [Installing _dkexample_](#installing-dkexample) (and more generally in [Bundling Python](advanced-python.html)). 

The libraries that are bundled are defined in the example `requirements.txt` file:

<div class="any-code"></div>

```
dronekit>=2.0.0
```


## Connecting to Solo

The MAVLink telemetry protocol (used to communicate with Solo) is served on UDP port 14550. You can set up downstream applications to connect as a UDP client to `udpin:0.0.0.0:14550` from any external device connected to its network (or from Solo's terminal).

From Python, you connect to Solo on this port using the `connect()` method as shown:

<div class="any-code"></div>

```py
from dronekit import connect, VehicleMode
import time
import sys

# Connect to UDP endpoint (and wait for default attributes to accumulate)
target = sys.argv[1] if len(sys.argv) >= 2 else 'udpin:0.0.0.0:14550'
print 'Connecting to ' + target + '...'
vehicle = connect(target, wait_ready=True)
```

The `connect()` method returns a `Vehicle` object that can be used to observe and control the drone.



## Retrieve parameters

The vehicle attributes can then be read, as shown:

<div class="any-code"></div>

```py
# Get all vehicle attributes (state)
print "Vehicle state:"
print " Global Location: %s" % vehicle.location.global_frame
print " Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
print " Local Location: %s" % vehicle.location.local_frame
print " Attitude: %s" % vehicle.attitude
print " Velocity: %s" % vehicle.velocity
print " Battery: %s" % vehicle.battery
print " Last Heartbeat: %s" % vehicle.last_heartbeat
print " Heading: %s" % vehicle.heading
print " Groundspeed: %s" % vehicle.groundspeed
print " Airspeed: %s" % vehicle.airspeed
print " Mode: %s" % vehicle.mode.name
print " Is Armable?: %s" % vehicle.is_armable
print " Armed: %s" % vehicle.armed
```

## Running helloworld.py on Solo

Using the *Solo CLI*, we can directly run scripts on Solo. The requirements for this are the following:

1. All Python code should live in the folder you run the `solo script` command in.
1. All Python package dependencies should be specified in the `requirements.txt` file.

Because we have done the above, we are able to complete the first step in deploying code.

### `solo script pack`

First we have to package our code into an archive that can be deployed to Solo. First, connect, ensure your computer is connected to the Internet (or if you are connected to Solo, you have run `solo wifi`). Then run the following:

<div class="host-code"></div>

```
solo script pack
```

After some processing, this will create an archive called `solo-script.tar.gz` in your current directory, or display an error if the process could not complete.

### `solo script run ...`

Now that we have a script archive, we can run it. Connect to Solo's wifi network. Next, run:

<div class="host-code"></div>

```
solo script run helloworld.py
```

This will upload the script archive to Solo, unpack it and its dependencies, and then attempt to run the `helloworld.py` script as indicated in the command line.

If this is successful, you will see the same result as above when you ran your command locally. The only difference here is that code is now running on Solo: your first step toward programming powerful applications that live on and control your drone autonomously.

Or in other words, you have just deployed your first code that runs, *literally*, in the cloud!
