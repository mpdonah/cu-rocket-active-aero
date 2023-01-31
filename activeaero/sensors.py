import board
import time

from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
from adafruit_lis3mdl import LIS3MDL
import adafruit_bmp3xx

class Sensors():
    def __init__(self):
        self.i2c = board.I2C()  # uses board.SCL and board.SDA
        self.sox = LSM6DSOX(self.i2c)
        # mag = LIS3MDL(i2c, address=0x1E)
        self.bmp = adafruit_bmp3xx.BMP3XX_I2C(self.i2c)
        self.base_altitude = 0
        self.set_base_altitude()

    def set_base_altitude(self):
        for _ in range(64):
            self.base_altitude += self.bmp.altitude
            time.sleep(0.1)
        self.base_altitude /= 64
    
    def get_sensor_data(self):
        data = {
            'acceleration': self.sox.acceleration,
            'gyro': self.sox.gyro,
            'altitude': self.bmp.altitude - self.base_altitude,
            'pressure': self.bmp.pressure,
            # 'magnetic': self.mag.magnetic,
        }
        
        return data
