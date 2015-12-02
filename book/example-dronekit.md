# Using DroneKit

*[DroneKit](http://dronekit.io/)* is a library that can be used to monitor and control a connected vehicle. Solo uses [DroneKit-Python v1.1](http://python.dronekit.io/) internally to develop its [Smart Shots](concept-smartshot.html). 

This example shows how to install the *latest* version of DroneKit into a virtual environment and run a basic script to retrieve vehicle information including position, speed, battery life, current flight mode etc.

The full source code for the example is [available on Github here](https://github.com/3drobotics/solodevguide/tree/master/examples/dkexample).

<aside class="note">
The latest version of *DroneKit-Python* includes many useful features and bug fixes that may not be present in Solo's default installation. The virtual environment approach used here means that you can use whatever DroneKit release you like (and don't have to risk affecting system stability by upgrading Solo).
</aside>

<aside class="caution">
This example uses *DroneKit-Python 2.0*, a standalone Python library. *DroneKit-Python 2.0* is not yet stable! Please [report issues](https://github.com/dronekit/dronekit-python/issues) you discover when using it.
</aside>


## Installing DroneKit on Solo

The process for bundling the example (including DroneKit) is described below in [Installing _dkexample_](#installing-dkexample) (and more generally in [Bundling Python](advanced-python.html)). 

The libraries that are bundled are defined in the example `requirements.txt` file:

<div class="any-code"></div>

```
protobuf==3.0.0a1
requests==2.5.1
wheel==0.24.0
dronekit==2.0.2
```

Note that we are installing a particular branch of `dronekit-python`.


## Connecting to Solo

The MAVLink telemetry protocol (used to communicate with Solo) is served on UDP port 14550. You can set up downstream applications to connect as a UDP client to `udpin:0.0.0.0:14550` from any external device connected to its network (or from Solo's terminal).

From Python, you connect to Solo on this port using the `connect()` method as shown:

<div class="any-code"></div>

```py
from dronekit import connect, VehicleMode

# Connect to UDP endpoint (and wait for default attributes to accumulate)
vehicle = connect('udpin:0.0.0.0:14550', wait_ready=True)
```

The `connect()` method returns a `Vehicle` object that can be used to observe and control the drone.



## Retrieve parameters

The vehicle attributes can then be read, as shown:

<div class="any-code"></div>

```py
# Get all vehicle attributes (state)
print "\nGet all vehicle attribute values:"
print " Global Location: %s" % vehicle.location.global_frame
print " Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
print " Local Location: %s" % vehicle.location.local_frame
print " Attitude: %s" % vehicle.attitude
print " Velocity: %s" % vehicle.velocity
print " GPS: %s" % vehicle.gps_0
print " Mount status: %s" % vehicle.mount_status
print " Battery: %s" % vehicle.battery
print " EKF OK?: %s" % vehicle.ekf_ok
print " Last Heartbeat: %s" % vehicle.last_heartbeat
print " Rangefinder: %s" % vehicle.rangefinder
print " Rangefinder distance: %s" % vehicle.rangefinder.distance
print " Rangefinder voltage: %s" % vehicle.rangefinder.voltage
print " Heading: %s" % vehicle.heading
print " Is Armable?: %s" % vehicle.is_armable
print " System status: %s" % vehicle.system_status.state
print " Groundspeed: %s" % vehicle.groundspeed    # settable
print " Airspeed: %s" % vehicle.airspeed    # settable
print " Mode: %s" % vehicle.mode.name    # settable
print " Armed: %s" % vehicle.armed    # settable
```

## Installing _dkexample_

<aside class="note">
See [Bundling Python](advanced-python.html) for an explanation of the following steps.
</aside>

Clone the [solodevguide](https://github.com/3drobotics/solodevguide) repository and cd into the [examples/dkexample](https://github.com/3drobotics/solodevguide/tree/master/examples/dkexample) directory.

In this folder, prepare your environment by running:

<div class="host-code"></div>

```sh
pip install virtualenv
virtualenv env
echo 'import sys; import distutils.core; s = distutils.core.setup; distutils.core.setup = (lambda s: (lambda **kwargs: (kwargs.__setitem__("ext_modules", []), s(**kwargs))))(s)' > env/lib/python2.7/site-packages/distutils.pth
```

<aside class="note">
On Windows, the last command should instead be:

<div class="host-code"></div>

```sh
echo 'import sys; import distutils.core; s = distutils.core.setup; distutils.core.setup = (lambda s: (lambda **kwargs: (kwargs.__setitem__("ext_modules", []), s(**kwargs))))(s)' > env\Lib\site-packages\distutils.pth
```
</aside>

Activate the virtual environment:

<div class="host-code"></div>

```sh
# On Linux
source ./env/bin/activate

# On Windows
env\Scripts\activate.bat
```

Install the Python dependencies locally, and then package them for Solo:

<div class="host-code"></div>

```sh
pip install -r requirements.txt
pip wheel -r ./requirements.txt --build-option="--plat-name=py27"
```

Next, and every time we make changes to Python, we can sync our code to Solo using *rsync*:

<div class="host-code"></div>

```sh
solo install-pip
rsync -avz --exclude="*.pyc" --exclude="env" ./ root@10.1.1.10:/opt/dkexample
```

<aside class="note">
It is possible to install *rsync* on Windows and use the above command. Alternatively you can use *WinSCP*, create the **opt** folder in Solo's root and then drag/drop the **dkexample** folder into it (you do not need to copy/can delete the **env** folder).
</aside>

Now SSH into Solo. Navigate to the example directory and install packages:

```sh
pip install virtualenv
cd /opt/dkexample
virtualenv env
source ./env/bin/activate
pip install --no-index ./wheelhouse/* -UI
```

Then you can run `python example.py` to see Solo's telemetry output in realtime to the console.

