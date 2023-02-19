import board
import busio
import digitalio

import adafruit_sdcard
import storage

class Logger():
    def __init__(self) -> None:
        self.spi = busio.SPI(board.SCK, MOSI=board.TX, MISO=board.RX)
        self.cs = digitalio.DigitalInOut(board.IO1)
        self.sdcard = adafruit_sdcard.SDCard(self.spi, self.cs)
        self.vfs = storage.VfsFat(self.sdcard)
        storage.mount(self.vfs, "/sd")
    
    def set_headers(self, headers):
        with open("/sd/data.csv", "a") as f:
            f.write(",".join(headers))
            f.write("\r\n")
        pass
    
    def log_data(self, data):
        with open("/sd/data.csv", "a") as f:
            f.write(",".join(data))
            f.write("\r\n")
    