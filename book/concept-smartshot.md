# Smart Shots

[Smart shots](http://3drobotics.com/smart-shots/) allow you to pre-program complicated flight paths, enabling users to concentrate on when to take the shot rather than how to fly the vehicle.

The Smart Shot framework builds upon DroneKit, and adds support to pause and resume shots \(storing the flight state\) and re-map controller buttons and sticks during a shot.

The most important functions in the `solo.smartshot` are:

* _Handling RC input._ Remapping the control sticks to perform alternate functions. For example, this is used in Cable Cam to allow the right stick to control Solo's position along the virtual cable instead of its position relative to earth.
* _Buttons._ A and B can be mapped to provide shortcuts like setting fixed waypoints or recording a position.

Since there isn't a framework to implement custom Smart Shots, to intall a custom Smart Shot, you must override an existing flight mode. In this example, our custom Smart Shot called AutoPan, will override the Sport Flight Mode.

Prerequisites

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

**Step 2. Modify shotManager.py**

shotManager.py manages the SmartShots. Add an import for your custom smart shot, add an entry to handleButtons function to handle the button press mapped to your custom smart shot, and an entry to the triggerShot function the handleButtons function trigger the smart shot.

Add an import for autopan at the top of shotManager.py. It can be anywhere at the top as long as it is with the other imports.

```py
...
import modes
import orbit
import autopan
import RCRemapper
import selfie
```

Add an entry to the handleButtons function to handle the button press mapped to Autopan.

```py
def handleButtons(self):
        ...
        if self.currentShot == shots.APP_SHOT_NONE:
            if event == btn_msg.Press:
                if button == btn_msg.ButtonA or button == btn_msg.ButtonB:
                    # see what the button is mapped to
                    (shot, mode) = self.buttonManager.getFreeButtonMapping(button)

                    # hack to get pano
                    if (mode == 13):
                        logger.log("hack - mode: %s" % modes.MODE_NAMES[mode])
                        shot = shots.APP_SHOT_AUTOPAN

                    # only allow entry into these shots if the app is attached
                    allowedShots = [shots.APP_SHOT_ORBIT, shots.APP_SHOT_CABLECAM, shots.APP_SHOT_AUTOPAN]
        ...
```

Add an entry to triggerShot function

```py
def triggerShot(self, shot):
    # invalid shot!
    if shot not in shots.SHOT_NAMES:
        logger.log("[triggerShot]: Error, trying to trigger an invalid shot! %d"%(shot))
        return
    ...
    elif self.currentShot == shots.APP_SHOT_AUTOPAN:
        self.initStreamRates()
        self.curController = autopan.AutoPanController(self.vehicle, self)
    ...
```

TBD

```py
import solo
from dronekit.lib import VehicleMode, Location

class FlipShot(solo.smartshot):
    def __init__(self, vehicle, shotmgr):
        self.vehicle = vehicle
        self.shotmgr = shotmgr

    def handle_rcs(self, channels):
        pass

    def handle_button(self, button, event):
        pass
```

