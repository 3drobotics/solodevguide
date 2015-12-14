
import math
from dronekit import *
from pymavlink.mavutil import mavlink
import time
import threading
import sys


class SimpleDrone():


    def __init__(self,vehicle,joystick_feel = 2.0, update_rate = 15):
        self.vehicle = vehicle
        self.joystick_feel = joystick_feel
        self.fence_breach = False
        self.last_send_point = 0
        self.last_send_move = 0
        self.last_send_translate = 0
        self.update_rate = update_rate

    def take_control(self):
        print "Requesting Control.."
        self.vehicle.mode = VehicleMode("GUIDED")
        while self.vehicle.mode != "GUIDED":
            time.sleep(0.1)
        print "Control granted"

    # move - Send the copter flying in a direction - params: -1.0-1.0
    def move(self, x = 0, y = 0, z = 0):
        if self.fence_breach:
            raise StandardError("You are outside of the fence")
        if self.vehicle.mode != 'GUIDED':
            print '\033[91m' + "SimpleDroneError: 'move({0},{1},{2})' was not executed. Vehicle was not in GUIDED mode".format(x,y,z) + '\033[0m'
            return
        #limit our update rate
        if (time.time() - self.last_send_move) < 1.0/self.update_rate:
            return
        x = max(min(x,1),-1) * self.joystick_feel
        y = max(min(y,1),-1) * self.joystick_feel
        z = max(min(z,1),-1) * self.joystick_feel
        yaw = self.vehicle.attitude.yaw #radians

        #rotate to earth-frame angles and scale
        vx_ef = (y*math.cos(yaw) - x*math.sin(yaw))
        vy_ef = (y*math.sin(yaw) + x*math.cos(yaw))
        vz_ef = -z

        # create the SET_POSITION_TARGET_LOCAL_NED command
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
                                                     0,       # time_boot_ms (not used)
                                                     0, 0,    # target system, target component
                                                     mavlink.MAV_FRAME_LOCAL_NED, # frame
                                                     0x01C7,  # type_mask (ignore pos | ignore acc)
                                                     0, 0, 0, # x, y, z positions (not used)
                                                     vx_ef, vy_ef, vz_ef, # x, y, z velocity in m/s
                                                     0, 0, 0, # x, y, z acceleration (not used)
                                                     0, 0)    # yaw, yaw_rate (not used)

        # send command to vehicle
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()
        self.last_send_move = time.time()
        print "Moving..."


    # brake - Stop the copter moving
    def brake(self):
        mode = self.vehicle.mode
        msg  = self.vehicle.message_factory.set_mode_encode(0,
                                                mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                                                17)
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()
        self.vehicle.mode = mode

    # point - Point the copter in a direction
    def point(self,degrees, relative = True):

        if self.fence_breach:
            raise StandardError("You are outside of the fence")
        if self.vehicle.mode != 'GUIDED':
            print '\033[91m' + "SimpleDroneError: 'point({0})' was not executed. Vehicle was not in GUIDED mode".format(degrees) + '\033[0m'
            return
        #limit our update rate
        if (time.time() - self.last_send_point) < 1.0/self.update_rate:
            return
        if relative:
            is_relative=1 #yaw relative to direction of travel
        else:
            is_relative=0 #yaw is an absolute angle

        if degrees !=0:
            direction = int(degrees/abs(degrees))
        else:
            direction = 1
        degrees = degrees % 360
        # create the CONDITION_YAW command using command_long_encode()
        msg = self.vehicle.message_factory.command_long_encode(
            0, 0,    # target system, target component
            mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
            0, #confirmation
            degrees,    # param 1, yaw in degrees
            0,          # param 2, yaw speed deg/s
            direction,          # param 3, direction -1 ccw, 1 cw
            is_relative, # param 4, relative offset 1, absolute angle 0
            0, 0, 0)    # param 5 ~ 7 not used
        # send command to vehicle
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()
        self.last_send_point = time.time()

    # rotate - Rotate the copter in a direction. Currently not supported by arducopter
    def rotate(self,input):
        pass

    # step_left - Send the copter left some distance - params: distance meters
    def translate(self, x = 0, y = 0, z = 0,wait_for_arrival = False,dist_thres = 0.3):
        if self.fence_breach:
            raise StandardError("You are outside of the fence")
        if self.vehicle.mode != 'GUIDED':
            print '\033[91m' + "SimpleDroneError: 'translate({0},{1},{2})' was not executed. Vehicle was not in GUIDED mode".format(x,y,z) + '\033[0m'
            return
        #limit our update rate
        if (time.time() - self.last_send_translate) < 1.0/self.update_rate:
            return
        yaw = self.vehicle.attitude.yaw #radians
        location = self.vehicle.location.global_relative_frame #latlon

        #rotate to earth-frame angles
        x_ef = y*math.cos(yaw) - x*math.sin(yaw)
        y_ef = y*math.sin(yaw) + x*math.cos(yaw)

        latlon_to_m = 111319.5   # converts lat/lon to meters
        lat = x_ef / latlon_to_m + location.lat
        lon = y_ef / latlon_to_m + location.lon
        alt = z + location.alt


        msg = self.vehicle.message_factory.set_position_target_global_int_encode(
                                                    0,       # time_boot_ms (not used)
                                                    0, 0,    # target system, target component
                                                    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
                                                    0b0000111111111000, # type_mask (only speeds enabled)
                                                    lat*1e7, # lat_int - X Position in WGS84 frame in 1e7 * meters
                                                    lon*1e7, # lon_int - Y Position in WGS84 frame in 1e7 * meters
                                                    alt, # alt - Altitude in meters in AMSL altitude, not WGS84 if absolute or relative, above terrain if GLOBAL_TERRAIN_ALT_INT
                                                    0, # X velocity in NED frame in m/s
                                                    0, # Y velocity in NED frame in m/s
                                                    0, # Z velocity in NED frame in m/s
                                                    0, 0, 0, # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
                                                    0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

        # send command to vehicle
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()
        self.last_send_translate = time.time()
        self.point(0)
        print "translating..."
        if wait_for_arrival:
            while self.vehicle.mode == "GUIDED":
                veh_loc = self.vehicle.location.global_relative_frame
                diff_lat_m = (lat - veh_loc.lat) * latlon_to_m
                diff_lon_m = (lon - veh_loc.lon) * latlon_to_m
                diff_alt_m = alt - veh_loc.alt
                dist_xyz = math.sqrt(diff_lat_m**2 + diff_lon_m**2 + diff_alt_m**2)
                if dist_xyz < dist_thres:
                    print "Arrived"
                    return
            print '\033[93m' + "SimpleDroneError: 'translate({0},{1},{2})' was interrupted. Vehicle was switched out of GUIDED mode".format(x,y,z) + '\033[0m'

    # takeoff - takeoff to some altitude, needs armed status - params: meters
    def takeoff(self, altitude_meters=3):
        if self.vehicle.mode != 'GUIDED':
            print '\033[91m' + "SimpleDroneError: 'takeoff({0})' was not executed. Vehicle was not in GUIDED mode".format(altitude_meters) + '\033[0m'
            return

        while not self.vehicle.armed:
            print " Waiting for arming..."
            time.sleep(1)

        print "Taking off..."
        if self.vehicle.system_status != SystemStatus('STANDBY'):
            print "Already airborne"
            return
        self.vehicle.simple_takeoff(altitude_meters)
        # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
        #  after Vehicle.simple_takeoff will execute immediately).
        while self.vehicle.mode == 'GUIDED':
            #Break and return from function just below target altitude.
            if self.vehicle.location.global_relative_frame.alt>=altitude_meters*0.95:
                print "Takeoff Complete"
                return
            time.sleep(1)
        print '\033[93m' + "SimpleDroneError: 'takeoff({0})' was interrupted. Vehicle was swicthed out of GUIDED mode".format(altitude_meters) + '\033[0m'


    # RTH - return to home
    def RTH(self):
        self.vehicle.mode = VehicleMode("RTL")

    # enable_fence - Activate a safe operating zone - params: meters, meters, radius of cylinder in meters
    def enable_fence(self, alt_floor, alt_ceiling ,radius):
        self.fence_enabled = True
        self.fence_floor = alt_floor
        self.fence_ceiling = alt_ceiling
        self.fence_radius = radius
        fence_thread = threading.Thread(target = self._enforce_fence)
        fence_thread.start()

    #disble_fence - Disble the geo fence
    def disble_fence(self):
        self.fence_enabled = False
        self.fence_breach = False

    def _enforce_fence(self):
        while self.fence_enabled and self.vehicle.mode == "GUIDED":
            try:
                veh_loc = self.vehicle.location.global_relative_frame
                home_loc = self.vehicle.home_location
                if home_loc is None:
                    cmds = self.vehicle.commands
                    cmds.download()
                    cmds.wait_ready()
                    home_loc = self.vehicle.home_location

                latlon_to_m = 111319.5   # converts lat/lon to meters
                dist_xy_home = math.sqrt(((home_loc.lat - veh_loc.lat) * latlon_to_m)**2 +((home_loc.lon - veh_loc.lon) * latlon_to_m)**2)
                if dist_xy_home >= self.fence_radius or veh_loc.alt < self.fence_floor or veh_loc.alt > self.fence_ceiling:
                    self.brake()
                    self.fence_breach = True
                    print '\033[91m' + "Fence Breach! Braking" + '\033[0m'
                    time.sleep(1)
                    break
            except:
                pass

            time.sleep(0.1)

    def release(self):
        print "Releasing control and Braking vehicle"
        self.disble_fence()
        self.brake()
        time.sleep(1)
