import time
import machine
import ujson

class Settings:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
          cls.instance = super(Settings, cls).__new__(cls)
        return cls.instance
    def __init__(self):
        
        import ujson
        with open('../config.json') as data_file:
            data_str = data_file.read()

            data = ujson.loads(data_str)
            self.wifiSSID = data["wifi"]["SSD"]
            self.wifiPassword = data["wifi"]["password"]
            self.dev_eui = data["lora"]["dev_eui"]
            self.app_eui = data["lora"]["app_eui"]
            self.app_key = data["lora"]["app_key"]
            
            self.notification_endpoint = data["notification_endpoint"]
            self.use_wifi = data["useWiFi"]
            self.sequence_time_ms = data["sequence_time_ms"]
            #print('SSD: {} & pass: {}',yourWifiSSID,yourWifiPassword)


        



