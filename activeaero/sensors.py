import board

from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
from adafruit_lis3mdl import LIS3MDL
import adafruit_bmp3xx

i2c = board.I2C()  # uses board.SCL and board.SDA
sox = LSM6DSOX(i2c)
mag = LIS3MDL(i2c, address=0x1E)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

def get_sensor_data():
    data = {
        'acceleration': sox.acceleration,
        'gyro': sox.gyro,
        'altitude': bmp.altitude,
        'pressure': bmp.pressure,
        # 'magnetic': mag.magnetic,
    }
    
    return data
