# PhageBox Arduino Library

## Description

This libarary has been written for the PhageBox extension module. It assumes access to the Arduino Libraries. This is an embedded C implementation of PCR using a finite state machine. This then controls GPIO registers directorly (bare metal) and implements a timer for switching states. The outcome of these modules is finite state machine that can control peltier (heating) modules on the device.

### Block Diagram

The below outlines the software used to impliment the finite state machine controlled PCR.

![Software box diagram](../../figures/box_diagram.png)

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

### Usage once library is installed

Once installed, you can send commands through Serial/UART for controlling backlight, magnetic module and temperature modules:

1. Heater 1 for 32 PCR cycles. **Cycles**: 15 seconds at 90C, 20 seconds at 50C, and 60 seconds at 72C.

```
<H,1,32,15,90,20,50,60,72>
```

2. Heater 2 for 32 PCR cycles. **Cycles**: 15 seconds at 90C, 20 seconds at 50C, and 60 seconds at 72C.

```
<H,2,32,15,90,20,50,60,72>
```

3. Toggle the LED

```
<B,0,1>
```

4. Toggle the MAGNET

```
<B,1,0>
```

5. Toggle both the MAGNET and LED

```
<B,1,1>
```
