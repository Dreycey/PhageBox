#!/usr/local/bin/python3
# in-house packages
import phagebox_modules.control_modules as ctrl
import phagebox_modules.arduino_controller as ard_ctrl
# std packages
import numpy as np
import random
# non-std packages
import tkinter as tk
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
TITLE_FONT= ("Verdana", 30)
style.use("ggplot")

# Page classes
class phageBoxGUI(tk.Tk):
    """
    This class contains all of the code regarding the tkinter GUI used for the
    phagebox software.
    """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Setting properties of the main frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # instantiate the other frame/page classes
        self.frames = {}
        for F in (PCRPage, PhageBoxHome):
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
    PhageBox GUI. This will have navigation buttons to all of the different
    modules available for the PhageBox.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # labels for the page
        label = tk.Label(self, text="PhageBox PCR Module", font=TITLE_FONT)
        label.grid(row=1, column=3)

        # button definitions - navigation
        button1 = tk.Button(self, text="PhageBox PCR", width=10, height=5, command=lambda: controller.show_frame(PCRPage))
        button1.grid(row=2, column=2)

        button2 = tk.Button(self, text="DNA Isolation", width=10, height=5, command=lambda: controller.show_frame(PhageBoxDNAiso))
        button2.grid(row=2, column=3)

        img_height = 500
        img_width = int(img_height * 1.8)
        load = Image.open("figures/phagebox.png").resize((img_width,img_height))
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=3, rowspan=2, columnspan=8)


class PCRPage(tk.Frame):
    """
    This class is responsible for the PCR page of the PhageBot graphical
    user interface.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        ard_obj = ard_ctrl.arduino_controller('/dev/cu.usbserial-1440')

        # labels for the page
        label = tk.Label(self, text="PhageBox PCR Module", font=TITLE_FONT)
        label.grid(row=1, column=2)

        # button definitions - navigation
        button1 = tk.Button(self, text="PhageBox Home", width=10, height=3,
                            command=lambda: controller.show_frame(PhageBoxHome))
        button1.grid(row=2, column=2)

        # button toggle the light
        button2 = tk.Button(self, text="toggle light", width=10, height=3,
                            command=lambda: ard_obj.toggleBacklight())
        button2.grid(row=2, column=3)

        # button definitions - function of page
        ## Input into the page (i.e. config file)
        tk.Label(self, text="Path for the config file").grid(row=3)
        self.e1 = tk.Entry(self)
        self.e1.grid(row=3, column=2)

        ## Output file for actual run
        tk.Label(self, text="Output file for measured temperatures").grid(row=4)
        self.e2 = tk.Entry(self)
        self.e2.grid(row=4, column=2)

        ## Button to trigger Bang Bang Controller
        plotconfig_button = tk.Button(self, text="Plot the config protocol", width=15,
                                    height=2, command=self.temp_trigger)
        plotconfig_button.grid(row=3, column=3)

        bangbang_button = tk.Button(self, text="Run the PCR Simulation", width=15,
                                    height=2, command=self.pcr_trigger)
        bangbang_button.grid(row=4, column=3)

    def plotTempTimeVec(self,tempvec, timevec):
        """
        This method creates a figure with the time and temperature vectors.
        """
        # correcting time and temperature vectors
        timevec2 = [ sum(timevec[:i]) for i in range(len(timevec)) ]
        tempvec2 = []
        for temp_index in range(len(tempvec)):
            for time_i in range(int(timevec[temp_index])): # TODO this is a hack..
                tempvec2.append(tempvec[temp_index])

        # plot the temp vs time figure
        pcr_fig, ax_array = plt.subplots() #Figure(figsize=(8,4), dpi=100)
        #pcr_subfig1 = pcr_fig.add_subplot(111)
        ax_array.plot(range(len(tempvec2)), tempvec2)
        ax_array.set_title("Temperature Regulation of the PhageBox", size=15)
        ax_array.set_ylabel("Temperature (Celsius)")
        ax_array.set_xlabel("Time (minutes)")

        return pcr_fig, ax_array

    def temp_trigger(self):
        """
        This method controls plotting the config file for the PCR.
        """
        config_file_path = self.e1.get()
        pcr_object = ctrl.PhageBoxPCR(config_file_path) #instantiate
        tempvec, timevec = pcr_object.prepareTempVec()

        # displaying to tkinter
        fig, ax_array = self.plotTempTimeVec(tempvec, timevec)
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=6, columnspan=4)

    def pcr_trigger(self):
        """
        This function starts  the communication with the arduino. In essence, it
        calls the PCR control module to impliment a backend controller for
        regulating the temperatures according to an input config file.
        """

        # if len(self.e1.get()) < 1:
        #     print(" \n CANT RUN THIS!! Must input a config file first!! \n")
        #
        # # creating a backend object and calling the bang-bang ctrl
        # config_file_path = self.e1.get()
        # pcr_object = ctrl.PhageBoxPCR(config_file_path)
        # # call the bang bang method call to regulate the temperature
        # pcr_object.bangbang_ctrl(self.e2.get())


        ###### NEW
        config_file_path = self.e1.get()
        pcr_object = ctrl.PhageBoxPCR(config_file_path) #instantiate
        tempvec, timevec = pcr_object.prepareTempVec()

        # correcting time and temperature vectors
        timevec2 = [ sum(timevec[:i]) for i in range(len(timevec)) ]
        tempvec2 = []
        for temp_index in range(len(tempvec)):
            for time_i in range(int(timevec[temp_index])): # TODO this is a hack..
                tempvec2.append(tempvec[temp_index])

        # displaying to tkinter
        fig, ax_array = plt.subplots()

        #self.plotTempTimeVec(fig, ax_array, tempvec, timevec)
        canvas = FigureCanvasTkAgg(fig, self)
        #canvas.draw()
        canvas.get_tk_widget().grid(row=6, columnspan=4)

        x = np.arange(0, 2*np.pi, 0.01)  # x-array

        def animate(i):
            pullData = open(self.e2.get(),"r").read()
            dataList = pullData.split('\n')
            xList = []
            yList = []
            for eachLine in dataList:
                if len(eachLine) > 1:
                    y, x = eachLine.split(',')
                    xList.append(float(x))
                    yList.append(float(y))
            ax_array.clear()
            l1, = ax_array.plot(range(len(tempvec2)), tempvec2)
            l2, = ax_array.plot(xList, yList)
            ax_array.legend((l1, l2), ('PCR Protocol', 'Measured Temp'))
            ax_array.set_title("Temperature Regulation of the PhageBox", size=15)
            ax_array.set_ylabel("Temperature (Celsius)")
            ax_array.set_xlabel("Time (minutes)")

        ani = animation.FuncAnimation(fig, animate, interval=1000)

        # print("it should be working..")
        # ard = ard_ctrl.arduino_controller('/dev/cu.usbserial-1440')
        # x = threading.Thread(target=ard.bangbang(tempvec2,
        #                                          range(len(tempvec2)),
        #                                          self.e2.get(), '2', '1','TEC_1:'),
        #                      args=(1,))
        # x.start()

        tk.update()

def main():
    root = phageBoxGUI()
    root.mainloop()

if __name__ == "__main__":
    main()
