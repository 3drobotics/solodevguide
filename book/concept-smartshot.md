# Smart Shots

[Smart shots](http://3drobotics.com/smart-shots/) allow you to pre-program complicated flight paths, enabling users to concentrate on when to take the shot rather than how to fly the vehicle.

The Smart Shot framework builds upon DroneKit, and adds support to pause and resume shots (storing the flight state) and re-map controller buttons and sticks during a shot.

The most important functions in the `solo.smartshot` are:

* *Handling RC input.* Remapping the control sticks to perform alternate functions. For example, this is used in Cable Cam to allow the right stick to control Solo's position along the virtual cable instead of its position relative to earth.
* *Buttons.* A and B can be mapped to provide shortcuts like setting fixed waypoints or recording a position.
* *Resume from brake.* When the pause button is pressed, the drone goes into BRAKE mode and the flight state is lost. This function is called after five seconds to restore the flight mode state and prepare the shot to continue once the user resumes controlling Solo.

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
