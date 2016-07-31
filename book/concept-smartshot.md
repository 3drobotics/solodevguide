# Smart Shots

[Smart shots](http://3drobotics.com/smart-shots/) allow you to pre-program complicated flight paths, enabling users to concentrate on when to take the shot rather than how to fly the vehicle.

The Smart Shot framework builds upon DroneKit, and adds support to pause and resume shots \(storing the flight state\) and re-map controller buttons and sticks during a shot.

The most important functions in the `solo.smartshot` are:

* _Handling RC input._ Remapping the control sticks to perform alternate functions. For example, this is used in Cable Cam to allow the right stick to control Solo's position along the virtual cable instead of its position relative to earth.
* _Buttons._ A and B can be mapped to provide shortcuts like setting fixed waypoints or recording a position.

Since there isn't a framework to implement custom Smart Shots, to intall a custom Smart Shot, you must override an existing flight mode. In this example, our custom Smart Shot called AutoPan, will automatically yaw the Solo in 45 degreee increments and take a picture at each heading. It will override the Sport Flight Mode.

**Prerequisites:**

* Enable Advanced Flight Modes
* Map Sport to Button A or Button B

To install a custom smart shot requires modification to the following files:

* modes.py
* shotManager.py
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

shots.py contains the definition of shots. Add and Autopan constant and add the constant to the SHOT\_NAMES array.

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

**Step 3. Modify shotManager.py**

shotManager.py manages the SmartShots. Add an import for your custom smart shot, add an entry to handleButtons function to handle the button press mapped to your custom smart shot, and an entry to the triggerShot function the handleButtons function trigger the smart shot.

Add an import for autopan at the top of shotManager.py. It can be anywhere at the top as long as it is with the other import statements.

```py
...
import modes
import orbit
import autopan
import RCRemapper
import selfie
...
```

Add an entry to the handleButtons function to handle the controller button mapped to Autopan.

```py
def handleButtons(self):
        ...
        if self.currentShot == shots.APP_SHOT_NONE:
            if event == btn_msg.Press:
                if button == btn_msg.ButtonA or button == btn_msg.ButtonB:
                    # see what the button is mapped to
                    (shot, mode) = self.buttonManager.getFreeButtonMapping(button)

                    # hack to get autopan
                    if (mode == 13):
                        logger.log("hack - mode: %s" % modes.MODE_NAMES[mode])
                        shot = shots.APP_SHOT_AUTOPAN

                    # only allow entry into these shots if the app is attached
                    allowedShots = [shots.APP_SHOT_ORBIT, shots.APP_SHOT_CABLECAM, shots.APP_SHOT_AUTOPAN]
        ...
```

Add an entry to triggerShot function to trigger the Autopan Smart Shot.

```py
def triggerShot(self, shot):
    # invalid shot!
    if shot not in shots.SHOT_NAMES:
        logger.log("[triggerShot]: Error, trying to trigger an invalid shot! %d"%(shot))
        return
    ...
    elif self.currentShot == shots.APP_SHOT_AUTOPAN:
        self.initStreamRates()
        self.curController = autopan.AutoPanShot(self.vehicle, self)
    ...
```

**Step 4. Add your custom smart shot dronekit-python script.**

This example SmartShot, AutoPan will yaw the Solo and take a picture at each heading.

```py
test
## autopan.py
# Implement autopan using DroneKit
# This is a shot where the copter takes a picture while automatically
# yawing.
# Created by Ahmed Agbabiaka# Created: 2015/11/15
# Last Modified: 2016/01/01
# Copyright (c) 2016 Viresity, Inc. All Rights Reserved.

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

# modes
AUTOPAN_PHOTO = 0
AUTOPAN_VIDEO = 1

AUTOPAN_SETUP = 0
AUTOPAN_RUN = 1
AUTOPAN_EXIT = 2

logger = shotLogger.logger

MAVLINK_GIMBAL_SYSTEM_ID = 1
MAVLINK_GIMBAL_COMPONENT_ID = 154
VIDEO_MODE = 0
PHOTO_MODE = 1

class AutoPanShot():
    def __init__(self, vehicle, shotmgr):
        #vehicle object
        self.vehicle = vehicle

        #shotmanager object
        self.shotmgr = shotmgr

        # state machine
        self.state = AUTOPAN_SETUP

        # default mode
        self.autoPanType = AUTOPAN_PHOTO

        # default camPitch
        self.camPitch = camera.getPitch(self.vehicle)

        # default camYaw to current heading
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
    		SwitchGoProMode(VIDEO_MODE)
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
    				self.TakePicture()
    				self.handlePitchYaw()
    				
    				SwitchGoProMode(PHOTO_MODE)
			
            		self.Pan( 90, -1, True)
            		self.TakePicture()
            		time.sleep(2)
        
            		self.Pan( 45, 1, True)
            		self.TakePicture()
            		time.sleep(2)
            
            		self.Pan( 0, 1, True)
            		self.TakePicture()
            		time.sleep(2)
            
            		self.Pan( 45, 1, True)
            		self.TakePicture()
            		time.sleep(2)
		
            		self.Pan( 90, 1, True)
            		self.TakePicture()
            		time.sleep(2)
    				self.handlePitchYaw()
       
        # Always call flush to guarantee that previous writes to the vehicle
        # have taken place
        self.vehicle.flush()

    def initAutoPan(self):
    	# We reset to the beginning for all states
        if self.autoPanType == AUTOPAN_PHOTO:
            logger.log("[AUTOPAN]: Init Photo Pan")
            self.enterPhotoMode()
            self.initPhoto()
        else:
            logger.log("[PANO]: Init Video Pan")
    
    def takePhoto(self):
    	self.shotmgr.goproManager.handleRecordCommand(self.shotmgr.goproManager.captureMode, RECORD_COMMAND_TOGGLE)
    	
    def takeVideo(self, channels):
    	tbd
		
	def Pan(heading, direction, relative):			
		if relative:
			is_relative=1 #yaw relative to direction of travel
		else:
			is_relative=0 #yaw is an absolute angle (0-360; 0 is north)
		
		# create the CONDITION_YAW command using command_long_encode()
		msg = self.vehicle.message_factory.command_long_encode(
			0, 0,			# target system, target component
			mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
			0, 				#confirmation
			heading,    	# param 1, yaw in degrees
			0,          	# param 2
			direction,      # param 3, direction -1 ccw, 1 cw
			is_relative,	# param 4, relative offset 1, absolute angle 0
			0, 0, 0)		# param 5 ~ 7 not used
		
		# send command to vehicle
		self.vehicle.send_mavlink(msg)
		
		# Always call flush to guarantee that previous writes to the vehicle have taken place
        self.vehicle.flush()
	
	def SwitchGoProMode(mode):
		msg = self.vehicle.message_factory.gopro_set_request_encode(
			MAVLINK_GIMBAL_SYSTEM_ID, MAVLINK_GIMBAL_COMPONENT_ID,	# target system, target component
			mavutil.mavlink.GOPRO_COMMAND_CAPTURE_MODE,				# command
			(mode, 0, 0, 0))										# params 1-4
			
		# send command to vehicle
		self.vehicle.send_mavlink(msg)
		
		# Always call flush to guarantee that previous writes to the vehicle have taken place
        self.vehicle.flush()
	
	def TakePicture():
		msg = self.vehicle.message_factory.gopro_set_request_encode(
			MAVLINK_GIMBAL_SYSTEM_ID, MAVLINK_GIMBAL_COMPONENT_ID,	# target system, target component
			mavutil.mavlink.GOPRO_COMMAND_CAPTURE_SHUTTER,			# command
			(1, 0, 0, 0))											# params 1-4
		
		# send command to vehicle
		self.vehicle.send_mavlink(msg)
		
		# Always call flush to guarantee that previous writes to the vehicle have taken place
        self.vehicle.flush()
        
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
            if self.panoType == AUTOPAN_VIDEO:
                buttonMgr.setArtooButton(btn_msg.ButtonB, shots.APP_SHOT_AUTOPAN, btn_msg.ARTOO_BITMASK_ENABLED, "Video\0")
            elif self.panoType == AUTOPAN_PHOTO:
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
                    self.resetPano()
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
            #clear Pano Video yaw speed
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

        self.camPitch += value * PANO_PITCH_SPEED * UPDATE_TIME
        
        if self.camPitch > 0.0:
            self.camPitch = 0.0
        elif self.camPitch < -90:
            self.camPitch = -90
            
    def manualYaw(self, stick):
        if stick == 0:
            return
        self.camYaw += stick * PANO_YAW_SPEED * UPDATE_TIME
        if stick > 0:
            self.camDir = 1
        else:
            self.camDir = -1
        
        self.camYaw = location_helpers.wrapTo360(self.camYaw)
    
    def handlePitchYaw(self):
        '''Send pitch and yaw commands to gimbal or fixed mount'''
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
        
    def enterPhotoMode(self):
        # switch into photo mode if we aren't already in it
        self.shotmgr.goproManager.sendGoProCommand(mavutil.mavlink.GOPRO_COMMAND_CAPTURE_MODE, (CAPTURE_MODE_PHOTO, 0 ,0 , 0))

    def resume_from_brake(self):
        pass

```

TBD

