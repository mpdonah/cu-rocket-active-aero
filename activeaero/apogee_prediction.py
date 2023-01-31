from time import sleep
import time
import math
from math import cos
from math import sin
import numpy as np


# Constants to be set prior to flight
mass = 1.966023     # Mass of rocket + empty motor, needs to be calculated prior to each flight
area = 0.0049483 # Cross-sectional area of tube, in m^2
rho = 1.22      # Air density, going to be constant at low altitudes but will need to be calculated for IREC
k = 0.5 * rho * 0.58 * area # Wind resistance

# Following lines need to be replaced with whatever the code uses to gather sensor data
pressure = 900      # Air pressure, line needs to be replaced with whatever the microcontroller uses
az = 1 # acceleration vector on z component, whichever side of the sensor faces up
ax = 0 # acceleration vector on x component, whichever side is the roll axis
ay = 0 # acceleration vector on y component, whichever side is the pitch axis
opit = 0 # pitch orientation
orol = 0 # roll orientation       all orientation in radians
oyaw = 0 # yaw orientation

t = 0       # Needs to be set so pressing a push button will set this off

# Following code is running in "armed" state

looptime = round(time.time() * 1000)
state = 'launchpad'
curaltm = 0
curvelpres = 0
curvelacc = 0

while t == 0:       # Keeps in flight mode

    lasttime = looptime
    looptime = round(time.time() * 1000)
    timedif = (looptime - lasttime)/1000


    # Altitude calculations
    if state is 'launchpad':
        alt = (288.15/-0.0065 * (((pressure/1013.25)**0.1903)-1))               # Base altitude, or whatever altitude the rocket starts at
        curvel = 0                                                              # Base altitude constantly adjusted at launchpad to prevent drift in readings
    lastalt = curaltm
    curaltm = (288.15/-0.0065 * (((pressure/1013.25)**0.1903)-1)) - alt         # Current altitude relative to launchpad
    curalt = curaltm * 3.28
    if state is not 'launchpad':
        lastvelpres = curvelpres
        curvelpres = ((curalt - lastalt)/timedif + lastvelpres)/2


    azvect = az*sin(opit) + ay*cos(opit)*sin(orol) + ax*cos(opit)*cos(orol)     # True vertical acceleration, if the code is set up correctly, any orientation should register 1g of acceleration
    apaz = (azvect-1)*9.81                                                      # True vertical acceleration, removes normal force from accelerometer
    if apaz < 0.01 or apaz > -0.01:
        apaz = 0
    lastvelacc = curvelacc
    curvelacc = apaz * timedif + lastvelacc                                           # Calculates the vertical velocity


    appredone = 3.28*(mass / (2*k) * np.log((mass*9.8+curvelacc**2)/(mass*9.8))) + curalt   # First apogee prediction, uses velocity from accelerometer
    appredtwo = 3.28*(mass / (2*k) * np.log((mass*9.8+curvelpres**2)/(mass*9.8))) + curalt  # Second apogee prediction, uses velocity from altitude


    if state is 'launchpad':            # Rocket on launchpad
        timeint = 5000              # Printing interval on launchpad, set to 5 seconds
        if az > 1.1:                    # az needs to detect over 1.1 gees, only possible if the pi were to accelerate upwards
            state = 'launch'
    if state is 'launch':
        timeint = 100               # Printing interval during flight, set to 0.1 seconds
        if az < 0:
            state = 'ascent'
    if state is 'ascent':           # Climbing altitude with motor off
        if curaltm < lastalt:                      # Check if altitude drops
            apcheck = apcheck + 1
        else:
           apcheck = 0
        if apcheck > 5:                            # Needs 5 consecutive drops in altitude to switch states
            state = 'descent'
    if state is 'descent':           # Beginning descent, drogue deployed
        if curalt < 50 and azvect < 1.1:                  # Altitude needs to be less than 50ft above launchsite and standard vertical acceleration sustained
            if curtimer - startimer > 15000:              # 10 second timer placed in case of false positive, IREC descent at least 20 seconds after main chute
                state = 'landed'                          # It's likely the sensors will think the landing has been reached prior to the actual touchdown
                startimer = round(time.time() * 1000)                        # the timer will reset to ensure the rocket is landed and not slowly descending, steady descent means 0 acceleration, same as landed
                curtimer = round(time.time() * 1000)
            else:
                curtimer = round(time.time() * 1000)
        else:
            startimer = round(time.time() * 1000)           # Timer resets if azvect > 1.1 or curalt > 50
            curtimer = round(time.time() * 1000)
    if state is 'landed':           # Touchdown
        curtimer = round(time.time() * 1000)        # No timestamps here, landing will always last for 10 seconds
        timeint = 1000              # Printing interval once landed, set to 1 second
        if curtimer - startimer > 10000:              # Idling for 10 seconds in this state ends the program
            t = 1   # ends flight state

print("end")

# STILL NEEDED:
# Sensors need to be all added in
# Data needs to be recorded to some file, all sensor data, curalt, curvelacc, curvelpres, appredone, appredtwo
# With data recording, I'd like to use the time interval stuff again to prevent clogging of files
# Push button code to 'arm' the system, I'm also thinking we put a little light in to check if it's armed too

