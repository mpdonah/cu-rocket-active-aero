import board
import time

from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
from adafruit_lsm6ds import AccelRange
from adafruit_lis3mdl import LIS3MDL, Rate
from adafruit_bmp3xx import BMP3XX_I2C

class Sensors():
    def __init__(self):
        self.i2c = board.I2C()  # uses board.SCL and board.SDA
        self.sox = LSM6DSOX(self.i2c)
        self.mag = LIS3MDL(self.i2c, address=0x1C)
        self.bmp = BMP3XX_I2C(self.i2c)
        self.base_altitude = 0
        self.set_base_altitude()
        
        self.sox.accelerometer_range = AccelRange.RANGE_16G

    def set_base_altitude(self):
        for _ in range(64):
            self.base_altitude += self.bmp.altitude
            time.sleep(0.1)
        self.base_altitude /= 64
    
    def get_sensor_data(self):
        try:
            accel = self.sox.acceleration
        except:
            print("Failed to read Accelerometer")
            accel = (0, 0, 0)
        
        try:
            gyro = self.sox.gyro
        except:
            print("Failed to read Gyroscope")
            gyro = (0, 0, 0)
        
        try:
            alt = self.bmp.altitude
            pressure = self.bmp.pressure
            temp = self.bmp.temperature
        except:
            print("Failed to read Barometer")
            alt = self.base_altitude
            pressure = 0
            temp = 0
            
        
        try:
            mag = self.mag.magnetic
        except:
            print("Failed to read Magnetometer")
            mag = (0, 0, 0)
        
        data = {
            'acceleration': accel,
            'gyro': gyro,
            'altitude': alt - self.base_altitude,
            'pressure': pressure,
            'temp': temp,
            'mag': mag,
        }
        
        return data
