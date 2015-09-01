# Gimbal Bay

The Gimbal Bay is an extensible interface to which any “Made For Solo”-approved 3rd party vendors can sell an attachable 3-axis gimbal and camera solution. The specifications to the Bay have been made open and freely available here to encourage development with Solo add-ons.

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

...

## Developer spec

The Gimbal Cable has three primary responsibilities:

### Control over MAVLink with Serial

The Gimbal TX and Gimbal RX lines send MAVLink data over a serial connection between the Pixhawk flight controller and the gimbal. This connection is used to both control the pitch, roll, and yaw of the gimbal motors as well as send commands over to the camera (start recording, stop recording, change modes, etc.). More details on camera control can be found in the Software Interface section.

### Coprocessing with USB

The Gimbal Cable provides a USB 2.0 interface with the i.MX6 co-processor on-board Solo. This interface should be used for firmware updating and can optionally be used for any sort of additional processing. For example, you can pull a still from the camera, transfer it to the co-processor, and search the image for pre-defined target. Communication between the Solo coprocessor and the gimbal is not yet available for 3rd party developers.

### Powering the Gimbal

The Gimbal Cable provides two different voltage source to the Gimbal Bay:
VCC Battery (13.5 - 16.8V, 2A)
VCC 5V (Regulated, 5A)

The 5V source should only be used to power the camera. The battery voltage is used for any other purposes.

### HDMI Mini 

The HDMI Mini connection is responsible for transferring video from the camera on the Solo to the first person view in the 3DR app. The HDMI connection does not have the audio pins connected. The video feed supports up to 1080p resolution at 60 frames per second.
Suuported resolutions:
1280x720p60
1280x720p30
720x480p60
720x480p30
640x480p60
640x480p30
1280x720p25(PAL)
720x480p25(PAL)


