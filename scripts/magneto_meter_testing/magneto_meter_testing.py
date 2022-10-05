#!/usr/bin/python3
"""
DESCRIPTION:
    This script is used in conjunction to the magnetometer
    to collect data from the magenetometer. 
USAGE:
    python magneto_meter_testing.py -p <path to UART port> -o <Output CSV> [--disc_test]
EXAMPLE:
    python magneto_meter_testing.py -p /dev/cu.usbmodem14101 -o OUTTEST.csv
"""
# non-std packages
from typing import List
import serial
import argparse
import sys
import os

# Create an argparse.Namespace object from input args.
def parseArgs(argv=None) -> argparse.Namespace:
    """
    This method takes in the arguments from the command and performs
    parsing.
    INPUT: 
        Array of input arguments
    OUTPUT:
        returns a argparse.Namespace object
    """
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-p", "--port", help="input port path", required=True)
    group.add_argument("-d", "--disc_test", action="store_true")
    parser.add_argument("-o", "--outputfile", help="output csv file path", required=True)
    return parser.parse_args(argv)

class ArduinoMagnetoMeterMonitor:
    """ object for pulling in data from arduino """

    def __init__(self, port):
        self.port = port
        self.serial = serial.Serial(port, 9600)
        self.x = 0
        self.y = 0
        self.z = 0

    def writeMagneticOutputToCSV(self, outputCSV, discreet_tests=False):
        """
        This method outputs the z,x,y readings of the
        magnetic flux to a file. It is assumed this will
        be running continuously. 
        """
        if os.path.exists(outputCSV):
            os.remove(outputCSV)
        output_file = open(outputCSV, "a")
        output_file.write(f"time_counter,x (uTesla),y (uTesla),z (uTesla)\n")
        time_counter = 0
        while True:
            magnetic_measures: str = self.serial.readline().decode('ascii').strip(" ").strip("\n").strip("\r")
            val_return = magnetic_measures.lower()
            if "x:" in val_return:
                self.x = val_return.split(":")[1]
            elif "y:" in val_return:
                self.y = val_return.split(":")[1]
            elif "z:" in val_return:
                self.z = val_return.split(":")[1]
            else:
                continue
            output_file.write(f"{time_counter},{self.x},{self.y},{self.z}\n")
            time_counter += 1
            if time_counter % 10 == 0:
                print(f"{time_counter} timepoints added", end="\r")
            if (time_counter % 10 == 0) and discreet_tests:
                val = input("SWITCH (state ON/OFF): ")
                output_file.write(f"SWITCH {val} \n")
                self.serial.reset_input_buffer()

def main():
    """ 
    This is the flow of the script for measuring the
    magnetic flux produced by the magenetometer module,
    and collecting this information into a CSV.
    """
    arguments = parseArgs(sys.argv[1:])
    mag_monitor = ArduinoMagnetoMeterMonitor(arguments.port)
    mag_monitor.writeMagneticOutputToCSV(arguments.outputfile, discreet_tests=arguments.disc_test)

if __name__ == "__main__":
    main()