from time import sleep
import time
import math
from math import cos
from math import sin
from ulab import numpy as np


# Constants to be set prior to flight
mass = 2.132     # Mass of rocket + empty motor, needs to be calculated prior to each flight
area = 0.0049483 # Cross-sectional area of tube, in m^2
rho = 1.22      # Air density, going to be constant at low altitudes but will need to be calculated for IREC
k = 0.5 * rho * 0.58 * area # Wind resistance

# Following lines need to be replaced with whatever the code uses to gather sensor data


t = 0       # Needs to be set so pressing a push button will set this off

# Following code is running in "armed" state

class ApogeePrediction():
    def __init__(self):
        self.looptime = round(time.monotonic_ns() / 10**9 * 10**3)
        self.lastalt = 0
        self.curaltm = 0
        self.curvelacc = 0
        self.lastvelpres = 0

    def predict_apogee(self, curalt, az):#, ax, ay, opit, orol):
        lasttime = self.looptime
        self.looptime = round(time.monotonic_ns() / 10**9 * 10**3)
        timedif = (self.looptime - lasttime)/1000
        curvelpres = ((curalt - self.lastalt)/timedif + self.lastvelpres)/2
        self.lastalt = curalt

        # azvect = az*sin(opit) + ay*cos(opit)*sin(orol) + ax*cos(opit)*cos(orol)     # True vertical acceleration, if the code is set up correctly, any orientation should register 1g of acceleration
        azvect = az
        apaz = (azvect-1)                                                      # True vertical acceleration, removes normal force from accelerometer
        if apaz < 0.01 or apaz > -0.01:
            apaz = 0
        lastvelacc = self.curvelacc
        self.curvelacc = apaz * timedif + lastvelacc                                           # Calculates the vertical velocity

        appredone = (mass / (2*k) * np.log((mass*9.8+self.curvelacc**2)/(mass*9.8))) + curalt   # First apogee prediction, uses velocity from accelerometer
        appredtwo = (mass / (2*k) * np.log((mass*9.8+curvelpres**2)/(mass*9.8))) + curalt  # Second apogee prediction, uses velocity from altitude
        
        self.lastvelpres = curvelpres
        
        return appredone, appredtwo


    # STILL NEEDED:
    # Sensors need to be all added in
    # Data needs to be recorded to some file, all sensor data, curalt, self.curvelacc, curvelpres, appredone, appredtwo
    # With data recording, I'd like to use the time interval stuff again to prevent clogging of files
    # Push button code to 'arm' the system, I'm also thinking we put a little light in to check if it's armed too

