'''
virtualjoystick.py
This program will allow you to control solo's xy using an on screen joystick.
It is designed to be run on a GCS.
It utilizes DroneDirect which allows for directional control using dronekit
Note: It is very twitchy and will have kickback
Programming exercise:
Implement a better velocity decay
'''
import pygame
from dronekit import *
from dronedirect import DroneDirect
import time
import math


def draw_joystick(center, stick, radius):
    #draw virtual joystick
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, (0, 0, 255), center, stick, 2)
    pygame.draw.circle(screen, (0, 255, 0), center, radius, 2)
    pygame.display.flip()


SIM = True
JOYSTICK_FEEL = 2.0
DECAY = 0.7

running = True
width, height = 300, 300
radius = width / 3
down = False
screen = pygame.display.set_mode((width, height))
center = width / 2, height / 2
joy = width / 2, height / 2
last_decay = 0
draw_joystick(center, joy, radius)

print "connecting to drone..."
if SIM:
    vehicle = connect('127.0.0.1:14551', wait_ready=True)
else:
    vehicle = connect('0.0.0.0:14550', wait_ready=True)

sd = DroneDirect(vehicle, joystick_feel=JOYSTICK_FEEL)
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

x, y = 0, 0
try:
    while running:
        #read user input
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            center = event.pos
            joy = event.pos
            down = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            down = False
            joy = width / 2, height / 2
            center = width / 2, height / 2
        elif event.type == pygame.MOUSEMOTION and down:
            joy = event.pos

        if down:
            #Normilize joystick commands
            x = (joy[0] - width / 2.0) / radius
            y = -(joy[1] - height / 2.0) / radius

        else:  #decay the values after stick release
            if time.time() - last_decay > .1:
                x = x * DECAY
                y = y * DECAY
                last_decay = time.time()

        draw_joystick(center, joy, radius)
        sd.move(x=x, y=y, z=0)

finally:
    sd.release()
