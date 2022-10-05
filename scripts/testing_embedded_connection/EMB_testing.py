"""
PES project
________________

This file is used to test the embedded device. 

Eventually the gui will be updated basaed on this script. 
"""
import serial
import sys
import time
from struct import * 


if __name__ == "__main__":
    port_in = str(sys.argv[1])
    ser = serial.Serial(port_in, 9600)
    while (True):
        # message = bytearray([1, 2])
        message = b'101010'
        message = pack('15l',0,1,2,3,4,5,6,7,8,9,10,11,12,13,14)
        message = 'M'.encode()
        print(message)
        ser.write(message)
        reading = ser.readline()
        print(reading)
        time.sleep(1)