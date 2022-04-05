#!/usr/local/bin/python3
# in-house packages
import phagebox_modules.control_modules as ctrl
import phagebox_modules.arduino_controller as ard_ctrl
# std packages
import numpy as np
import random
import os.path
from os import path
import sys
# non-std packages
import tkinter as tk
from multiprocess import Process
import tkinter.font as font
#from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import threading

"""
This module contains all of the source code used for
creating the tkinter GUI. Different functions for making
the phagebox layout can be found in this python file.
"""



# Globals
LARGE_FONT= ("Verdana", 12)
TITLE_FONT= ("Verdana", 40)
style.use("ggplot")

# Page classes
class phageBoxGUI(tk.Tk):
    """
    This class contains all of the code regarding the tkinter GUI used for the
    phagebox software.
    """

    def __init__(self, serial_port, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.ser_port = serial_port
        # Setting properties of the main frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # instantiate the other frame/page classes
        frames_list = [PhageBoxHome]
        self.frames = {}
        for F in frames_list:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(PhageBoxHome)

    def show_frame(self, cont):
        """
        This function is called by the daughter classes to pull the page to the
        front.
        """
        frame = self.frames[cont]
        frame.tkraise()

class PhageBoxHome(tk.Frame):
    """
    This class is responsible for the constructing the home page for the
    PhageBox GUI.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # save an attribute for the ser port
        self.ser_port = controller.ser_port
        self.ROWCURR = 0
        self.ard_process = False # arduino process
        ard_obj = ard_ctrl.arduino_controller('/dev/cu.usbserial-1440')

        # labels for the page
        label = tk.Label(self, text="PhageBox", font=("Helvetica", 70))
        label.grid(row=0, column=1, sticky="e")
        self.ROWCURR += 1

        # image of the phagebox
        img_height = 200
        img_width = int(img_height * 4)
        self.addImage("figures/phagebox.png",[img_width,img_height], [self.ROWCURR,0,2,8])
        self.ROWCURR += 1

        # Visual Control
        self.ROWCURR += 1
        ## label
        visctrl_label = tk.Label(self, text="Visual Control", font=("Helvetica", 40))
        visctrl_label.grid(row=self.ROWCURR, column=0,pady=(40, 5), sticky="w")
        self.ROWCURR += 1
        ## Description
        VISCTRL_DESC= """ The visual controller helps with lighting on the phage box."""
        visctrl_desc = tk.Label(self, text=VISCTRL_DESC, font=("Helvetica", 20, "italic"))
        visctrl_desc.grid(row=self.ROWCURR, column=0,columnspan=5, sticky="w")
        self.ROWCURR += 1
        ## Button
        visctrl = tk.Button(self, text="Toggle Light", width=20, height=5,
                            command=lambda: ard_obj.toggleBacklight())
        visctrl.grid(row=self.ROWCURR, column=0, sticky="w")
        visctrl['font'] = font.Font(size=20)
        ## image of the magnet on the phagebox
        vis_img_height = 125
        vis_img_width = int(vis_img_height * 1.8)
        vis_load = Image.open("figures/backlight.png").resize((vis_img_width,vis_img_height))
        vis_render = ImageTk.PhotoImage(vis_load)
        vis_img = tk.Label(self, image=vis_render)
        vis_img.image = vis_render
        vis_img.grid(row=self.ROWCURR, column=1, rowspan=1, columnspan=1, sticky='w')
        self.ROWCURR += 1

        # Magentic Control
        self.ROWCURR += 1
        ## label
        magctrl_label = tk.Label(self, text="Magnetic Control", font=("Helvetica", 40))
        magctrl_label.grid(row=self.ROWCURR, column=0,pady=(40, 5), sticky="w")
        self.ROWCURR += 1
        ## Description
        MAGCTRL_DESC= """ The magnetic controller helps with electromagnet activation."""
        magctrl_desc = tk.Label(self, text=MAGCTRL_DESC, font=("Helvetica", 20, "italic"))
        magctrl_desc.grid(row=self.ROWCURR, column=0,columnspan=5, sticky="w")
        self.ROWCURR += 1
        ## Button
        magctrl = tk.Button(self, text="Toggle Magnet", width=20, height=5,
                            command=lambda: ard_obj.toggleMagnet())
        magctrl.grid(row=self.ROWCURR, column=0, sticky="w")
        magctrl['font'] = font.Font(size=20)
        ## image of the magnet on the phagebox
        mag_img_height = 125
        mag_img_width = int(mag_img_height * 1.8)
        mag_load = Image.open("figures/phagebox_magnet.png").resize((mag_img_width,mag_img_height))
        mag_render = ImageTk.PhotoImage(mag_load)
        mag_img = tk.Label(self, image=mag_render)
        mag_img.image = mag_render
        mag_img.grid(row=self.ROWCURR, column=1, rowspan=1, columnspan=1, sticky='w')
        self.ROWCURR += 1

    def addImage(self, pic_path, pic_vec, gridvec):
        """
        If more images are addded, use this to make it clean.
        """
        load = Image.open(pic_path).resize(pic_vec)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=gridvec[0],
                 column=gridvec[1],
                 rowspan=gridvec[2],
                 columnspan=gridvec[3])

######
# MAIN
######
HELPMSG = """

You must have a serial port when using the phagebox GUI.
For example, use the folowing command:

python phagebox_v3.py /dev/cu.usbserial-1440
"""

def main():
    ARG_LENGTH = 2
    if (len(sys.argv) != ARG_LENGTH):
        print(HELPMSG)
        exit(1)
    root = phageBoxGUI(sys.argv[1])
    root.mainloop()

if __name__ == "__main__":
    main()
