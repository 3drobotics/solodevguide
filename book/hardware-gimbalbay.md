# Gimbal Bay

The Gimbal Bay is an extensible interface to which any “Made For Solo”-approved 3rd party vendors can sell an attachable 3-axis gimbal and camera solution. The specifications to the Bay have been made open and freely available here to encourage the development of Solo add-ons.

## Electrical Interface
There are two physical connections from the Solo to a gimbal. The Solo Gimbal cable, which primarily manages the position and recording state of the camera, and the HDMI cable which routes the video signal. 

The board side connector can be found on Digikey [here](http://www.digikey.com/product-detail/en/5031540890/5031540890-ND/2819082). The mating connector can be found here 

Pin | Description
--- | ---
1 | VCC Battery
2 | VCC 5V
3 | GND (Gimbal)
4 | GND (USB)
5 | Gimbal Rx
6 | Gimbal Tx
7 | USB D+
8 | USB D-

## Hardware spec

<aside class="todo">
This section is missing.
</aside>

## Developer spec

The Gimbal Cable has three primary responsibilities:

### Control over MAVLink with Serial

The Gimbal TX and Gimbal RX lines send [MAVLink](http://qgroundcontrol.org/mavlink/start) data over a serial connection between the Pixhawk flight controller and the gimbal. This connection is used to both control the pitch, roll, and yaw of the gimbal motors as well as send commands over to the camera (start recording, stop recording, change modes, etc). More details on camera control can be found in the [Software Interface](#software-interface) section.

### Coprocessing with USB

The Gimbal Cable provides a USB 2.0 interface with the i.MX6 co-processor on-board Solo. This interface should be used for firmware updating and can optionally be used for any sort of additional processing. For example, you can pull a still from the camera, transfer it to the co-processor, and search the image for pre-defined target. Communication between the Solo coprocessor and the gimbal is not yet available for 3rd party developers.

### Powering the Gimbal

The Gimbal Cable provides two different voltage source to the Gimbal Bay:
VCC Battery (13.5 - 16.8V, 2A)
VCC 5V (Regulated, 5A)

The 5V source should only be used to power the camera. The battery voltage is used for any other purposes.

### HDMI Mini 

The [HDMI](https://en.wikipedia.org/wiki/HDMI) Mini connection is responsible for transferring video from the camera on the Solo to the first person view in the 3DR app. The HDMI connection does not have the audio pins connected. The video feed supports up to 1080p resolution at 60 frames per second.

Supported resolutions:

* 1280x720p60
* 1280x720p30
* 720x480p60
* 720x480p30
* 640x480p60
* 640x480p30
* 1280x720p25(PAL)
* 720x480p25(PAL)

## Software Interface

In order to have Solo control a gimbal, Ardupilot must know how to communicate with the gimbal. Fortunately, Ardupilot already has the ability to communicate with several types of pre-existing gimbal controllers including *SToRM32* and *Alexmos*. The custom Solo Gimbal protocol is not yet supported by any released versions of Ardupilot. 

*SToRM32* is recommended as it features the most straightforward communication protocol. You can find more information about [this type of gimbal controller here](http://www.olliw.eu/storm32bgc-wiki/Main_Page) and Ardupilot integration can be [found here](http://copter.ardupilot.com/wiki/common-storm32-gimbal/).

<aside class="warning">
For development purposes, a Pixhawk 1 and Copter 3.3 Ardupilot firmware are recommended. The Solo development stack is not yet ready to integrate multiple types of gimbals so it will not work on Solo. 
</aside>


### Common Gimbal Camera Control
There are a set of camera functions that are common amongst all gimbal/camera systems. These functions include START RECORDING/STOP RECORDING, POWER ON/OFF, & CHANGE MODES.

However, 3rd party developers cannot currently take advantage of the pre-set camera-related buttons on the Solo controller because they are sent as GoPro specific commands.In addition, there is not yet a way for 3rd party developers to capture any button events on the Solo coprocessor or Ardupilot.

### Custom Gimbal Camera Control

<aside class="note">
History Note: MAVLink was designed several years ago when there were only a few hundred people using UAVs in academia. As such, the protocol has a number of design flaws primarily caused by the maintenance of a central repository of commands and supported devices. For example, some camera-related commands include a `CAMERA_ID` param but others don’t - this consistency can’t be easily changed because there are already other codebases depending on this packet format. As another example, multiple developers may try to use the same previously unused component or system id at the same time and come into conflict with each other.
</aside>


As a workaround for many of the protocol’s inadequacies, `COMMAND_LONG` was created and it’s the recommended command for any unique, custom camera or gimbal functionality:

Byte index | Value Size (bytes) | Value Description | Value
--- | --- | --- | ---
0 | 4 | Param 1 | {DEPENDENDENT ON COMMAND}
4 | 4 | Param 2 | {DEPENDENDENT ON COMMAND}
8 | 4 | Param 3 | {DEPENDENDENT ON COMMAND}
12 | 4 | Param 4 | {DEPENDENDENT ON COMMAND}
16 | 4 | Param 5 | {DEPENDENDENT ON COMMAND}
20 | 4 | Param 6 | {DEPENDENDENT ON COMMAND}
24 | 4 | Param 7 | {DEPENDENDENT ON COMMAND}
28 | 2 | MAV_COMMAND (User defined command) | {DEPENDENDENT ON USE CASE}
30 | 1 | Target System | 0
31 | 1 | Target Component | MAV_COMP_ID_GIMBAL
32 | 1 | Confirmation Number | Nth time packet was sent

`COMMAND_LONG` essentially gives MAVLink consumers the ability to define their own commands without worrying about whether it already exists in the MAVLink spec or if other developers are writing a conflicting spec. It is essentially a packet within a packet. 3rd party developers can define their own commands (`MAV_COMMAND`, byte 28 above) and up to 7 parameters to send along with that command. Their application can capture the `COMMAND_LONG` packet header and then parse the custom `MAV_COMMAND` identifier to route the packet to the appropriate handler.

