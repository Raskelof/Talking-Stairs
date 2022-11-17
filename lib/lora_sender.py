import time
from network import LoRa
import socket
import binascii

class LoRaSender:
    def __init__(self, dev_eui_value, app_eui_value, app_key_value):
        
        self.lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
        self.lora.reset()
        print('Init LoRa')
        # TTN
        #dev_eui = binascii.unhexlify('70B3D57ED005708B')
        #app_eui = binascii.unhexlify('10D9C8A3C9C80000')
        #app_key = binascii.unhexlify('353A522BEE2D01A7CA48D877A1EBE740')

        #helium
        dev_eui = binascii.unhexlify(dev_eui_value)
        app_eui = binascii.unhexlify(app_eui_value)
        app_key = binascii.unhexlify(app_key_value)

        self.lora.nvram_restore()

        if(self.lora.has_joined() == False):
            print("LoRa not joined yet")
            self.lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=0)
            
            while not self.lora.has_joined():
                time.sleep(4)
                print('Not joined yet...' + str(self.lora.has_joined()))
                
            print("LoRa Joined!!!")
            self.lora.nvram_save()
        else:
            print("LoRa Joined directly")

    def send(self, msg):

        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        # set the LoRaWAN data rate
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
        # make the socket blocking
        # (waits for the data to be sent and for the 2 receive windows to expire)
        s.setblocking(True)

        # send some data
        print('send data')

        msg_bytes = bytes(msg, 'utf-8')
        s.send(msg_bytes)

        # make the socket non-blocking
        # (because if there's no data received it will block forever...)
        s.setblocking(False)

        # get any data received (if any...)
        data = s.recv(64)
        self.lora.nvram_save()
        help(s)
        s.close()
        print('recieve bytes')
        print(data)

        

