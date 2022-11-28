#FeatherS3 Helper Library
# 2022 Seon Rozenblum, Unexpected Maker
#
# Project home:
#   https://feathers3.io
#

# Import required libraries
import time
import neopixel
import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn

# Init Blink LED
led13 = DigitalInOut(board.LED)
led13.direction = Direction.OUTPUT

# Init LDO2 Pin
ldo2 = DigitalInOut(board.LDO2)
ldo2.direction = Direction.OUTPUT

# Setup the BATTERY voltage sense pin
vbat_voltage = AnalogIn(board.BATTERY)

# Setup the VBUS sense pin
vbus_sense = DigitalInOut(board.VBUS_SENSE)
vbus_sense.direction = Direction.INPUT

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3, auto_write=True, pixel_order=neopixel.RGB)

   
# Helper functions

def toggle_led():
    """Set the internal LED IO13 to it's inverse state"""
    led13.value = not led13.value

def led_set( state ):
    """Set the internal LED IO13 to this state"""
    led13.value = state

def set_neopixel_color( r, g, b ):
    """Set the onboard NeoPixel to this colour"""
    pixel[0] = ( r, g, b, 0.5)

def set_ldo2_power(state):
    """Enable or Disable power to the onboard NeoPixel to either show colour, or to reduce power fro deep sleep."""
    global ldo2
    ldo2.value = state
    
def get_battery_voltage():
    """Get the approximate battery voltage."""
    # I don't really understand what CP is doing under the hood here for the ADC range & calibration,
    # but the onboard voltage divider for VBAT sense is setup to deliver 1.1V to the ADC based on it's
    # default factory configuration.
    # This forumla should show the nominal 4.2V max capacity (approximately) when 5V is present and the
    # VBAT is in charge state for a 1S LiPo battery with a max capacity of 4.2V   
    global vbat_voltage
    return (vbat_voltage.value / 5371)

def get_vbus_present():
    """Detect if VBUS (5V) power source is present"""
    global vbus_sense
    return vbus_sense.value
    

