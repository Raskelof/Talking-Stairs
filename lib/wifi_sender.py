import time
import network
from network import WLAN
import socket
import binascii
import urequests as requests
import machine

class WiFiSender:
    def __init__(self, SSID, password, notification_endpoint):
        
        self.notification_endpoint = notification_endpoint
        
        wlan = network.WLAN(mode=network.WLAN.STA)
        wlan.connect(ssid=SSID, auth=(WLAN.WPA2, password))

        while not wlan.isconnected():
            machine.idle()
            
        print("WiFi connected succesfully")
        print(wlan.ifconfig())
        

    def send(self):

        res = requests.get(url=self.notification_endpoint)
        print(res.text)

        


