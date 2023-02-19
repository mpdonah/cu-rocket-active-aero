from ulab import numpy as np

class Stage():
    PRE_FLIGHT = 1
    IN_FLIGHT = 2
    DESCENT = 3
    ON_GROUND = 4
    
    def __init__(self, value: int = 1):
        self.value = value
        self.name = self.name()
    
    def name(self) -> str:
        if self.value == Stage.PRE_FLIGHT:
            return "PRE_FLIGHT"
        elif self.value == Stage.IN_FLIGHT:
            return "IN_FLIGHT"
        elif self.value == Stage.DESCENT:
            return "DESCENT"
        elif self.value == Stage.ON_GROUND:
            return "ON_GROUND"
        else:
            return "UNKNOWN"
    

class FlightStatus:
    def __init__(self):
        self.stage = Stage()
        self.altitude_list = []
    
    def current_stage(self) -> int:
        """Returns the current stage of the rocket.
        Returns:
            Stage: The current stage of the rocket.
        """
        return self.stage
    
    def current_stage_name(self) -> str:
        """Returns the current stage of the rocket as a string.
        Returns:
            str: The current stage of the rocket as a string.
        """
        return self.stage.name

    def add_altitude(self, altitude: float) -> None:
        """Adds an altitude to the altitude list and sets the current altitude.
        
        Args:
            altitude (float): The altitude to add to the list.
        """
        self.altitude_list.append(altitude)
        if len(self.altitude_list) == 65:
            self.altitude_list.pop(0)
        elif len(self.altitude_list) > 65:
            print('CRITICAL ERROR: Too many altitude variables stored')
    
    def check_liftoff(self) -> bool:
        """Determines if the rocket has liftoff.
        Checks if the rocket has gained more than 1 meter of altitude in the last second OR
        The rocket has gained a total of 10 meters since the starting altitude
        Returns:
            bool: True if the rocket has liftoff, False otherwise.
        """
        lm = np.median(np.array(self.altitude_list[64-8:]))  # Newest 8 samples (1 seconds)
        fm = np.median(np.array(self.altitude_list[:64-8]))  # Oldest 56 samples (7 seconds)
        return lm > fm + 1 or lm > 10
    
    
    # IMPORTANT: SHOULD WE USE LESS OLDER SAMPLES TO DETECT APOGEE SOONER???
    def check_apogee(self) -> bool:  # Checks if the rocket is past the apogee
        """Determines if the rocket has passed the apogee.
        
        If the median of the last second of altitude values is less than the
        median of the previous values, declare apogee has passed
        
        Returns:
            bool: True if the rocket has passed the apogee, False otherwise.
        """
        lm = np.median(np.array(self.altitude_list[64-8:]))  # Newest 8 samples (1 seconds)
        fm = np.median(np.array(self.altitude_list[64-16:64-8]))  # Second newest 8 samples 1 to 2 second ago)
        return lm < fm
    
    def check_landed(self) -> bool:
        """Determines if the rocket has landed.
        Returns:
            bool: True if the rocket has landed, False otherwise.
        """
        lm = np.median(np.array(self.altitude_list[64-8:]))  # Newest 8 samples (.5 seconds)
        return lm < 10  # Altitude is already relative to base altitude. Checking if we are below 10 meters above base altitude

    def new_telemetry(self, telemetry: dict) -> None:
        """Updates the flight status based on the new telemetry.
        Args:
            telemetry (dict): Current telemetry from the Sense Hat.
        """
        self.add_altitude(telemetry['altitude'])
        
        if len(self.altitude_list) >= 64:
            if self.stage.value == Stage.PRE_FLIGHT and self.check_liftoff():
                self.stage.value = Stage.IN_FLIGHT
            elif self.stage.value == Stage.IN_FLIGHT and self.check_apogee():
                self.stage.value = Stage.DESCENT
            elif self.stage.value == Stage.DESCENT and self.check_landed():
                self.stage.value = Stage.ON_GROUND
        else:
            print("Need more altitude, collecting...")