import time, gc, os
import pwmio
import board
from adafruit_motor import servo

import feathers3
from sensors import Sensors
from flight_status import FlightStatus
from logger import Logger
from apogee_prediction import ApogeePrediction

from digitalio import DigitalInOut, Direction, Pull


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
        
        self.btn = DigitalInOut(board.IO33)
        self.btn.direction = Direction.INPUT
        self.btn.pull = Pull.UP

        pwm = pwmio.PWMOut(board.A2, frequency=50)
        pwm.duty_cycle = 1500
        self.motor = servo.ContinuousServo(pwm, min_pulse=1000, max_pulse=2000)
        
        self.flight_status = FlightStatus()
        self.sensors = Sensors()
        
        self.logger = Logger()
        
        self.apg1 = ApogeePrediction()
        self.apg2 = ApogeePrediction()
        
        feathers3.set_ldo2_power(True)
        feathers3.set_neopixel_color(0,0,255)

    def print_data_header():
        print(f"{'Time':<15} {'Acceleration':<40} {'Gyro':<45} {'Altitude':<10}")
    
    def print_data(self, sensor_data):
        current_time = time.time()
        sensor_data = self.sensors.get_sensor_data()
        print(f"{current_time:<15} {str(list(sensor_data['acceleration'])):<40} {str(list(sensor_data['gyro'])):<45} {sensor_data['altitude']:<10}")

    def main(self):
        last_poll = time.monotonic_ns()
        start_time = time.monotonic_ns()
        
        armed = False
        while not armed:
            if self.btn.value:
                armed = True
        
        headers = ['time', 'accelx', 'accely', 'accelz', 'gyrox', 'gyroy', 'gyroz', 'magx', 'magy', 'magz', 'altitude', 'pressure', 'temp', 'apogee1', 'apogee2', 'apogee3', 'apogee4', 'flightStage']
        self.logger.set_headers(headers)
        
        # feathers3.toggle_led()
        feathers3.set_neopixel_color(0,255,0)
        print("!ARMED!")
        print(f"Started: {start_time/10**9}")
        finished = False
        while True:
            if last_poll + (0.03125 * 10**9) <= time.monotonic_ns():
                last_poll = time.monotonic_ns()
                telemetry = self.sensors.get_sensor_data()
                self.flight_status.new_telemetry(telemetry)
                
                apogee1, apogee2, apogee3, apogee4 = 0, 0, 0, 0
                
                # if(self.flight_status.current_stage().value == 2):
                # Switch X and Z Values
                apogee1, apogee2 = self.apg1.predict_apogee(telemetry['altitude'], telemetry['acceleration'][0])
                apogee3, apogee4 = self.apg2.predict_apogee(telemetry['altitude'], telemetry['acceleration'][0] + telemetry['acceleration'][1] + telemetry['acceleration'][2])
                if(self.flight_status.current_stage().value == 4):
                    finished = True
                    feathers3.set_neopixel_color(255,0,0)
                
                self.logger.log_data([str(d) for d in [last_poll, telemetry['acceleration'][0], telemetry['acceleration'][1], telemetry['acceleration'][2], telemetry['gyro'][0], telemetry['gyro'][1], telemetry['gyro'][2], telemetry['mag'][0], telemetry['mag'][1], telemetry['mag'][2], telemetry['altitude'], telemetry['pressure'], telemetry['temp'], apogee1, apogee2, apogee3, apogee4, self.flight_status.current_stage_name()]])
                print(f"Pulled Data at {time.monotonic_ns() / 10**9}")
            
        print("Finished: {}".format(time.monotonic_ns()))
        
