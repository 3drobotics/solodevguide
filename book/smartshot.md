# Authoring a Smart Shot

TODO: Rebrand these probably, move out of /usr/bin

```py
from __future__ import print_function
from droneapi.lib import VehicleMode
from droneapi.lib import Location
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
import pathHandler
import roi
import shotLogger
import shots
from shotManagerConstants import *
import yawPitchOffsetter
# on host systems these files are located here
sys.path.append(os.path.realpath('../../flightcode/stm32'))
import btn_msg

class MyController():
    def __init__(self, vehicle, shotmgr):
        self.vehicle = vehicle
        self.shotmgr = shotmgr

    def handleRCs( self, channels ):
    	pass

    def handleButton(self, button, event):
        pass

    def handleOptions(self, options):
        pass

    def setButtonMappings(self):
        pass

    def updateAppOptions(self):
        pass

    def resumeFromBrake(self):
        pass

    def setupTargeting(self):
        pass
```

Then use [DroneKit Python](https://python.dronekit.io/).
