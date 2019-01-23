'''
helloworld.py
This program will draw 3DR in the sky. It is designed to be run onboard solo.
It utilizes SimpleDrone which allows for directional control using dronekit
Default size(scale = 1.0) is 4.4x2 meters. Change the scale factor to increase size.
Programming exercise:
Switch y and z axis to make a cool night writing program.
'''

from dronekit import *
from SimpleDrone import SimpleDrone
import time

SIM = False


def translate(x=0, y=0, z=0):
    scale = 1.0
    sd.translate(x=x * scale, y=y * scale, z=z * scale, wait_for_arrival=True)


print "connecting to drone..."
if SIM:
    vehicle = connect('127.0.0.1:14551', wait_ready=True)
else:
    vehicle = connect('udpout:127.0.0.1:14560', wait_ready=True)

sd = SimpleDrone(vehicle)
sd.take_control()

if SIM:
    #arm and takeoff drone - DO NOT USE THIS ON A REAL DRONE ONLY IN SIMULATION
    if vehicle.armed == False:
        # Don't let the user try to arm until autopilot is ready
        print " Waiting for vehicle to initialise..."
        while not vehicle.is_armable:
            time.sleep(1)
        vehicle.armed = True
        print 'Vehicle Armed'
    sd.takeoff()

try:
    #3
    translate(x=1.0)
    translate(x=-1.0, y=-1.0)
    translate(x=0.7)
    translate(x=0.3, y=-0.5)
    translate(x=-0.3, y=-0.5)
    translate(x=-0.7)

    #D
    translate(x=0.7)
    translate(x=1.0, y=1.0)
    translate(y=-1.0)
    translate(x=0.5)
    translate(x=0.5, y=1.0)
    translate(x=-0.5, y=1.0)
    translate(x=-0.5)

    #R
    translate(x=2.4)
    translate(x=0.3, y=-0.5)
    translate(x=-0.3, y=-0.5)
    translate(x=-0.7)
    translate(x=1, y=-1)

finally:
    sd.release()
