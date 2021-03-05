#!/usr/local/bin/python3
# in-house packages
import control_modules as ctrl 
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
        button1 = tk.Button(self, text="PhageBox PCR", width=10, height=5,                                                   command=lambda: controller.show_frame(PCRPage))   
        button1.grid(row=2, column=2)

        button2 = tk.Button(self, text="DNA Isolation", width=10, height=5,                                                  command=lambda: controller.show_frame(PhageBoxDNAiso))   
        button2.grid(row=2, column=3)        
        
        button3 = tk.Button(self, text="Phage Titer Assay", width=10, height=5,                                              command=lambda: controller.show_frame(TiterAssay))   

class PCRPage(tk.Frame):
    """
    This class is responsible for the PCR page of the PhageBot graphical 
    user interface. 
    """
   
    def __init__(self, parent, controller):                                     
        tk.Frame.__init__(self, parent) 
        # labels for the page                                        
        label = tk.Label(self, text="PhageBox PCR Module", font=TITLE_FONT)             
        label.grid(row=1, column=2)
                                             
        # button definitions - navigation
        button1 = tk.Button(self, text="PhageBox Home", width=10, height=3,                                                  command=lambda: controller.show_frame(PhageBoxHome))   
        button1.grid(row=2, column=2)

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

    def temp_trigger(self):
        """
        This method controls plotting the config file for the PCR.
        """
        config_file_path = self.e1.get()
        pcr_object = ctrl.PhageBoxPCR(config_file_path)
        tempvec, timevec = pcr_object.prepareTempVec()
        # correcting time and temperature vectors
        timevec2 = [ sum(timevec[:i]) for i in range(len(timevec)) ]
        tempvec2 = []
        for temp_index in range(len(tempvec)): 
            for time_i in range(int(timevec[temp_index])): # TODO this is a hack..
                tempvec2.append(tempvec[temp_index])
        # plot the temp vs time figure
        pcr_fig = Figure(figsize=(8,4), dpi=100) 
        pcr_subfig1 = pcr_fig.add_subplot(111)
        pcr_subfig1.plot(range(len(tempvec2)),  tempvec2)
        pcr_subfig1.set_title("Temperature Regulation of the PhageBox", size=15)
        pcr_subfig1.set_ylabel("Temperature (Celsius)")
        pcr_subfig1.set_xlabel("Time (minutes)")
        # displaying to tkinter
        canvas = FigureCanvasTkAgg(pcr_fig, self) 
        canvas.draw()
        canvas.get_tk_widget().grid(row=6, columnspan=4)
        # making the toolbar
        toolbar = NavigationToolbar2TkAgg(canvas, self) #TODO wtf is "canvas"      
        toolbar.update()
        canvas._tkcanvas.grid(row=4, column=1)

    def pcr_trigger():
        """
        This function starts  the communication with the arduino. In essence, it
        calls the PCR control module to impliment a backend controller for
        regulating the temperatures according to an input config file. 
        """
        
        if len(self.e1.get()) < 1:
            print(" \n CANT RUN THIS!! Must input a config file first!! \n")
        
        # creating a backend object and calling the bang-bang ctrl
        config_file_path = self.e1.get()
        pcr_object = ctrl.PhageBoxPCR(config_file_path)
        # call the bang bang method call to regulate the temperature
        pcr_object.bangbang_ctrl(self.e2.get())       
 

class TiterAssay(tk.Frame):
    """
    """
    pass

class PhageBoxDNAiso(tk.Frame):
    """
    """
    pass

class PCRPage2(tk.Frame):
    """
    """   
    pass



root = phageBoxGUI()
#ani = animation.FuncAnimation(f, animate, interval=1000)
root.mainloop()

#def main():
#    """
#    controls the entire gui/backend
#    """
#    root = phageBoxGUI()
#    root.mainloop()
#
#if __name__ == "__main()__":
#    root = phageBoxGUI()
#    root.mainloop()
