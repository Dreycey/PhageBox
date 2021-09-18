#!/usr/bin/python3
"""
DESCRIPTION:
    This script is used in conjunction to the magnetometer
    to collect data from the magenetometer. 
"""
# non-std packages
from typing import List
import serial
import argparse
import sys


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
    parser.add_argument("-o", "--outputfile", help="output csv file path", required=True)
    return parser.parse_args(argv)

class ArduinoMagnetoMeterMonitor:
    """ object for pulling in data from arduino """

    def __init__(self, port):
        self.port = port
        self.serial = serial.Serial(port, 9600)
    
    def writeMagneticOutputToCSV(self, outputCSV):
        """
        This method outputs the z,x,y readings of the
        magnetic flux to a file. It is assumed this will
        be running continuously. 
        """
        output_file = open(outputCSV, "a")
        time_coounter = 0
        while True:
            magnetic_measures: List[str] = str(self.serial.readline()).split("\t")
            for val_return in magnetic_measures:

                if "x" in val_return:
                    x = val_return.split(" ")[1]
                elif "y" in val_return:
                    y = val_return.split(" ")[1]
                elif "z" in val_return:
                    z = val_return.split(" ")[1]
                else:
                    return NameError(" {val_return} did not have x, y, or z for parsing")
            output_file.write(f"{time_coounter},{x},{y},{z}")
            time_coounter += 1

def main():
    """ 
    This is the flow of the script for measuring the
    magnetic flux produced by the magenetometer module,
    and collecting this information into a CSV.
    """
    arguments = parseArgs(sys.argv)
    mag_monitor = ArduinoMagnetoMeterMonitor(arguments.port)
    mag_monitor.writeMagneticOutputToCSV(arguments.ouputflie)

if __name__ == "__main__":
    main()