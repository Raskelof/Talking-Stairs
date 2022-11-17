from machine import Pin
import time

class Led:
    def __init__(self):
        self.led = Pin('P22', Pin.OUT)

    def on(self):
        self.led(1)
        
    def off(self):
        self.led(0)
        
    def flash(self):
        self.on()
        time.sleep_ms(300)
        self.off()
