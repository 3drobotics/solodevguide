# Smart Shots

Smart Shots consist of several functions that provide a high-level interface for controlling the drone. The most important methods they provide:

* *Handling RC input.* Remapping the control sticks to do alternate functions is used, for example, in Cable Cam to allow the right stick to be 
* *Buttons.* A and B can be mapped to provide shortcuts like setting fixed waypoints or recording a position.
* *Resume from brake.* When the pause button is pressed, the drone goes into BRAKE mode and the flight state is lost. This function is called shortly afterward to restore the flight state and prepare the shot to continue.

<aside class="todo">
This guide does not yet document how to author your own Smart Shots, though this is being worked on. A conceptual API is shown below for how this will work. `vehicle` refers to a DroneKit API interface.
</aside>

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

    def resume_from_brake(self):
        pass
```
