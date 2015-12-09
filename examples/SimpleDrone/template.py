'''
template.py
This program is a template for using SimpleDrone.

'''
from dronekit import *
from SimpleDrone import SimpleDrone

SIM = True

print "connecting to drone..."
if SIM:
    vehicle = connect('127.0.0.1:14551', wait_ready=True)
else:
    vehicle = connect('0.0.0.0:14550', wait_ready=True) # connecting from GCS
    #vehicle = connect('udpout:127.0.0.1:14560', wait_ready=True) #connecting from onboard solo


sd = SimpleDrone(vehicle)
sd.take_control()

if SIM:
    #arm and takeoff drone - DO NOT USE THIS ON A REAL DRONE ONLY IN SIMULATION
    if vehicle.armed == False:
        # Don't let the user try to arm until autopilot is ready
        print " Waiting for vehicle to initialise..."
        while not vehicle.is_armable:
            time.sleep(1)
        vehicle.armed   = True
        print 'Vehicle Armed'
    sd.takeoff()

try:
    '''
    YOUR CODE HERE
    '''

finally:
    sd.release()
