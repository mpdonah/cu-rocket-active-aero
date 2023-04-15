# from activeaero import ActiveAero

# def main():
#     active_aero = ActiveAero()
#     active_aero.main()
    

# main()

import time
import board
import pwmio
from adafruit_motor import servo

# create a PWMOut object on Pin A2.
pwm = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
my_servo = servo.Servo(pwm)

while True:
    while True:
        angle = input("Enter an angle between 0 and 180: ")
        angle = int(angle)
        my_servo.angle = angle

