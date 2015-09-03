# Using DroneKit

*[DroneKit](http://dronekit.io/)* is a library that can interact with Solo via telemetry, flight modes, or positional control. Solo uses *DroneKit-Python* internally to develop its [Smart Shots](concept-smartshot.html). In this example, we'll install and use 

<aside class="danger">
This uses a branch of DroneKit Python that is not yet stable.
</aside>

## Connecting to Solo externally

MAVLink is served from Solo on UDP port 14560. In this configuration, you can set up downstream applications to connect as a UDP client to this address. For example:

```
mavproxy.py --master udpout:10.1.1.10:14560
```

This command address work on Solo or from an external device on the network.

## Running DroneKit

Using this `requirements.txt` file:

```
protobuf==3.0.0a1
requests==2.5.1
wheel==0.24.0
git+https://github.com/tcr3dr/mavlink@tcr-pymavlink
git+https://github.com/dronekit/dronekit-python@tcr-nomp
```

We can run this script on Solo (or when connected to Solo's wifi):

```py
from droneapi import connect
from droneapi.lib import VehicleMode
from pymavlink import mavutil
import time

# First get an instance of the API endpoint
api = connect('udpout:10.1.1.10:14560')
# Get the connected vehicle (currently only one vehicle can be returned).
vehicle = api.get_vehicles()[0]

time.sleep(5)

# Get all vehicle attributes (state)
print "\nGet all vehicle attribute values:"
print " Location: %s" % vehicle.location
print " Attitude: %s" % vehicle.attitude
print " Velocity: %s" % vehicle.velocity
print " GPS: %s" % vehicle.gps_0
print " Groundspeed: %s" % vehicle.groundspeed
print " Airspeed: %s" % vehicle.airspeed
print " Mount status: %s" % vehicle.mount_status
print " Battery: %s" % vehicle.battery
print " Rangefinder: %s" % vehicle.rangefinder
print " Rangefinder distance: %s" % vehicle.rangefinder.distance
print " Rangefinder voltage: %s" % vehicle.rangefinder.voltage
print " Mode: %s" % vehicle.mode.name    # settable
print " Armed: %s" % vehicle.armed    # settable
```
