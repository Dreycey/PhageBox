#!/usr/local/bin/python3
"""
Author: Dreycey Albin

Description:
------------
    This module communicates through UART with a particular port. 
    This module performs 'backend' communication with an embedded 
    device, here the PhageBox. Further extension may be made to this
    frontend-backend design pattern by using a model-view controller varient.

Design Patterns:
----------------
    1. Model-view controller interface. This file contains the interface that utilizes
       an adapter pattern.

Communication Through UART
--------------------------
1. "<H,1,32,15,90,20,50,60,72>"
    The above says heater 1 for 32 PCR cycles. 15 seconds at 90C, ,20 seconds at 50C, and 60 seconds at 72C.
2. "<H,2,32,15,90,20,50,60,72>"
    The above says heater 2 for 32 PCR cycles. 15 seconds at 90C, ,20 seconds at 50C, and 60 seconds at 72C.
3. "<B,0,1>"
    toggle the LED
4. "<B,1,0>"
    toggle the MAGNET
5. "<B,1,1>"
    toggle both the MAGNET and LED


Useful Methods/Classes
----------------------
    1. ArduinoController - acts as a controller for Arduino. This acts as an API for the embedded software.
"""
# standard library
from time import sleep
from serial import Serial
import numpy, sys
import time
import threading
import tkinter as tk
# non-standard library
# in-house packages




class ArduinoController:
    """
    Description:
        This class contains methods for controlling the arduino.
    """

    def __init__(self, port_in):
        """
        Description:
            Initialization for the class for controlling the arduino
        """
        # check for serial (template factory?)
        self._stop_event = threading.Event()
        self.ser : Serial = Serial(port_in, 9600)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        sleep(2) # wait for connection
        self.backlightOn = False
        self.magnetOn = False
        self.t1 = threading.Thread(target=self.read_serial)
        self.t1.start()
        self.current_temperatures = [-1, -1, -1]
        self.set_temperatures = [-1, -1]
        
    def __del__(self):
        """
        Description: 
            body of destructor
        """
        print("arduino-adapter destructor being called")
        self.ser.__del__()

    def stop_now(self):
        self.stop()
        self.t1.join()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def send_serial_msg(self, str):
        """
        Description:
            Sends a string through serial.
        """
        self.ser.write(bytes(str, 'ascii'))

    def toggleBacklight(self):
        """
        Description:
            turns the backlight on and off
        """
        print("light toggle is being called")
        self.send_serial_msg("<B,0,1>")
        if (self.backlightOn):
            self.backlightOn = False
        else:
            self.backlightOn = True

    def toggleMagnet(self):
        """
        Description:
            turns the magnet on and off
        """
        print("magnet toggle is being called")
        self.send_serial_msg("<B,1,0>")
        if (self.magnetOn):
            self.magnetOn = False
        else:
            self.magnetOn = True

    def start_pcr(self, peltier, cycles, d_temp, d_time, a_temp, a_time, e_temp, e_time):
        """
        Description:
            This method initiates PCR for a given peliter.
        """
        print("STARTING PCR")
        peltier = int(peltier)
        cycles = int(cycles)
        d_temp = round(d_temp, 1)
        d_time = round(d_time, 1)
        a_temp = round(a_temp, 1)
        a_time = round(a_time, 1)
        e_temp = round(e_temp, 1)
        e_time = round(e_time, 1)
        if peltier == 3:
            print(f"<H,1,{cycles},{d_time},{d_temp},{a_time},{a_temp},{e_time},{e_temp}>")
            self.send_serial_msg(f"<H,1,{cycles},{d_time},{d_temp},{a_time},{a_temp},{e_time},{e_temp}>")
            print(f"<H,2,{cycles},{d_time},{d_temp},{a_time},{a_temp},{e_time},{e_temp}>")
            self.send_serial_msg(f"<H,2,{cycles},{d_time},{d_temp},{a_time},{a_temp},{e_time},{e_temp}>")
        else:
            print(f"<H,2,{cycles},{d_time},{d_temp},{a_time},{a_temp},{e_time},{e_temp}>")
            self.send_serial_msg(f"<H,{peltier},{cycles},{d_time},{d_temp},{a_time},{a_temp},{e_time},{e_temp}>")

    def read_serial(self):
        """
        Description:
            This method reads serial.
        Note:
            This should be ran on a seperate thread considering it is always read!
        """
        while not self.stopped():
            if self.ser.in_waiting:
                serial_in_string = str(self.ser.readline()).strip("b").strip("'").strip("\\n").strip("\r")
                pelt_identifier = serial_in_string.split(",")[0]
                if pelt_identifier == "T_METAL":
                    temperature = serial_in_string.split(",")[-1]
                    self.current_temperatures[0] = float(temperature)
                elif pelt_identifier == "T_FRONT":
                    temperature = serial_in_string.split(",")[-1]
                    self.current_temperatures[1] = float(temperature)
                elif pelt_identifier == "T_BACK":
                    temperature = serial_in_string.split(",")[-1]
                    self.current_temperatures[2] = float(temperature)
                elif pelt_identifier == "T_FRONT_SET":
                    temperature = serial_in_string.split(",")[-1]
                    self.set_temperatures[0] = float(temperature)
                elif pelt_identifier == "T_BACK_SET":
                    temperature = serial_in_string.split(",")[-1]
                    self.set_temperatures[1] = float(temperature)
                else:
                    print(serial_in_string)


# def main():
#     #####
#     # Controlling the temperature
#     #####
#     arrd = ArduinoController(ss)
#     arrd.toggleMagnet()

# if __name__ == "__main__":
#     main()
