# The Talking Stairway 
## Tutorial on how to detect vibrations from a stairway and trigger notifications over LoRa/WiFi
> IoT examination project at LNU - Applied Internet of Things

###### tags: `IoT` `examination` `LNU` `Heltec` `ESP32` `LoRa` `Detect vibrations`

Author: Rikard Askelöf

---

This tutorial describes the steps needed to build your own vibration detection device to trigger events over LoRa or WiFi. My personal aim was to install this setup in my stairway to detect a person walking in the stairway but the use case could be anything where you have a need to detect vibrations and act on them.

Depending on your environment, use case and experience the setup process takes 10 - 40h. 

**Table of Contents**

1. [Objectives](#Objectives)
2. [Material](#Material)
3. [Environment setup](#Environment-setup)
4. [Putting everything together](#Putting-everything-together)
5. [Platforms and infrastructure](#Platforms-and-infrastructure)
6. [The code](#The-code)
7. [The physical network layer](#The-physical-network-layer)
8. [Visualisation and user interface](#Visualisation-and-user-interface)
9. [Finalizing the design](#Finalizing-the-design)

<!---
Give a short and brief overview of what your project is about.
What needs to be included:

- [ ] Title
- [ ] Your name and student credentials (xx666xxx)
- [ ] Short project overview
- [ ] How much time it might take to do (an approximation)
-->

### Objectives

The purpose of the project is to detect a person walking down stairways and send a notification over WiFi/LoRa. In my specific case I used that notification to play an audio message to the person walking down to greet them with a voice saying e.g. "Good morning" or "Hello".

Coming from a developer background in system/web/app development my main goal of this project was to learn more about IoT development and specifically using communication technologies like LoRa. 

<!--
Describe why you have chosen to build this specific device. What purpose does it serve? What do you want to do with the data, and what new insights do you think it will give?

- [ ] Why you chose the project
- [ ] What purpose does it serve
- [ ] What insights you think it will give
-->

### Material

I have chosen to build my device using the microcontroller NodeMCU ESP32 Heltec mainly because it supports both WiFi and LoRa. A nice little bonus included on this device is the built-in OLED display which was very handy to display application status when not connected to the computer. 

| Product | Where to buy | Description | Price |
| --------- | ---------------- | ---------------- | ----------------: |
| NodeMCU ESP32 Heltec | [link](https://www.amazon.se/dp/B08243JHMW?ref_=pe_24982401_518009621_302_E_DDE_dt_1) | Microcontroller supporting WiFi and Lora. Built in OLED display. | 350SEK |
| Vibration sensor high sensitivity | [link](https://www.electrokit.com/produkt/vibrationssensor-hog-kanslighet/) | Measures vibration through digital output | 42SEK |
| Jumper wires male-male | [link](https://www.electrokit.com/produkt/labbsladd-40-pin-30cm-hane-hane/) | Wires to connect the circuits | 49SEK |
| Jumper wires female-male | [link](https://www.electrokit.com/produkt/labbsladd-40-pin-30cm-hona-hane/) | Wires to connect the circuits | 49SEK |
| USB to Micro USB cable | [link](https://www.kjell.com/se/produkter/kablar-kontakter/usb-kablar/linocell-micro-usb-kabel-svart-05-m-p93424?gclid=Cj0KCQiAsdKbBhDHARIsANJ6-jdFMu6K6bP9FJbrX_VwUeSgRLyFK9sPdiU4-TL19HrHKeCEr88ER2IaAqSyEALw_wcB&gclsrc=aw.ds) | Cable to program the device | 110SEK |
| Battery | [link](https://www.kjell.com/se/produkter/el-verktyg/laddare/mobilladdare/powerbank/linocell-powerbank-10000-mah-p89256) | Power supply | 199SEK |
| Breadboard | [link](https://sizable.se/P.TVY7M/Kopplingsdack-med-830-punkter) | Breadboard to connect device and sensor during development | 59SEK |

### Environment setup

This project was programmed in MicroPython and to get you started you will need to set up the environment.

##### 1. Install drivers

 + Connect the Heltec board to your computer using a USB to micro USB cable
 + Download drivers and install preferred version from https://www.silabs.com/documents/public/software/CP210x_Windows_Drivers.zip

##### 2. Flash the firmware with PyCom MicroPython

 + Download the firmware for Heltec Boards from https://github.com/H-Ryan/Heltec/blob/main/PyCom%20MicroPython/Heltec%20PyCom%20MicroPython.zip?raw=true
 + Open a browser and head over to https://espressif.github.io/esptool-js/ and click "Connect"
 + Update the "Flash address" to "0x0000" instead of "0x1000"
 + Click "Program". This will start the flashing process.
 + Close down this tab/page when finished.

##### 3. Install IDE on computer

 + For this project I ended up using Thonny for development which is lightweight IDE for microcontrollers but I would suggest you try using either VS Code or Atom with the PyMakr plugin installed. I had some stability issues uploading new code when I used VS Code with PyMakr but it's definitely a more modern setup. You can download Thonny from here: https://thonny.org/

##### 4. Verify your installation

 + Open Thonny and hit the stop/restart button. You should se the following statement when the device boots up 
 > Pycom MicroPython 1.20.2.r4 [v1.20.1.r2-392-g172cf5d0-dirty] on 2021-01-19; Heltec Wireless Stick with ESP32


### Putting everything together

To get the physical setup in place we need to connect our vibration sensor and LoRa antenna. To make things a little bit easier I used a breadboard to connect the circuits. 

#### Steps

##### 1. Disconnect any power supply (computer or battery)
##### 2. Connect LoRa antenna
##### 3. Connect vibration sensor
+ Connect one wire from **5V** on the board to pin **VCC** on the sensor 
+ Connect one wire from **GND** on the board to pin **GND** o the sensor
+ Connect one wire from **PIN10** on the board to pin **DO** (digital output)
##### 4. As power supply I used a power bank with **5V DC** connected with USB

![IoT circuits](https://github.com/Raskelof/Talking-Stairs/blob/main/assets/sketch_circuits.png?raw=true)

### Platforms and infrastructure

As the device supports wireless communication using both WiFi and LoRA there are two ways to connect the device to the internet. Both the database and the web server is hosted on the **Azure** Platform so if you use WiFi these are the services required to be set up. If you instead want to use LoRa you also need to set up a **Helium** account and configure your device and integration. Read more about the platform setup under "The physical network layer".

#### Cost

The cost for using Helium could be free or at least very low depending on your usage. $0.0002 per day if you use one uplink every hour during the day. The hosting on Azure could more costly, while the web app is free if you go for the "Dev web app" the database has a minimum price of 128 SEK / month that would be sufficient for our requirements. I would recommend to facilitate any existing database and infrastructure you might have at hand because the requirements are very low as we are only using one table with limited reads and writes. Using the Azure trial / free tier would also give you 1 year of free services.


### The code

One central file is the `config.json` file. Besides configuring the communication method (WiFi or LoRa) mentioned below you can also set the `sequence_time_ms`. This value controls how often the device should send vibrations at a maximum. Default is set to 2000 ms which means the device will suppress any notifications 2000 ms after a vibration. This is to avoid spamming.   

**Explanation of libraries in use**

| Library | Explanation |
| ------- | ----------- |
| **lora_sender.py** | Utility class to connect to WiFi and send a GET request |
| **screen.py** | Utility class to display messages on the built-in oled display |
| **settings.py** | Class to read and expose properties from the config.json file |
| **ssd1306.py** [link](https://github.com/stlehmann/micropython-ssd1306/blob/master/ssd1306.py) | Open source library to use the oled display |
| **urequests.py** [link](https://github.com/micropython/micropython-lib/blob/master/python-ecosys/urequests/urequests.py) | Open source utility library to make request over HTTP |
| **vibration_detection.py** | Initiate sensor and listen to vibrations |
| **wifi_sender.py** | Utility class to connect to LoRa and send data |


The central part of the main.py file is the callback method `on_vibration_detected` where the actual incoming vibrations are being handled and processed. There's also another callback method defined `on_pin_read_OK` which makes sure reading from pin (P10) is OK. 

```python=
from screen import Screen
from vibration_detection import VibrationDetection
from lora_sender import LoRaSender
from wifi_sender import WiFiSender
from settings import Settings

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

def **on_pin_read_OK()**:
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

```

### The physical network layer


#### Supporting both WiFi and LoRA
My first plan was to use LoRa as the sole wireless protocol to send notifications. As it turned out the signalling between my home and public TTN gateways and Helium gateways was too weak/unreliable so I ended up adding a configurable fallback to use WiFi instead. This can be easily configured in the configuration file described below. To make testing more convenient I've added confirmation messages to the built in OLED display which will display **"LoRa OK"** or **"WiFi OK"** if everything connects well.

The choice of using LoRa as an optional communication method was simply based on my interest of learning more about this protocol. For my use case (installation indoors) it's not very reliable and I would recommend using WiFi instead if it's feasible. WiFI would also be without latency if you have the requirement to get the notifications in real time or close to real time. On the other hand if your environment is outdoors with good connectivity, LoRa could be the preferred choice.


![IoT circuits](https://github.com/Raskelof/Talking-Stairs/blob/main/assets/IoT-stairs_connectivity.png?raw=true)


The picture above describes how detected vibrations are sent out from the device, gets logged in the database and finally greeting pulled from a local application to play an audio message. No matter if you choose WiFi or LoRa, the message sent will go through the same HTTP endpoint.

To configure WiFi or LoRa you need to set the following variable in the `config.json` file

```js
"useWiFi": true
```

#### Setting up communication using WiFi

Besides configuring the correct SSD and password you also need to provide the endpoint URL to which all notifications will be sent using HTTP GET.

```js
"notification_endpoint": "http://mydomain.com/myendpoint"
```

#### Setting up communication using LoRa with Helium

To set the device up using LoRa and Helium follow the steps found in this guide

https://hackmd.io/@lnu-iot/HJUu_sIO9

When you have your device set up in Helium you also need to provide the following configuration in the `config.json` file.

```js
"dev_eui": "x",
"app_eui": "x",
"app_key": "x"
```

If everything is correctly configured you should now see the message "LoRa OK" after boot up and after a successful  join to a Helium gateway.

As a last step you need to set up a new integration in the Helium console. Add a new "HTTP" integration and specify  the "Endpoint URL". Next go to the "Flows" section and create a link between your device and the HTTP integration you just created.

### Visualisation and user interface

The visualisation comes in the form of an audio message with a text-to-speech greeting being played to the end user.

.NET and c# is my preferred choice of language so it was natural to set up the infrastructure around the device using .NET. The code and setup is very simple though so I would suggest you use whatever language you feel comfortable with. The following describes the purpose and logic in each application.

#### Web server hosted on Azure
Web server hosted using Azure Web Apps. Contains one endpoint that logs any requests in the database described below.

#### MSSQL Database hosted on Azure
MSSQL is the Microsoft relational database. This installation is a very primitive setup with one table (stairwayVibrations) with columns for primary id, createdOn and data. I choose this database only by personal convenience. Data will be logged to the database whenever a vibration event is triggered from the device.

#### .NET Console application hosted on local computer
One console application polling the database for new log rows (stairwayVibrations) and plays a sound using Microsoft.Speech. This console application can be run without installation on any Windows computer. In my setup I connected the computer to a Bluetooth speaker to get a better sound experience when receiving the greeting.

The application code for this

```c#
class Program
    {

        static void Main(string[] args)
        {
            IDB _db = new DB();
            SpeechSynthesizer synthesizer = new SpeechSynthesizer();
            synthesizer.Volume = 100;  // 0...100
            synthesizer.Rate = -2;     // -10...10

            Console.WriteLine("Start listening for vibrations");

            while (true) {
                var hasBeenUpdated = Convert.ToBoolean((int)_db.ExecScalar("sp_hasUpdate", DateTime.Now.AddHours(-1).AddSeconds(-1)));

                if (hasBeenUpdated) {

                    Console.WriteLine("Vibrations detetcted...");
                    Thread.Sleep(14000);
                    
                    
                    synthesizer.Speak("Good morning!");

                    Thread.Sleep(1000);
                }
            }

        }
    }
```

### Finalizing the design

You can watch a proof of concept demo of the complete device and platform setup here:
https://photos.app.goo.gl/m8jURnoubJgfNXZ16


![Device Debug](https://github.com/Raskelof/Talking-Stairs/blob/main/assets/device_debug.jpg?raw=true)

I'm happy with the end result of this project but I haven't reached the end goal. To get real practical use of the device I would like to identify WHO is walking down the stairway to play a personalised message instead of a general greeting. One way to slove this would be to find a even more senesitive vibration sensor so I can detect smaller vibrations and also get the stength of the vibration. Another approach would be to use mulitple vibration sensors and attach them to different stairs on the stairway.

To be continued...

