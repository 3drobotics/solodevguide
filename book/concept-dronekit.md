# DroneKit

[DroneKit-Python](http://python.dronekit.io/) is a Python library that can be used to connect to, monitor and control a vehicle. You can use it to write your own scripts and interact with Solo from either a ground station or from Solo's onboard companion computer.

<aside class="note">
Solo uses [DroneKit-Python v1.1](http://python.dronekit.io/) internally to develop its [Smart Shots](concept-smartshot.html). When you create your own DroneKit-Python scripts you can run them with the *latest* version of DroneKit in a virtual environment.
</aside>

Working with DroneKit-Python is virtually the same on any platform/vehicle. Developers should read the [DroneKit-Python Documentation](http://python.dronekit.io/) in order to understand the key concepts.

This topic provides a very brief introduction to the "nuances" of working with DroneKit-Python on Solo. It explains how a script should connect to Solo, how to deploy and run scripts on the device, some limitations of using DroneKit scripts (as opposed to using [Smart Shots](concept-smartshot.html)), and how to access useful platform features. 

<aside class="tip">
You can try out most of the ideas presented here by [running the examples](example-get-started.html).
</aside>



## Connecting to Solo

The MAVLink telemetry protocol (used to communicate with Solo) is served on UDP port 14550. Scripts can connect as a UDP client to `udpin:0.0.0.0:14550` from any external device connected to its network or from Solo's terminal.

From Python, you connect to Solo on this port using the `connect()` method as shown:

<div class="any-code"></div>

```py
from dronekit import connect

# Connect to UDP endpoint (and wait for default attributes to accumulate)
print 'Connecting to Solo ...'
vehicle = connect('udpin:0.0.0.0:14550', wait_ready=True)
```

The `connect()` method returns a `Vehicle` object that can be used to observe and control the drone.

Other than the connection string used for Solo, all other aspects of calling the API are the same as in the [DroneKit-Python documentation](http://python.dronekit.io/).


## Deploying scripts to Solo

Scripts can be deployed and run on Solo using the [Solo CLI](starting-utils.html#deployingrunning-dronekit-scripts-on-solo). The CLI takes care of packaging all the scripts in a folder along with all dependencies listed in the folder's **requirements.txt** file. It can then be used to transfer the package to Solo, install it, and run a specified script in a virtual environment.

<aside class="note">
This approach has several benefits over using Solo's "inbuilt" version of DroneKit-Python:

1. No Internet connection or reliance on package management on Solo is needed.
1. Packages are installed in a virtual environment, so they don't collide with the global Solo namespace.
1. You can always use the most recent DroneKit-Python in your examples (the inbuilt version is updated less regularly).
1. The *Solo CLI* is simple to use and will already be present developer's computers. 
</aside>



### solo script pack

`solo script` is used to package all code and dependencies needed to run a script. It creates an archive that can be deployed to Solo (as described in the next section).

The command is run inside a directory which should contain all needed Python scripts along with a `requirements.txt` file listing all the needed `pip` dependencies. Minimally this will include the latest version of DroneKit:

   <div class="any-code"></div>

   ```
   dronekit>=2.0.0
   ```

<aside class="tip">
The system will install fresh copies of any listed files into the script's virtual environment on Solo. The exception is OpenCV; if this is listed then a system version will be used instead. 
</aside>

Open a terminal, navigate to the directory to package, and enter the following command:

<div class="host-code"></div>

```
solo script pack
```

After some processing, this will create an archive called `solo-script.tar.gz` in your current directory, or display an error if the process could not complete.


### solo script run ...

In order to deploy the script archive and run the app, first connect to Solo's wifi network. 

Then enter the following command to upload the script archive to Solo, unpack it and its dependencies, and then attempt to run the specified python script (`yourscriptname.py`):

<div class="host-code"></div>

```
solo script run yourscriptname.py
```



## Accessing Solo Features

DroneKit-Python scripts can use any features of the underlying platform that are (or can be made) accessible to Python. 

For example, DroneKit-Python does not have any API for direct access to camera/video (though it can control the Camera gimbal). However it can use platform services to access video frames and libraries like *OpenCv* for post-processing. See [this example](example-opencv.html) for more information.


## DroneKit-Python Limitations

There is currently no inbuilt support for:

* Launching DroneKit-Python scripts from the Controller.
* Launching DroneKit-Python scripts on system boot.
* Passing parameters to a script after it has started.
* Pausing or restarting a script due to external interaction.

Some of these features are available to [Smart Shots](concept-smartshot.html).