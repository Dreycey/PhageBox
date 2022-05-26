# PhageBox Arduino Library

## Description
This libarary has been written for the PhageBox extension module. It assumes access to the Arduino Libraries. This is an embedded C implementation of PCR using a finite state machine. This then controls GPIO registers directorly (bare metal) and implements a timer for switching states. The outcome of these modules is finite state machine that can control peltier (heating) modules on the device.

## Elegance
All of the code has been refactored a couple of times. In particular, a big focus was ensuring a clean implimentation, clean code, and consistency.

## Testing

How did you prove that your code is correct?

The code was proven correct by ensuring timing was vissually accurate and by turning the heaters on. Likewise, GPIO testing was validated visually by turning on the on board electromagnets and the relays for the peltier modules.

Error cases were handled using print outs to the serial port, if the end user supplies commands that are not recognized by the serial parsing module. A python script was originally used to send commands through UART, but the Serial window provided by the Arduino IDE did the job needed for testing the ability to change temperature through UAART.


## Documentation / About

### VIDEO on project

Please watch the following video for a descriptive overview:


https://youtu.be/Ule5zzMIgWQ

There are also slides here in the repository.

### Block Diagram
The below outlines the software used to impliment the finite state machine controlled PCR.

![box diaram](box_diagram.png)

## Usage
To use this library, drag it into the arduinno libary and import.

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


