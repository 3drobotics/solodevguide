# Using DroneKit

*[DroneKit](http://dronekit.io/)* is a library that can interact with Solo via telemetry, flight modes, or positional control. Solo uses *DroneKit-Python* internally to develop its [Smart Shots](concept-smartshot.html). In this example, we'll install and use 

## Connecting to Solo externally

MAVLink, the telemetry protocol used to control and communicate with Solo, is served on UDP port 14560. When connected to Solo's network, you can set up downstream applications to connect as a UDP client to this address. For example, using the *[MAVProxy](http://dronecode.github.io/MAVProxy)* command line tool:

```
mavproxy.py --master udpout:10.1.1.10:14560
```

You're able to connect to `10.1.1.10:14560` both from Solo's terminal as well as on an external device on its network.

## Using DroneKit on Solo

<aside class="danger">
This example a forthcoming release of DroneKit-Python that is not yet stable. Please [file any issues](https://github.com/dronekit/dronekit-python/issues) you have while using it.
</aside>

Our example will use DroneKit-Python 2.0, a standalone Python library that is able to communicate with Solo's autopilot and retrieve information about its position, speed, battery life, and current flight mode.

The most important consideration is the libraries. We will be using this `requirements.txt` file for this example:

```
protobuf==3.0.0a1
requests==2.5.1
wheel==0.24.0
git+https://github.com/tcr3dr/mavlink@tcr-pymavlink
git+https://github.com/dronekit/dronekit-python@tcr-nomp
```

Note that we are installing a particular version of `pymavlink` and a particular branch of `dronekit-python`.

From Python, it's simple to connect to Solo and retrieve parameters:

```py
from droneapi import connect

# Connect to UDP endpoint.
vehicle = connect('udpout:10.1.1.10:14560')
# Wait for parameters to accumulate.
time.sleep(5)

# Print our location and attitude.
print "Location: %s" % vehicle.location
print "Attitude: %s" % vehicle.attitude
```

## Installing _dkexample_

<aside class="note">
See [Bundling Python](advanced-python.html) for an explanation of the following steps.
</aside>

Clone the [solodevguide](https://github.com/3drobotics/solodevguide) repository and cd into the [examples/dkexample](https://github.com/3drobotics/solodevguide/tree/master/examples/dkexample) directory.

In this folder, prepare your environment by running:

```sh
virtualenv env
echo 'import sys; import distutils.core; s = distutils.core.setup; distutils.core.setup = (lambda s: (lambda **kwargs: (kwargs.__setitem__("ext_modules", []), s(**kwargs))))(s)' > env/lib/python2.7/site-packages/distutils.pth
```

Install the Python dependencies locally, and then package them for Solo:

```sh
source ./env/bin/activate
pip install -r requirements.txt
pip wheel -r ./requirements.txt --build-option="--plat-name=py27"
```

Next, and every time we make changes to Python, we can sync our code to Solo using *rsync*:

```sh
rsync -avz --exclude="*.pyc" --exclude="env" ./ solo:/opt/dkexample
```

Now SSH into Solo. Navigate to the example directory and install packages:

```sh
cd /opt/dkexample
virtualenv env
source ./env/bin/activate
pip install --no-index ./wheelhouse/* -UI
```

Then you can run `python example.py` to see Solo's telemetry output in realtime to the console.
