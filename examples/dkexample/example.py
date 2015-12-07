from dronekit import connect, VehicleMode
import time

# Connect to UDP endpoint
vehicle = connect('udpin:0.0.0.0:14550', wait_ready=True)

# Wait for parameters to accumulate.
#time.sleep(5)

# Get all vehicle attributes (state)
print "\nGet all vehicle attribute values:"
print " Global Location: %s" % vehicle.location.global_frame
print " Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
print " Local Location: %s" % vehicle.location.local_frame
print " Attitude: %s" % vehicle.attitude
print " Velocity: %s" % vehicle.velocity
print " GPS: %s" % vehicle.gps_0
print " Mount status: %s" % vehicle.mount_status
print " Battery: %s" % vehicle.battery
print " EKF OK?: %s" % vehicle.ekf_ok
print " Last Heartbeat: %s" % vehicle.last_heartbeat
print " Rangefinder: %s" % vehicle.rangefinder
print " Rangefinder distance: %s" % vehicle.rangefinder.distance
print " Rangefinder voltage: %s" % vehicle.rangefinder.voltage
print " Heading: %s" % vehicle.heading
print " Is Armable?: %s" % vehicle.is_armable
print " System status: %s" % vehicle.system_status.state
print " Groundspeed: %s" % vehicle.groundspeed    # settable
print " Airspeed: %s" % vehicle.airspeed    # settable
print " Mode: %s" % vehicle.mode.name    # settable
print " Armed: %s" % vehicle.armed    # settable