# Talking stairs 
## IoT examination project at LNU - Applied Internet of Things

###### tags: `IoT` `examination` `LNU` `Heltec` `ESP32` `LoRa` `Detect vibrations`
---
**Table of Contents**


[TOC]


## Tutorial on how to detect vibrations from stairways and trigger notifications over LoRa/WiFi

Author: Rikard Askelöf

This turtorial describes the steps needed to build your own vibration detection device to trigger events over LoRa or WiFi. My personal aim was to install this setup in my stairway to detect a person walking in the stairway but the use case could be anything where you have a need to detect vibrations and act on them.

Depending on your enviroment, use case and experience the setup process takes 10 - 30h. 

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

Comming from a developer backround in system/web/app development my main goal of this project was to learn more about IoT development and specifically using communication protocols like LoRa. 

<!--
Describe why you have chosen to build this specific device. What purpose does it serve? What do you want to do with the data, and what new insights do you think it will give?

- [ ] Why you chose the project
- [ ] What purpose does it serve
- [ ] What insights you think it will give
-->

### Material

Explain all material that is needed. All sensors, where you bought them and their specifications. Please also provide pictures of what you have bought and what you are using.

- [ ] List of material
- [ ] What the different things (sensors, wires, controllers) do - short specifications
- [ ] Where you bought them and how much they cost


> Example:
>| IoT Thing | For this         |
>| --------- | ---------------- |
>| Perhaps   | a table          |
>| is a      | jolly good idea? |
>
>In this project I have chosen to work with the Pycom LoPy4 device as seen in Fig. 1, it's a neat little device programmed by MicroPython and has several bands of connectivity. The device has many digital and analog input and outputs and is well suited for an IoT project.



### Environment setup

This project was programmed in MicroPython and to get you started you will need to setup the enviroment.

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

 + For this project I ended up using Thonny for development which is lightweight IDE for micro controllers but I would suggest you try using either VS Code or Atom with the PyMakr plugin installed. I had some stability issues uploading new code when I used VS Code with PyMakr but it's definitly a more modern setup. You can download Thonny from here: https://thonny.org/

##### 4. Verify your installation

 + Open Thonny and hit the stop/restart button. You should se the following statement when the device boots up 
 > Pycom MicroPython 1.20.2.r4 [v1.20.1.r2-392-g172cf5d0-dirty] on 2021-01-19; Heltec Wireless Stick with ESP32


### Putting everything together

To get the physical setup in place when need to connect our vibration sensor and LoRa antenna. To make things a litle bit easier I used a breadboard to connect the circuits. 

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

As the device supports wireless communication using both WiFi and LoRA the infrastructure to forward the vibration signals is built with **Azure Cloud PLatform** and **Helium**. If you plan to use WiFi you can simply skip the Helium part. 

Read more about the platform setup under "The physical network layer".

#### Cost

The cost for using Helium could be free or at least very low depending on your usage. $0.0002 per day if you use one uplink every hour during the day. The hosting on Azure could more costly, while the web app is free if you go for the "Dev web app" the database has minimum price of 128 kr / month that would be sufficient for our requirements. I would recommend to facilitate any existing database and infrastructure you might have at hand because the requirements are very low as we are only using one table with limited reads and writes. Using the Azure trial / free tier would also give you 1 year of free services.


### The code

Import core functions of your code here, and don't forget to explain what you have done. Do not put too much code here, focus on the core functionalities. Have you done a specific function that does a calculation, or are you using clever function for sending data on two networks? Or, are you checking if the value is reasonable etc. Explain what you have done, including the setup of the network, wireless, libraries and all that is needed to understand.


```python=
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
    loraSender = LoRaSender()
    s.display('LoRa OK')

def on_pin_read_OK():
    s.clear();
    s.display('Pin OK')

def on_vibration_detected(ms_since_last_vibration):
    print('Yes sir')
    print(ms_since_last_vibration)
    
    sequence_time_ms = 2000
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
My first plan was to use LoRa as the sole wireless protocol to send notifications. As it turned out the signaling between my home and public TTN gatways and Helium gateways was too unreliable so I ended up adding a configurable fallback to use WiFi instead. This can be easily configured in the configuration file described below. To make testing more convenient I've added confirmation messages to the built in OLED display which will display **"LoRa OK"** or **"WiFi OK"** if everyhings connects well.

The choice of using LoRa as an optional communication method was simply based on my interest of learning more about this protocol. For my use case (installation indoors) it's not very reliable and I would recommend using WiFi instead if it's feasible. WiFI would also be without latency if you have the requirement to get the notifications in real time or close to real time. On the other hand if your enviroment is outdoors with good connectivity LoRa could be the preferred choice.


![IoT circuits](https://github.com/Raskelof/Talking-Stairs/blob/main/assets/IoT-stairs_connectivity.png?raw=true)


The picture above descibes how detected vibrations are sent out from the device, gets logged in the database and finally geeting pulled from a local application to play an audio message. No matter if you choose WiFi or LoRa, the message sent will go through the same HTTP endpoint.

To configure WiFi or LoRa you need to set the following variable in the `config.json`

```js
"useWiFi": true
```

##### Setting up communication using WiFi

Besides configuring the corrrect SSD and password you also need to provide the endpoint URL to which all notifications will be sent using HTTP GET.

```js
"notification_endpoint": "http://mydomain.com/myendpoint"
```

##### Setting up communication using LoRa with Helium

To set the device up using LoRa and Helium follow the steps found in this guide

https://hackmd.io/@lnu-iot/HJUu_sIO9

When you have your device setup in Helium you also need provide the following configuration in the `config.json` file.

```js
"dev_eui": "x",
"app_eui": "x",
"app_key": "x"
```

If everything is correctly configured you should now see the message "LoRa OK" after boot up and after a successfull join to a Helium gateway.

As a last step you need to set up a new integration in the Helium console. Add a new "HTTP" integration and specifiy the "Endpoint URL". Next go to the "Flows" section and create link between your device and the HTTP integration you just created.


How is the data transmitted to the internet or local server? Describe the package format. All the different steps that are needed in getting the data to your end-point. Explain both the code and choice of wireless protocols.

- [ ] How often is the data sent? 
- [ ] Which wireless protocols did you use (WiFi, LoRa, etc ...)?
- [ ] Which transport protocols were used (MQTT, webhook, etc ...)
- [ ] Elaborate on the design choices regarding data transmission and wireless protocols. That is how your choices affect the device range and battery consumption.
- [ ] What alternatives did you evaluate?
- [ ] What are the design limitations of your choices?

### Visualisation and user interface

The visualization comes in the form of a audio message wit a greeting being played to the end user.

.NET and c# is my preferred choice of language so it was natural to setup the infrastructure around the device using .NET. The code and setup is very simple though so I would suggest you use whatever language you feel comfortable with. The following describes the purpose and logics in each application.

##### Web server hosted on Azure
Web server hosted using Azure Web Apps. Contains one endpoint that logs any requests in the datasbase |

##### MSSQL Database hosted Azure
One table with columns for primary id, createdOn and data

.NET Console application hosted on local computer
##### One console aplication polling the database for new log rows (vibrations) and plays a sound using Microsoft.Speech
>

Describe the presentation part. How is the dashboard built? How long is the data preserved in the database?

- [ ] Provide visual examples on how the visualisation/UI looks. Pictures are needed.
- [ ] How often is data saved in the database. What are the design choices?
- [ ] Explain your choice of database. What kind of database. Motivate.
- [ ] Automation/triggers of the data.
- [ ] Alerting services. Are any used, what are the options and how are they in that case included.

### Finalizing the design

Show the final results of your project. Give your final thoughts on how you think the project went. What could have been done in an other way, or even better? Pictures are nice!

- [ ] Show final results of the project
- [ ] Pictures
- [ ] *Video presentation

---