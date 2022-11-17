import ssd1306
import time
from machine import I2C, Pin

class Screen:
    def __init__(self):
        i2c_scl = Pin('P4', mode=Pin.OUT, pull=Pin.PULL_UP)
        i2c_sda = Pin('P3', mode=Pin.OUT, pull=Pin.PULL_UP)
        i2c = I2C(0, I2C.MASTER, baudrate=100000, pins=(i2c_sda,i2c_scl))
        
        devices = i2c.scan() # this returns a list of devices

        device_count = len(devices)

        if device_count == 0:
            print('No i2c device found.')
        else:
            print(device_count, 'devices found.')

        for device in devices:
            print('Decimal address:', device, ", Hex address: ", hex(device))
        
        self.oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
        

    def display(self, text, value=None):

        print(text)
        self.oled.fill(0)
        self.oled.text(text, self.text_position(text), 10)
        
        if value is not None:
            self.oled.text(value, self.text_position(value), 25)
        
        self.oled.show()
        
    def clear(self):

        self.oled.fill(0)
        self.oled.show()
        
    def text_position(self, text):
        text_position = 50 - len(text)
        
        if text_position < 0:
            text_position = 0
            
        return 0
        
