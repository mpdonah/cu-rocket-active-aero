import time, gc, os
import pwmio
import board
from adafruit_motor import servo

import feathers3
import sensors

motor: servo.ContinuousServo

class ActiveAero():
    def __init__(self):
        self.setup()
    
    def setup(self):
        print("\Booting Active Aero Flight Controller!")
        print("------------------\n")

        print("Memory Info - gc.mem_free()")
        print("---------------------------")
        print("{} Bytes\n".format(gc.mem_free()))

        flash = os.statvfs('/')
        flash_size = flash[0] * flash[2]
        flash_free = flash[0] * flash[3]
        # Show flash size
        print("Flash - os.statvfs('/')")
        print("---------------------------")
        print("Size: {} Bytes\nFree: {} Bytes\n".format(flash_size, flash_free))
        print("---------------------------")
        
        pwm = pwmio.PWMOut(board.A2, frequency=50)
        pwm.duty_cycle = 1500
        self.motor = servo.ContinuousServo(pwm, min_pulse=1000, max_pulse=2000)


    def main(self):
        print(f"{'Time':<15} {'Acceleration':<40} {'Gyro':<45} {'Altitude':<10}")
        while True:
            current_time = time.time()
            sensor_data = sensors.get_sensor_data()
            print(f"{current_time:<15} {str(list(sensor_data['acceleration'])):<40} {str(list(sensor_data['gyro'])):<45} {sensor_data['altitude']:<10}")
            
            time.sleep(0.1)
