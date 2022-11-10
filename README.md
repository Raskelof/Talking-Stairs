# Talking stairs 
## IoT examination project at LNU - Applied Internet of Things

###### tags: `IoT` `examination` `LNU` `Heltec` `ESP32` `LoRa` `Detect vibrations`
---
**Table of Contents**


[TOC]


## Tutorial on how to detect vibrations from stairways and trigger notifications over LoRa/WiFi

Author: Rikard Askelöf

This turtorial describes the steps needed to build your own vibration detection device to trigger events over LoRa or WiFi. My personal aim was to install this setup in my stairway to detect a person walking in the stairway but the use case could be anything where you have a need to detect vibrations.

Depending on your enviroment and personal requirements, the setup process takes 10 - 30h. 

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
>
>![LoPy!](https://pycom.io/wp-content/uploads/2018/08/lopySide-1.png)
>Fig. 1. LoPy4 with headers. Pycom.io


### Environment setup

This project was programmed in MicroPython and to get you started you will need to setup the enviroment.

##### 1. Install drivers

 + Connect the Heltec board to your computer using a USB to micro USB cable
 + Download drivers and install preferd version from https://www.silabs.com/documents/public/software/CP210x_Windows_Drivers.zip

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

How is all the electronics connected? Describe all the wiring, good if you can show a circuit diagram. Be specific on how to connect everything, and what to think of in terms of resistors, current and voltage. Is this only for a development setup or could it be used in production?

- [ ] Circuit diagram (can be hand drawn) (Fritzing, Tinkercad, etc.)
- [ ] Electrical calculations
- [ ] Limitations of hardware depending on design choices.
- [ ] Discussion about a way forward - is it possible to scale?

### Platforms and infrastructure

Describe your choice of platform(s). You need to describe how the IoT-platform works, and also the reasoning and motivation about your choices. Have you developed your own platform, or used 

Is your platform based on a local installation or a cloud? Do you plan to use a paid subscription or a free? Describe the different alternatives on going forward if you want to scale your idea.

- [ ] Describe platform in terms of functionality
- [ ] Explain and elaborate what made you choose this platform
- [ ] Provide a pricing discussion. What are the prices for different platforms, and what are the pros and cons of using a low-code platform vs. developing yourself?

https://photos.app.goo.gl/ArGd5DNedDc5cGzP9

![IoT circuits](https://github.com/Raskelof/Talking-Stairs/blob/main/assets/sketch_circuits.png?raw=true)

### The code

Import core functions of your code here, and don't forget to explain what you have done. Do not put too much code here, focus on the core functionalities. Have you done a specific function that does a calculation, or are you using clever function for sending data on two networks? Or, are you checking if the value is reasonable etc. Explain what you have done, including the setup of the network, wireless, libraries and all that is needed to understand.


```python=
import this as that

def my_cool_function():
    print('not much here')

s.send(package)

# Explain your code!
```

### The physical network layer

How is the data transmitted to the internet or local server? Describe the package format. All the different steps that are needed in getting the data to your end-point. Explain both the code and choice of wireless protocols.

- [ ] How often is the data sent? 
- [ ] Which wireless protocols did you use (WiFi, LoRa, etc ...)?
- [ ] Which transport protocols were used (MQTT, webhook, etc ...)
- [ ] Elaborate on the design choices regarding data transmission and wireless protocols. That is how your choices affect the device range and battery consumption.
- [ ] What alternatives did you evaluate?
- [ ] What are the design limitations of your choices?

### Visualisation and user interface

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