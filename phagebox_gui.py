"""
Author: Dreycey Albin

Description:
    This file contains the app for the phagebox. This activates the
    front end which can interact with the backend arduino controller.

Design Pattern:
    This uses a model-view-controller for interacting the phagebox.
"""
# standard library
import tkinter as tk
from tkinter import ttk
import sys
import atexit
# non-standard library
import argparse
import customtkinter
# in-house packages
from src.phagebox_gui.phagebox_view import PhageBoxGUI
from src.phagebox_gui.arduino_controller import ArduinoController



# global control
customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green



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
    parser.add_argument("-s", "--serial_port", help="Specify the serial port", required=True)
    parser.add_argument("-m", "--slope", type=float, default=1.2, help="Slope of (Chip Temp vs Peltier Temp) [Default 1.2 @RT]", required=False)
    parser.add_argument("-b", "--intercept", type=float, default=-2, help="y-intercept (Chip Temp vs Peltier Temp) [Default -2 @RT]", required=False)
    parser.add_argument("-v", "--verbose", action="store_true", help="prints output figures and debug info", required=False)
    return parser.parse_args(argv)

class App(customtkinter.CTk):
    """
    Description:
        This app class is the primary object that
        instiates the system.
    """
    WIDTH = 900
    HEIGHT = 600

    def __init__(self, serial_port, y_int, slope):
        super().__init__()
        super().columnconfigure(0, weight=1)
        super().rowconfigure(0, weight=1)

        # add title for the GUI
        self.title('PhageBox')

        # arduino-adapter instantiation 
        self.model = ArduinoController(serial_port)

        # create a view and place it on the root window
        view = PhageBoxGUI(self, self.model, y_int, slope)
        view.grid(row=0, column=0, padx=10, pady=10)

    def stop_now(self):
        """
        Description:
            This destroys the window when exiting, and ensures a
            'distructor like call to the model class'.
        """
        self.model.stop_now()
        self.destroy()

if __name__ == '__main__':
    args = parseArgs(sys.argv[1:])
    app = App(args.serial_port, args.intercept, args.slope)
    app.wm_protocol("WM_DELETE_WINDOW", app.stop_now)
    app.mainloop()