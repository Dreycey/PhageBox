![PhageBox Logo](figures/logo.png)

# Description
This repository contains a graphical user interface, arduino libraries, and modules that are used within the PhageBox. Below are instructions for using this code base, as well as information for initiating the GUI. 


## Building the PhageBox.
For building the phagebox, please review the build manual for a step-by-step build process. 

## Embedded Device Software.
![box diaram](figures/box_diagram.png)
### Install
To use this library, drag it into the arduinno libary and import.

### Arduino sketch example

```
#include <PhageBox.h> 

void setup()
{
    Serial.begin(9600);
    init_phagebox();
}

void loop() 
{
    start_phagebox();
}
```

### Usage once library is installed
Now from Serial you can send commands for controlling magnets and the "temperature modules":\

1. "<H,1,32,15,90,20,50,60,72>"
The above says heater 1 for 32 PCR cycles. 15 seconds at 90C, ,20 seconds at 50C, and 60 seconds at 72C.

2. "<H,2,32,15,90,20,50,60,72>"
The above says heater 2 for 32 PCR cycles. 15 seconds at 90C, ,20 seconds at 50C, and 60 seconds at 72C.

3. "<B,0,1>"
toggle the LED

4. "<B,1,0>"
toggle the MAGNET

4. "<B,1,1>"
toggle both the MAGNET and LED


## Graphial User Interface.

### Starting the GUI

General Usage:
```
usage: phagebox_app.py [-h] -s SERIAL_PORT [-m SLOPE] [-b INTERCEPT] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -s SERIAL_PORT, --serial_port SERIAL_PORT
                        Specify the serial port
  -m SLOPE, --slope SLOPE
                        Slope of (Chip Temp vs Peltier Temp) [Default 0.7 @RT]
  -b INTERCEPT, --intercept INTERCEPT
                        y-intercept (Chip Temp vs Peltier Temp) [Default 5
                        @RT]
  -v, --verbose         prints output figures and debug info
```

Example (Mac):
```
python phagebox_app.py -s /dev/tty.usbserial-1430 
```

Example (Windows):
```
python phagebox_app.py -s /dev/tty.usbserial-1430 
```



# DEPRECATED BELOW
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
