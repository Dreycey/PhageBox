# Phage-Box
This repository contains all of the code regarding the Phage-Box. 

![PhageBox Logo](figures/logo.png)

## Description
This repository contains a graphical user interface, arduino libraries, and modules that are used within the PhageBox. Below are instructions for using this code base, as well as information for initiating the GUI. 

## Basic Usage 

## Starting the GUI

1. Open the GUI using python:
```
python phagebox.py <port>
```

### Open the GUI using Mac
* An example is the following command, ensure the correct port is being passed.
```
python phagebox_v4.py /dev/cu.usbserial-1440
```

### Open the GUI using Windows
* An example is the following command, ensure the correct port is being passed.
```
python phagebox_v4.py COM2
```

# Other various Scripts included in the repository
## Basic temp measurements- 03/04/2021

1. Open the correct .ino for the arduino:

2. Start listening in on the serial port:
```
python arduino_controller.py 1
```

3. Start plotting dynamically
```
python control_modules.py
```
