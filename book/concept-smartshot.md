# Smart Shots

[Smart shots](http://3drobotics.com/smart-shots/) allow you to pre-program complicated flight paths, enabling users to concentrate on when to take the shot rather than how to fly the vehicle.

The Smart Shot framework builds upon DroneKit, and adds support to pause and resume shots \(storing the flight state\) and re-map controller buttons and sticks during a shot.

The most important functions in the `solo.smartshot` are:

* _Handling RC input._ Remapping the control sticks to perform alternate functions. For example, this is used in Cable Cam to allow the right stick to control Solo's position along the virtual cable instead of its position relative to earth.
* _Buttons._ A and B can be mapped to provide shortcuts like setting fixed waypoints or recording a position.

Since there isn't a framework to implement custom Smart Shots, to intall a custom Smart Shot, you must override an existing flight mode. In this example, our custom Smart Shot called AutoPan, which will automatically yaw the Solo in increments and take a picture at each heading. It will override the Sport Flight Mode.

**Prerequisites:**

* Enable Advanced Flight Modes
* Map Sport to Button A or Button B

To install a custom smart shot requires modification to the following files:

* modes.py
* shotFactory.py
* shots.py

You also need to install your custom smart shot python script \(i.e. autopan.py\) to \/usr\/bin on the Solo.

**Note**: When updating solo to a newer version, the update process will ignore modified files, so be sure to backup any changed files and restore prior to updating. Otherwise you will have to perform a factory reset. Also, depending on the firmware version installed on your Solo, the code in modes.py, shotManager.py and shots.py may vary from this example.

**Step 1. Modify modes.py**

modes.py is the mapping between Pixhawk Flight Modes and what is displayed on the controller. Change **Sport** to **Autopan**.

```py
#!/usr/bin/env python

# mode names - These are what Artoo displays

MODE_NAMES = {
    -1 : "None\0",
    0 : 'Stabilize\0',
    1 : 'Acro\0',
    2 : 'FLY: Manual\0',
    3 : 'Autonomous\0',
    4 : 'Takeoff\0',
    5 : 'FLY\0',
    6 : 'Return Home\0',
    7 : 'Circle\0',
    8 : 'Position\0',
    9 : 'Land\0',
    10 : 'OF_LOITER\0',
    11 : 'Drift\0',
    13 : 'AutoPan\0',
    14 : 'Flip\0',
    15 : 'Auto-tune\0',
    16 : 'Position Hold\0',
    17 : 'Brake\0',
    }
```

**Step 2. Modify shots.py**

shots.py contains the definition of shots. Add an Autopan constant and add the constant to the SHOT\_NAMES array.

```
APP_SHOT_RECORD = 4
APP_SHOT_FOLLOW = 5
APP_SHOT_AUTOPAN = 6

# NULL terminated for sending to Artoo
SHOT_NAMES = {
    APP_SHOT_NONE : "FLY\0",
    APP_SHOT_SELFIE : "Selfie\0",
    APP_SHOT_ORBIT : "Orbit\0",
    APP_SHOT_CABLECAM : "Cable Cam\0",
    APP_SHOT_FOLLOW : "Follow\0",
    APP_SHOT_AUTOPAN : "AutoPan\0"
}
```

**Step 3. Modify shotFactory.py**

shotFactory.py defines the list of Smart Shot classes. Add AutoPan to imports and APP\_SHOT\_AUTOPAN to ShotFactory object.

Add import autopan to imports section.

```
...
import pano
import autopan
...
```

Add APP\_SHOT\_AUTOPAN to ShotFactory object.

```
class ShotFactory(object):
    __shot_classes = {
        shots.APP_SHOT_SELFIE : selfie.SelfieShot,
        shots.APP_SHOT_ORBIT: orbit.OrbitShot,
        shots.APP_SHOT_CABLECAM : cable_cam.CableCamShot,
        shots.APP_SHOT_ZIPLINE : zipline.ZiplineShot,
        shots.APP_SHOT_FOLLOW : follow.FollowShot,
        shots.APP_SHOT_MULTIPOINT : multipoint.MultipointShot,
        shots.APP_SHOT_PANO : pano.PanoShot,
        shots.APP_SHOT_AUTOPAN : autopan.AutoPanShot,
        shots.APP_SHOT_REWIND : rewind.RewindShot,
        shots.APP_SHOT_TRANSECT : transect.TransectShot,
        shots.APP_SHOT_RTL : returnHome.returnHomeShot,
    }
```

**Step 4. Add your custom smart shot dronekit-python script.**

```py
#
# autopan.py
# Implement autopan using DroneKit
# This is a shot where the copter takes a picture while automatically
# yawing.
# Created by Ahmed Agbabiaka
# Sport Mode override, Controller Button integration and
# pan angle math by Jason Short and Will Silva
# Created: 2015/11/15
# Last Modified: 2016/01/01
# Copyright (c) 2015 Viresity, Inc. All Rights Reserved.

from dronekit import Vehicle, LocationGlobalRelative, VehicleMode

from pymavlink import mavutil
import os
from os import sys, path
import math
import struct
import time

sys.path.append(os.path.realpath(''))
import app_packet
import camera
import location_helpers
import shotLogger
import shots
from shotManagerConstants import *
import GoProManager
from GoProConstants import *
from sololink import btn_msg

YAW_SPEED = 10.0 #deg/s

CYLINDER_LENS_ANGLE = 160.0
AUTOPAN_CAPTURE_DELAY = int(UPDATE_RATE * 2.5)
AUTOPAN_MOVE_DELAY = int(UPDATE_RATE * 3.5)

AUTOPAN_YAW_SPEED = 60.0 # deg/s
AUTOPAN_PITCH_SPEED = 60.0 # deg/s

AUTOPAN_DEFAULT_FOV = 220
AUTOPAN_DEFAULT_VIDEO_YAW_RATE = 2.0

MAX_YAW_RATE = 60  # deg/s
MAX_YAW_ACCEL_PER_TICK = (MAX_YAW_RATE) / (4 * UPDATE_RATE)  # deg/s^2/tick

# modes
AUTOPAN_PHOTO = 0
AUTOPAN_VIDEO = 1

AUTOPAN_SETUP = 0
AUTOPAN_RUN = 1
AUTOPAN_EXIT = 2

VIDEO_COUNTER = 15

TICKS_TO_BEGIN = -25

logger = shotLogger.logger

class AutoPanShot():
    def __init__(self, vehicle, shotmgr):
        #vehicle object
        self.vehicle = vehicle

        #shotmanager object
        self.shotmgr = shotmgr

        # ticks to track timing in shot
        self.ticks = 0

        # state machine
        self.state = AUTOPAN_SETUP

        # default mode
        self.autoPanType = AUTOPAN_PHOTO

        # steps to track incrementing in shot
        self.step = 0
        self.stepsTotal = 0

        # Yaw rate for Video AutoPan shot
        self.degSecondYaw = AUTOPAN_DEFAULT_VIDEO_YAW_RATE

        # default FOV for Photo AutoPan shot
        self.cylinder_fov = AUTOPAN_DEFAULT_FOV
        self.lensFOV = CYLINDER_LENS_ANGLE

        # list of angles in photo AutoPan shot
        self.cylinderAngles = None

        # default camPitch
        self.camPitch = camera.getPitch(self.vehicle)

        # default camYaw to current pointing
        self.camYaw = camera.getYaw(self.vehicle)

        # set button mappings on Artoo
        self.setButtonMappings()

        # switch vehicle into GUIDED mode
        self.vehicle.mode = VehicleMode("GUIDED")

        # switch gimbal into MAVLINK TARGETING mode
        self.setupTargeting()

        # take over RC
        self.shotmgr.rcMgr.enableRemapping( True )

    # channels are expected to be floating point values in the (-1.0, 1.0) range
    def handle_rcs(self, channels):
        if self.autoPanType == AUTOPAN_VIDEO:
            self.takeVideo(channels)
            self.manualPitch(channels)
            self.handlePitchYaw()
        else:
            if self.state == AUTOPAN_SETUP:
                self.manualPitch(channels)
                self.manualYaw(channels[YAW])
                self.handlePitchYaw()
            else:
                if self.autoPanType == AUTOPAN_PHOTO:
                    self.takePicture()
                    self.handlePitchYaw()

    def initAutoPan(self):
        # switch gopro mode and initialize AutoPan mode
        if self.autoPanType == AUTOPAN_PHOTO:
            logger.log("[AUTOPAN]: Init Photo AutoPan")
            self.switchGoProMode(CAPTURE_MODE_PHOTO)
            self.initPhoto()
        else:
            logger.log("[AUTOPAN]: Init Video AutoPan")
            # GoProManager will automatically switch to video on RECORD_COMMAND_TOGGLE
            self.initVideo()

    def resetAutoPan(self):
        self.cylinderAngles = None

    def initPhoto(self):
        # Initialize the photo AutoPan shot

        self.cylinder_fov = max(self.cylinder_fov, 91.0)
        self.cylinder_fov = min(self.cylinder_fov, 360.0)

        self.yaw_total = self.cylinder_fov - (self.lensFOV / 4)
        steps = math.ceil(self.cylinder_fov / (self.lensFOV / 4))
        num_photos = math.ceil(self.cylinder_fov / (self.lensFOV / 4))
        yawDelta = self.yaw_total / (num_photos - 1)

        self.origYaw = camera.getYaw(self.vehicle)
        yawStart = self.origYaw - (self.yaw_total / 2.0)

        self.cylinderAngles = []

        for x in range(0, int(steps)):
            tmp = yawStart + (x * yawDelta)
            if tmp < 0:
                tmp += 360
            elif tmp > 360:
                tmp -= 360
            self.cylinderAngles.append(int(tmp))

        self.stepsTotal = len(self.cylinderAngles)

        # go to first angle
        self.camYaw = self.cylinderAngles.pop()

        # give first move an extra second to get there
        self.ticks = TICKS_TO_BEGIN
        self.updateAutoPanStatus(0, self.stepsTotal)

    def takePhoto(self):
        self.ticks += 1

        if self.cylinderAngles is None:
            self.initAutoPan()

        if self.state == AUTOPAN_RUN:
            # time delay between camera moves
            if self.ticks == AUTOPAN_CAPTURE_DELAY:
                self.shotmgr.goproManager.handleRecordCommand(self.shotmgr.goproManager.captureMode, RECORD_COMMAND_TOGGLE)

            if self.ticks > AUTOPAN_MOVE_DELAY:
                self.ticks = 0

                if len(self.cylinderAngles) == 0:
                    self.state = AUTOPAN_EXIT
                else:
                    # select new angle
                    self.camYaw = self.cylinderAngles.pop()

        elif self.state == AUTOPAN_EXIT:
            self.camYaw = self.origYaw
            # let user take a new Pano
            self.state = AUTOPAN_SETUP
            self.resetAutoPan()
            self.setButtonMappings()

    def takeVideo(self, channels):
        if self.state == AUTOPAN_RUN:
            # start recording
            self.shotmgr.goproManager.handleRecordCommand(self.shotmgr.goproManager.captureMode, RECORD_COMMAND_TOGGLE)

            # modulate yaw rate based on yaw stick input
            if channels[YAW] != 0:
                self.degSecondYaw = self.degSecondYaw + (channels[YAW] * MAX_YAW_ACCEL_PER_TICK)

            # limit yaw rate
            self.degSecondYaw = min(self.degSecondYaw, MAX_YAW_RATE)
            self.degSecondYaw = max(self.degSecondYaw, -MAX_YAW_RATE)

            # increment desired yaw angle
            self.camYaw += (self.degSecondYaw * UPDATE_TIME)
            self.camYaw %= 360.0

            self.counter += 1

            if self.counter > VIDEO_COUNTER:
                self.counter = 0
                self.state = AUTOPAN_EXIT
                # stop recording
                self.shotmgr.goproManager.handleRecordCommand(self.shotmgr.goproManager.captureMode, RECORD_COMMAND_TOGGLE)

        elif self.state == AUTOPAN_EXIT:
            self.camYaw = self.origYaw
            self.state = AUTOPAN_SETUP
            self.restAutoPan()
            self.setButtonMappings()

    def setButtonMappings(self):
        buttonMgr = self.shotmgr.buttonManager

        if self.autoPanType == AUTOPAN_VIDEO:
            buttonMgr.setArtooButton(btn_msg.ButtonA, shots.APP_SHOT_AUTOPAN, 0, "\0")
        else:        
            if self.state == AUTOPAN_RUN:
                buttonMgr.setArtooButton(btn_msg.ButtonA, shots.APP_SHOT_AUTOPAN, btn_msg.ARTOO_BITMASK_ENABLED, "Cancel\0")
            else:
                buttonMgr.setArtooButton(btn_msg.ButtonA, shots.APP_SHOT_AUTOPAN, btn_msg.ARTOO_BITMASK_ENABLED, "Begin\0")

        if self.state == AUTOPAN_SETUP:
            if self.autoPanType == AUTOPAN_VIDEO:
                buttonMgr.setArtooButton(btn_msg.ButtonB, shots.APP_SHOT_AUTOPAN, btn_msg.ARTOO_BITMASK_ENABLED, "Video\0")
            elif self.autoPanType == AUTOPAN_PHOTO:
                buttonMgr.setArtooButton(btn_msg.ButtonB, shots.APP_SHOT_AUTOPAN, btn_msg.ARTOO_BITMASK_ENABLED, "Photo\0")
        else:
            buttonMgr.setArtooButton(btn_msg.ButtonB, shots.APP_SHOT_AUTOPAN, 0, "\0")

    def handleButton(self, button, event):
        if button == btn_msg.ButtonA and event == btn_msg.Press:
            if self.autoPanType != AUTOPAN_VIDEO:
                if self.state == AUTOPAN_SETUP:
                    self.state = AUTOPAN_RUN
                else:
                    # enter standby
                    self.resetAutoPan()
                    self.state = AUTOPAN_SETUP
                    logger.log("[AUTOPAN]: Cancel AutoPan")
                    # if we are in video mode, stop Yawing
                    if self.autoPanType == AUTOPAN_VIDEO:
                        self.degSecondYaw = 0

            self.setButtonMappings()

        if button == btn_msg.ButtonLoiter and event == btn_msg.Press:
            if self.autoPanType == AUTOPAN_VIDEO:
                self.degSecondYaw = 0

        # cycle through options
        if self.state == AUTOPAN_SETUP and button == btn_msg.ButtonB and event == btn_msg.Press:
            #clear AutoPan Video yaw speed
            self.degSecondYaw = 0
            if self.autoPanType == AUTOPAN_VIDEO:
                self.autoPanType = AUTOPAN_PHOTO
            elif self.autoPanType == AUTOPAN_PHOTO:
                self.autoPanType = AUTOPAN_VIDEO
            self.setButtonMappings()

    def setupTargeting(self):
            # set gimbal targeting mode
            msg = self.vehicle.message_factory.mount_configure_encode(
                    0, 1,    # target system, target component
                    mavutil.mavlink.MAV_MOUNT_MODE_MAVLINK_TARGETING,  #mount_mode
                    1,  # stabilize roll
                    1,  # stabilize pitch
                    1,  # stabilize yaw
                    )
            self.vehicle.send_mavlink(msg)

    def manualPitch(self, channels):
        if abs(channels[THROTTLE]) > abs(channels[RAW_PADDLE]):
            value = channels[THROTTLE]
        else:
            value = channels[RAW_PADDLE]

        self.camPitch += value * AUTOPAN_PITCH_SPEED * UPDATE_TIME

        if self.camPitch > 0.0:
            self.camPitch = 0.0
        elif self.camPitch < -90:
            self.camPitch = -90

    def manualYaw(self, stick):
        if stick == 0:
            return
        self.camYaw += stick * AUTOPAN_YAW_SPEED * UPDATE_TIME
        if stick > 0:
            self.camDir = 1
        else:
            self.camDir = -1

        self.camYaw = location_helpers.wrapTo360(self.camYaw)

    def handlePitchYaw(self):
        # if we do have a gimbal, use mount_control to set pitch and yaw
        if self.vehicle.mount_status[0] is not None:
            msg = self.vehicle.message_factory.mount_control_encode(
                        0, 1,    # target system, target component
                        # pitch is in centidegrees
                        self.camPitch * 100,
                        0.0, # roll
                        # yaw is in centidegrees
                        self.camYaw * 100,
                        0 # save position
                        )
        else:
            # if we don't have a gimbal, just set CONDITION_YAW
            msg = self.vehicle.message_factory.command_long_encode(
                        0, 0,    # target system, target component
                        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
                        0, #confirmation
                        self.camYaw,  # param 1 - target angle
                        YAW_SPEED, # param 2 - yaw speed
                        self.camDir, # param 3 - direction
                        0.0, # relative offset
                        0, 0, 0 # params 5-7 (unused)
                        )

        self.vehicle.send_mavlink(msg)

    def switchGoProMode(mode):
        # switch gopro mode CAPTURE_MODE_PHOTO, CAPTURE_MODE_VIDEO
        self.shotmgr.goproManager.sendGoProCommand(mavutil.mavlink.GOPRO_COMMAND_CAPTURE_MODE, (mode, 0 ,0 , 0))

```

Put autopan.py on the solo in \/usr\/bin

**Step 5. Reboot Solo and the Controller**

Reboot Solo and the controller. When the controller is rebooted, AutoPan should be displayed on the controller as Mapped to Button A or Button B.

**Step 6. Start Custom Smart Shot**

Press Fly to take off and press the button mapped to AutoPan to start the AutoPan. Choose Photo or Video to choose a Photo or Video pan.

