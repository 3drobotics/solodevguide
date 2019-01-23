# Running the Examples

This guide contains a number of examples showing how to use DroneKit on Solo. These are stored on Github in separate folders under 
[solodevguide/examples](https://github.com/3drobotics/solodevguide/tree/master/examples).

The examples can be run locally from your development computer to communicate with either Solo or a simulated copter, or they can be run on Solo itself.


## Running on Solo

The following instructions can be used to package each of the examples on a host computer, then deploy and run them on Solo:

1. Clone the solodevguide repo and navigate to your target example (in this example: "helloworld"):

   <div class="host-code"></div>

   ```
   git clone https://github.com/3drobotics/solodevguide
   cd solodevguide/examples/helloworld
   ```

1. [Connect your host computer and Solo to the Internet](starting-utils.html#connecting-solo-to-the-internet) 
   (using the ``solo wifi`` command).
   
1. Package the current example folder for installation on Solo using the ``solo script pack command``:

   <div class="host-code"></div>

   ```
   solo script pack
   ```

  After some processing, this will create an archive called `solo-script.tar.gz` 
  in your current directory, or display an error if the process could not complete.
 
1. Install the script archive on Solo and run a specified script 
   using the ``solo script run`` command (your computer 
   must be connected to the Solo wifi). In this example we start **helloworld.py**: 

   <div class="host-code"></div>

   ```
   solo script run helloworld.py
   ```

<aside class="tip">
More general information can be found in [DroneKit:Deploying scripts to Solo](concept-dronekit.html#deploying-scripts-to-solo).
</aside>


## Running from a host PC to Solo

The following instructions explain how to run the examples locally from a host PC, communicating with Solo.

1. Clone the solodevguide repo and navigate to your target example (in this example: "helloworld"):

   <div class="host-code"></div>

   ```
   git clone https://github.com/3drobotics/solodevguide
   cd solodevguide/examples/helloworld
   ```

1. Connect your PC to the Solo WiFi network.

1. Run the target script as shown:

   <div class="host-code"></div>

   ```
   python helloworld.py 
   ```
   
   <aside class="tip">There is no need to specify a connection string as the example uses the Solo port by default (`'udpin:0.0.0.0:14550'`), and this is accessible while we're on the Solo WiFi network.</aside>


## Running from a host PC to Simulator

The following instructions explain how to run the examples locally from a host PC, communicating with a simulated device.

1. Set up a simulated vehicle using the instructions in the [DroneKit documents here](http://python.dronekit.io/guide/sitl_setup.html).

1. Clone the solodevguide repo and navigate to your target example (in this example: "helloworld"):

   <div class="host-code"></div>

   ```
   git clone https://github.com/3drobotics/solodevguide
   cd solodevguide/examples/helloworld
   ```

1. Run the target script, specifying the SITL loopback address as shown:

   <div class="host-code"></div>

   ```
   python helloworld.py 127.0.0.1:14550
   ```
   
   <aside class="note">Depending on how you set up the simulator, the loopback address may instead be `tcp:127.0.0.1:5760`.</aside>
   


