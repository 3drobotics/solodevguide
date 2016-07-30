# Smart Shots

[Smart shots](http://3drobotics.com/smart-shots/) allow you to pre-program complicated flight paths, enabling users to concentrate on when to take the shot rather than how to fly the vehicle.

The Smart Shot framework builds upon DroneKit, and adds support to pause and resume shots (storing the flight state) and re-map controller buttons and sticks during a shot.

The most important functions in the `solo.smartshot` are:

* *Handling RC input.* Remapping the control sticks to perform alternate functions. For example, this is used in Cable Cam to allow the right stick to control Solo's position along the virtual cable instead of its position relative to earth.
* *Buttons.* A and B can be mapped to provide shortcuts like setting fixed waypoints or recording a position.

Since there isn't a framework to implement custom Smart Shots, to intall a custom Smart Shot, you must override an existing flight mode. In this example, our custom Smart Shot called AutoPan, will override the Sport Flight Mode.

Prerequisites

* Enable Advanced Flight Modes
* Map Sport to Button A or Button B

To install a custom smart shot requires modification to the following files:

* modes.py
* shotManager.py
* shots.py

You also need to install your custom smart shot python script (i.e. autopan.py) to /usr/bin on the Solo.

**Note**: When updating solo to a newer version, the update process will ignore modified files, so be sure to backup any changed files and restore prior to updating. Otherwise you will have to perform a factory reset. Also, depending on the firmware version installed on your Solo, the code in modes.py, shotManager.py and shots.py may vary from this example.

Step 1. Modify modes.py

modes.py is the mapping between Pixhawk Flight Modes and what is displayed on the controller. Change **Sport** to **Autopan**.

```
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

Step 2. Modify shotManager.py

shotManager.py manages the SmartShots. Add an import for your custom smart shot, add an entry to handle the button press mapped to your custom smart shot, and an entry in the handleButtons function trigger the smart shot.

Add an import for autopan at the top of shotManager.py. It can be anywhere at the top as long as it is with the other imports.

```
    from GoProConstants import *
    import GoProManager
    import infiniCable
    import location_helpers
    import modes
    import orbit
    import autopan
    import RCRemapper
    import selfie
    import shotLogger
    import shots
    from shotManagerConstants import *
```

Add an entry in def handleButtons to handle the button press mapped to Autopan.

```
def handleButtons(self):
    buttonEvent = self.buttonManger.checkButtons()

    if buttonEvent is None:
        return

    button, event = buttonEvent.

```

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
