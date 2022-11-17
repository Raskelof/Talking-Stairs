import time
from machine import Pin

class VibrationDetection:
    def __init__(self):
        
        self.last_vibration_time = time.ticks_ms() - 1000

    def listen(self, onVibrationDetected, onPinReadOk):

        pin_input = Pin('P10', mode = Pin.IN)
        
        last_value = pin_input.value()

        onPinReadOk()
        print('start listening')
        while True:
            try:
                value = pin_input.value()
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
            #time.sleep(1)
            
            try:
                if(last_value != value):
                    last_value = value
                    time_since_last_vibration = time.ticks_ms() - self.last_vibration_time
                    self.last_vibration_time = time.ticks_ms()
                    
                    onVibrationDetected(time_since_last_vibration)
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
        

        


