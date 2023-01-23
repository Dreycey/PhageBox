#!/usr/bin/python3
"""_summary_
This module tests the PhageBox temperature sensors. Specifically,
this module is used to collect temperature readings along the length
of the chip. The accompanying notebook/script can be used to generate
plots once this script outputs a CSV.

"""
# non-std packages
from typing import List
import serial
import argparse
import sys
import os


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
    parser.add_argument("-o", "--outputfile",
                        help="output csv file path", required=True)
    return parser.parse_args(argv)


class ArduinoTempMonitor:
    """ object for pulling in temp data from arduino """

    def __init__(self, port):
        self.port = port
        self.serial = serial.Serial(port, 9600)

    def writeOutputToCSV(self, outputCSV, number_of_measurements=50):
        """
        This method saves the measured temperatures along the 
        phagebox chip to a specified output file.
        """
        # remove file if it exists
        if os.path.exists(outputCSV):
            os.remove(outputCSV)

        # open and initialize the output file
        output_file = open(outputCSV, "a")
        output_file.write(f"set temp,marker position,measured temperature\n")

        # find temperatures along the length of the device
        for temperature in range(60, 100, 10):
            print(f"Set temperature to {temperature}")
            input("Press Enter once temperature steady...")
            for position in range(0, 2, 1):
                print(f"Change position to {position}")
                input("Press Enter once position steady...")
                # collect temperatures at the current position for a set temperature.
                measurements = 0
                while measurements < number_of_measurements:
                    temp_measures: float = float(self.serial.readline().decode(
                        'ascii').strip(" ").strip("\n").strip("\r").lower())
                    print(temp_measures)
                    # save to CSV
                    output_file.write(
                        f"{temperature},{position},{temp_measures}\n")
                    # update counter and reset buffer.
                    measurements += 1
                    self.serial.reset_input_buffer()


def main():
    arguments = parseArgs(sys.argv[1:])
    mag_monitor = ArduinoTempMonitor(arguments.port)
    mag_monitor.writeOutputToCSV(
        arguments.outputfile)


if __name__ == "__main__":
    main()
