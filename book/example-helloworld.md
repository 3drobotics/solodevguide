# Hello World (from the sky)!

This example demonstrates a basic [DroneKit](concept-dronekit.html) script that retrieves vehicle information including position, speed, battery life, current flight mode etc.

<aside class="note">
This example is safe to run both locally and on Solo itself, because it doesn't arm the vehicle or start the motors.
</aside>


## How does it work?

### Connecting to Solo

The MAVLink telemetry protocol (used to communicate with Solo) is served on UDP port 14550.

The code to connect to Solo is shown below. This takes an argument for the connection string, but uses `udpin:0.0.0.0:14550` by default.  

<div class="any-code"></div>

```py
from dronekit import connect
import sys

# Connect to UDP endpoint (and wait for default attributes to accumulate)
target = sys.argv[1] if len(sys.argv) >= 2 else 'udpin:0.0.0.0:14550'
print 'Connecting to ' + target + '...'
vehicle = connect(target, wait_ready=True)
```

The `connect()` method returns a `Vehicle` object that can be used to observe and control the drone.


### Retrieve parameters

The vehicle attributes are then read, as shown:

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

### Close the vehicle

The final step in any script is to close the `Vehicle` object, which releases any resources owned by the script:

<div class="any-code"></div>

```py
vehicle.close()
print "Done."
```


## Running the example

The process for running the example is exactly described in [Running the Examples](example-get-started.html) (this topic shows how to run the example on Solo, and locally on a computer communicating with either Solo or a simulated vehicle).  There is addition information on running DroneKit scripts in [DroneKit:Deploying scripts to Solo](concept-dronekit.html#deploying-scripts-to-solo).

To run the example locally:

1. Clone the solodevguide repo and navigate to the "helloworld" example:

   <div class="host-code"></div>

   ```
   git clone https://github.com/3drobotics/solodevguide
   cd solodevguide/examples/helloworld
   ```
   
1. Connect your PC to the Solo Wifi network

1. Run the target script as shown:

   <div class="host-code"></div>

   ```
   python helloworld.py 
   ```
   
   After running the example you should see the following output on the terminal:

   ```
   >helloworld.py
   Connecting to udpin:0.0.0.0:14550...
   >>> PreArm: Need 3D Fix
   >>> APM:Copter solo-1.2.19 (331103b2)
   >>> PX4: 60133536 NuttX: d48fa307
   >>> Frame: QUAD
   >>> PX4v2 0020003C 33345112 32363238
   Vehicle state:
    Global Location: LocationGlobal:lat=0.0,lon=0.0,alt=-0.02
    Global Location (relative altitude): LocationGlobalRelative:lat=0.0,lon=0.0,alt=-0.02
    Local Location: LocationLocal:north=None,east=None,down=None
    Attitude: Attitude:pitch=0.0127924475819,yaw=2.03015804291,roll=-0.0335337780416
    Velocity: [-0.01, -0.02, -0.01]
    Battery: Battery:voltage=16.055,current=0.87,level=77
    Last Heartbeat: 0.826999902725
    Heading: 116
    Groundspeed: 0.0
    Airspeed: 0.0
    Mode: LOITER
    Is Armable?: False
    Armed: False>
   >> PreArm: Need 3D Fix

   Done.
   ```   
   
   
To run the example on Solo

1. [Connect your host computer and Solo to the Internet](starting-utils.html#connecting-solo-to-the-internet) 
   (using the ``solo wifi`` command).
   
1. After navigating to the *helloworld* directory, package the current example folder for installation on Solo using the ``solo script pack command``:

   <div class="host-code"></div>

   ```
   solo script pack
   ```
   
   The libraries that are bundled are defined in the [requirements.txt](https://github.com/3drobotics/solodevguide/blob/master/examples/helloworld/requirements.txt) file in the example directory. For this example DroneKit itself is the only dependency:
   
   <div class="any-code"></div>

   ```
   dronekit>=2.0.0
   ```

   After some processing, this will create an archive called `solo-script.tar.gz` 
   in your current directory, or display an error if the process could not complete.
 
1. Install the script archive on Solo and run the example using the ``solo script run`` command: 

   <div class="host-code"></div>

   ```
   solo script run helloworld.py
   ```

If this is successful, you will see the same result as above when you ran your command locally. The only difference here is that code is now running on Solo: your first step toward programming powerful applications that live on and control your drone autonomously.

Or in other words, you have just deployed your first code that runs, *literally*, in the cloud!
