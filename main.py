from screen import Screen
from vibration_detection import VibrationDetection
from lora_sender import LoRaSender
from wifi_sender import WiFiSender
from settings import Settings

print("####### init main.py #######")

config = Settings()

s = Screen()
s.clear()

if(config.use_wifi):
    s.display('Init Wifi')
    wifiSender = WiFiSender(config.wifiSSID, config.wifiPassword, config.notification_endpoint)
    s.display('Wifi OK')
else:
    s.display('Init LoRa')
    loraSender = LoRaSender(config.dev_eui ,config.app_eui ,config.app_key)
    s.display('LoRa OK')

def on_pin_read_OK():
    s.clear();
    s.display('Sensor OK')

def on_vibration_detected(ms_since_last_vibration):
    print('Vibration detected')
    print(ms_since_last_vibration)
    
    sequence_time_ms = config.sequence_time_ms
    if(ms_since_last_vibration > sequence_time_ms):
        
        s.clear()
        s.display(str(ms_since_last_vibration))

        if(config.use_wifi):
            wifiSender.send()
        else:
            loraSender.send('1')


vib = VibrationDetection()
vib.listen(on_vibration_detected, on_pin_read_OK)