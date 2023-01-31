import time, gc, os
import pwmio
import board
from adafruit_motor import servo

import feathers3
from sensors import Sensors
from flight_status import FlightStatus

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
        
        self.flight_status = FlightStatus()
        self.sensors = Sensors()

    def print_data_header():
        print(f"{'Time':<15} {'Acceleration':<40} {'Gyro':<45} {'Altitude':<10}")
    
    def print_data(self, sensor_data):
        current_time = time.time()
        sensor_data = self.sensors.get_sensor_data()
        print(f"{current_time:<15} {str(list(sensor_data['acceleration'])):<40} {str(list(sensor_data['gyro'])):<45} {sensor_data['altitude']:<10}")

    def main(self):
        last_poll = time.monotonic_ns()
        start_time = time.monotonic_ns()
        pulls = 0
        print(f"Started: {start_time/10**9}")
        while start_time + 10*10**9 > time.monotonic_ns():
            if last_poll + 62500000 < time.monotonic_ns():
                last_poll = time.time()
                self.flight_status.add_altitude(self.sensors.get_sensor_data()['altitude'])
                pulls += 1
        print(f"Ended: {(time.monotonic_ns() - start_time)/10**9}")
        print(pulls / 10)
