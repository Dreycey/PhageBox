#!/usr/local/bin/python3
"""
This module contains all of the source code used for
creating the tkinter GUI. Different functions for making
the phagebox layout can be found in this python file.
"""
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




# Globals
LARGE_FONT= ("Verdana", 12)
TITLE_FONT= ("Verdana", 40)
style.use("ggplot")
g_THREAD_STATE = 0

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
        """
        Constructor for the home page
        """
        tk.Frame.__init__(self, parent)

        # save an attribute for the ser port
        self.ser_port = controller.ser_port
        self.ROWCURR = 0
        self.ard_process = [None, None] # arduino process
        # TODO: DELETE: self.ard = [None, None]
        self.ard_obj = ard_ctrl.arduino_controller(self.ser_port)
        self.configEntryList = [None, None, None]
        self.parse_cmds = [('1', '2', 'TEC_MET:'),('3', '4', 'TEC_2:')]
        self.current_fig = None
        self.tempoutfileEntry = None
        self.temp_bool = False # i.e. is the temp being used

        # creating canvas to allow for scroll bar
        ## instantiate
        self.canvas = tk.Canvas(self, borderwidth=0, width=810,height=500) # background="#ffffff",
        self.frame = tk.Frame(self.canvas) #background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        ## connect scroll bar with canvas
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        ## connect frame with canvas
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)

        ####
        # SET UP SECTIONS ON FRAME
        ####
        # set up main header
        self.set_mainheader()
        # set up visual controller
        self.set_viscontroller()
        # set up magnets controller
        self.set_magcontroller()
        # set up temperature controller
        self.set_tempcontroller()
        # set up the buttons
        self.set_tempbuttons()

    def set_tempbuttons(self):
        """
        This method organizes all of the temperature buttons, etc
        """
        # Start button
        config_label = tk.Label(self.frame, text="Starting/Stopping PCR ", font=("Helvetica", 20, "bold"))
        config_label.grid(row=self.ROWCURR, sticky="w", column=0, pady=(20, 5))
        self.ROWCURR += 1
        ## Button
        temp1ctrl = tk.Button(self.frame, text="START TEMP", width=20, height=5,
                            command=lambda: self.start_button())
        temp1ctrl.grid(row=self.ROWCURR, column=0, sticky="w")
        temp1ctrl['font'] = font.Font(size=10)
        # Stop button
        temp2ctrl = tk.Button(self.frame, text="STOP TEMP", width=20, height=5,
                            command=lambda: self.stop_button())
        temp2ctrl.grid(row=self.ROWCURR, column=0, sticky="e")
        temp2ctrl['font'] = font.Font(size=10)
        # visualize button
        temp3ctrl = tk.Button(self.frame, text="Plot output file", width=20, height=5,
                              command=lambda: self.plot_outputfile())
        temp3ctrl.grid(row=self.ROWCURR, column=1, sticky="w", padx=(40, 0))
        temp3ctrl['font'] = font.Font(size=10)
        self.ROWCURR += 1

    def set_mainheader(self):
        """
        This method sets the title for the  GUI
        """
        # labels for the page
        label = tk.Label(self.frame, text="The PhageBox GUI", font=("Helvetica", 70))
        label.grid(row=0, column=0, columnspan=2, sticky="e")
        self.ROWCURR += 1
        ## image of the phagebox
        img_height = 200
        img_width = int(img_height * 4)
        self.addImage("figures/phagebox_banner.png",[img_width,img_height], [self.ROWCURR,0,2,8])
        self.ROWCURR += 2
        ## Description of the phagebox
        PHAGEBOX_DESC = """ The Phagebox is a DMF device attatchment that allows for"""
        PHAGEBOX_DESC += """ enhanced control over the \n DropBot. This works by having """
        PHAGEBOX_DESC += """ heating elements as well as magnetic elements \n for initiating"""
        PHAGEBOX_DESC += """ PCR and DNA immobilization, respectively. The controllers below allow \n"""
        PHAGEBOX_DESC += """ for researchers to easily control the attachment device, while \n"""
        PHAGEBOX_DESC += """ simultaneously controlling the DropBot device seperately. \n"""
        phagebox_desc = tk.Label(self.frame, text=PHAGEBOX_DESC, font=("Helvetica", 20, "italic"))
        phagebox_desc.grid(row=self.ROWCURR, column=0, columnspan=20)
        self.ROWCURR += 1

    def set_viscontroller(self):
        """
        This method sets informaton and button for the back light
        """
        # Visual Control
        self.ROWCURR += 1
        ## label
        visctrl_label = tk.Label(self.frame, text="Visual Control", font=("Helvetica", 40))
        visctrl_label.grid(row=self.ROWCURR, column=0, pady=(40, 5), sticky="w")
        self.ROWCURR += 1
        ## Description
        VISCTRL_DESC= """ The visual controller helps with lighting on the phage box."""
        visctrl_desc = tk.Label(self.frame, text=VISCTRL_DESC, font=("Helvetica", 20, "italic"))
        visctrl_desc.grid(row=self.ROWCURR, column=0,columnspan=5, sticky="w")
        self.ROWCURR += 1
        ## Button
        visctrl = tk.Button(self.frame, text="Toggle Light", width=20, height=5,
                            command=lambda: self.ard_obj.toggleBacklight())
        visctrl.grid(row=self.ROWCURR, column=0, sticky="w")
        visctrl['font'] = font.Font(size=20)
        ## image of the magnet on the phagebox
        vis_img_height = 125
        vis_img_width = int(vis_img_height * 1.8)
        vis_load = Image.open("figures/backlight.png").resize((vis_img_width,vis_img_height))
        vis_render = ImageTk.PhotoImage(vis_load)
        vis_img = tk.Label(self.frame, image=vis_render)
        vis_img.image = vis_render
        vis_img.grid(row=self.ROWCURR, column=1, rowspan=1, columnspan=1, sticky='w')
        self.ROWCURR += 1

    def set_magcontroller(self):
        """
        This method sets informaton and buttons for the electromagnet
        """
        # Magentic Control
        self.ROWCURR += 1
        ## label
        magctrl_label = tk.Label(self.frame, text="Magnetic Control", font=("Helvetica", 40))
        magctrl_label.grid(row=self.ROWCURR, column=0, pady=(40, 5), sticky="w")
        self.ROWCURR += 1
        ## Description
        MAGCTRL_DESC= """ The magnetic controller helps with electromagnet activation."""
        magctrl_desc = tk.Label(self.frame, text=MAGCTRL_DESC, font=("Helvetica", 20, "italic"))
        magctrl_desc.grid(row=self.ROWCURR, column=0,columnspan=5, sticky="w")
        self.ROWCURR += 1
        ## Button
        magctrl = tk.Button(self.frame, text="Toggle Magnet", width=20, height=5,
                            command=lambda: self.ard_obj.toggleMagnet())
        magctrl.grid(row=self.ROWCURR, column=0, sticky="w")
        magctrl['font'] = font.Font(size=20)
        ## image of the magnet on the phagebox
        mag_img_height = 125
        mag_img_width = int(mag_img_height * 1.8)
        mag_load = Image.open("figures/phagebox_magnet.png").resize((mag_img_width,mag_img_height))
        mag_render = ImageTk.PhotoImage(mag_load)
        mag_img = tk.Label(self.frame, image=mag_render)
        mag_img.image = mag_render
        mag_img.grid(row=self.ROWCURR, column=1, rowspan=1, columnspan=1, sticky='w')
        self.ROWCURR += 1

    def set_tempcontroller(self):
        """
        This method sets informaton and buttons for the temperature controller
        """
        # Temperature Control
        self.ROWCURR += 1
        ## label
        tempctrl_label = tk.Label(self.frame, text="Temperature Control", font=("Helvetica", 40))
        tempctrl_label.grid(row=self.ROWCURR, column=0, pady=(40, 5), sticky="w")
        self.ROWCURR += 1
        ## Description
        TEMPCTRL_DESC= """ The temperature controller helps with chip temperature and PCR."""
        tempctrl_desc = tk.Label(self.frame, text=TEMPCTRL_DESC, font=("Helvetica", 20, "italic"))
        tempctrl_desc.grid(row=self.ROWCURR, column=0,columnspan=5, sticky="w", pady=(0, 20))
        self.ROWCURR += 1
        ## output temp file
        out_label = tk.Label(self.frame, text="Output file path: ", font=("Helvetica", 20))
        out_label.grid(row=self.ROWCURR, columnspan=1, sticky="w")
        self.e2 = tk.Entry(self.frame)
        self.tempoutfileEntry = self.e2
        self.e2.grid(row=self.ROWCURR, column=0, sticky="e")
        out_label2 = tk.Label(self.frame, text="Note: MUST SPECIFY! (automatically saved)", font=("Helvetica", 20))
        out_label2.grid(row=self.ROWCURR, column=1, columnspan=7)
        self.ROWCURR += 1

        ## config file
        config_label = tk.Label(self.frame, text="Set a constant temp: ", font=("Helvetica", 20))
        config_label.grid(row=self.ROWCURR, sticky="w", column=0)
        self.e3 = tk.Entry(self.frame)
        self.e3.grid(row=self.ROWCURR, column=0, sticky="e")
        self.configEntryList[2] = self.e3
        out_label2 = tk.Label(self.frame, text="Note: Don't add config paths, if selected", font=("Helvetica", 20))
        out_label2.grid(row=self.ROWCURR, column=1, columnspan=6, stick="w")
        self.ROWCURR += 1

        ## Peltier module 1
        config_label = tk.Label(self.frame, text="Peltier Module 1 ", font=("Helvetica", 20, "bold"))
        config_label.grid(row=self.ROWCURR, sticky="w", column=0, pady=(20, 5))
        self.ROWCURR += 1
        config_label = tk.Label(self.frame, text="Config file path: ", font=("Helvetica", 20))
        config_label.grid(row=self.ROWCURR, sticky="w", column=0)
        self.e4 = tk.Entry(self.frame)
        self.configEntryList[0] = self.e4
        self.e4.grid(row=self.ROWCURR, column=0, sticky="e")
        mod1ctrl = tk.Button(self.frame, text="Plot Config", width=20, height=5,
                            command=lambda: self.temp_trigger(self.e4))
        mod1ctrl.grid(row=self.ROWCURR, column=1, sticky="w")
        mod1ctrl['font'] = font.Font(size=10)
        self.ROWCURR += 1

        ## Peltier module 2
        config_label = tk.Label(self.frame, text="Peltier Module 2 ", font=("Helvetica", 20, "bold"))
        config_label.grid(row=self.ROWCURR, sticky="w", column=0, pady=(20, 5))
        self.ROWCURR += 1
        config_label2 = tk.Label(self.frame, text="Config file path: ", font=("Helvetica", 20))
        config_label2.grid(row=self.ROWCURR, sticky="w", column=0)
        self.e5 = tk.Entry(self.frame)
        self.configEntryList[1] = self.e5
        self.e5.grid(row=self.ROWCURR, column=0, sticky="e")
        mod2ctrl = tk.Button(self.frame, text="Plot Config", width=20, height=5,
                            command=lambda: self.temp_trigger(self.e5))
        mod2ctrl.grid(row=self.ROWCURR, column=1, sticky="w")
        mod2ctrl['font'] = font.Font(size=10)
        self.ROWCURR += 1

    def plot_outputfile(self):
        """
        Here the plot for the ongoing PCR is made.
        """
        # initialize output file if it doesn't exist
        if not path.exists(self.tempoutfileEntry.get()):
            outfile = open(self.tempoutfileEntry.get(), "w+")
            outfile.close()

        if (len(self.configEntryList[0].get()) > 1):
            tempvec2, timevec = self.getTempVec(0) #TODO allow for other backgrounds
        # displaying to tkinter
        fig, ax_array = plt.subplots()

        #self.plotTempTimeVec(fig, ax_array, tempvec, timevec)
        canvas = FigureCanvasTkAgg(fig, self.frame)
        #canvas.draw()
        # TODO: make sure to be able to press plot multiple times with no issue
        canvas.get_tk_widget().grid(row=self.ROWCURR, columnspan=6)

        x = np.arange(0, 2*np.pi, 0.01)  # x-array

        def animate(i):
            pullData = open(self.tempoutfileEntry.get(),"r").read()
            dataList = pullData.split('\n')
            timeList = []
            t1List = []
            t2List = []
            t3List = []
            for eachLine in dataList:
                if len(eachLine) > 1:
                    time, t1, t2, t3 = eachLine.split(',')
                    timeList.append(float(time))
                    t1List.append(float(t1))
                    t2List.append(float(t2))
                    t3List.append(float(t3))
            ax_array.clear()
            if (len(self.configEntryList[0].get()) > 1):
                l1, = ax_array.plot(range(len(tempvec2)), tempvec2)
            l2, = ax_array.plot(timeList, t1List)
            l3, = ax_array.plot(timeList, t2List)
            l4, = ax_array.plot(timeList, t3List)
            if (len(self.configEntryList[0].get()) > 1):
                ax_array.legend((l1, l2, l3, l4), ('PCR Protocol', 'TEC 1', 'TEC 2', 'TEC metal'))
            else:
                ax_array.legend((l2, l3, l4), ('PCR Protocol', 'TEC 1', 'TEC 2', 'TEC metal'))
            ax_array.set_title("Temperature Regulation of the PhageBox", size=15)
            ax_array.set_ylabel("Temperature (Celsius)")
            ax_array.set_xlabel("Time (Seconds)")

        ani = animation.FuncAnimation(fig, animate, interval=1000)

        tk.update()

    def start_button(self):
        """ this starts whatever is set in the GUI wrt temp control"""
        if (self.temp_bool == False):
            if ((len(self.configEntryList[0].get()) != 0) and
               (len(self.configEntryList[1].get()) != 0)):
                print("BOTH ARE FILLED OUT")
                self.temp_bool = True
                self.arduino_on(self.tempoutfileEntry, 0)
                self.arduino_on(self.tempoutfileEntry, 1, True)

            elif (len(self.configEntryList[0].get()) != 0):
                print("just module 1 filled out")
                self.temp_bool = True
                self.arduino_on(self.tempoutfileEntry, 0)

            elif (len(self.configEntryList[1].get()) != 0):
                print("just module 2 filled out")
                self.temp_bool = True
                self.arduino_on(self.tempoutfileEntry, 1)

            elif (len(self.configEntryList[2].get()) != 0):
                print("constant temp specified")
                self.temp_bool = True
                self.arduino_on(self.configEntryList[2], 0, False, True)
                #self.ard_obj.setConstantTemp(self.configEntryList[2].get())
            else:
                print("No temperature info is filled out!")
        else:
            print(" \n\n Temperature regulation is already in progress!")
            print("Press the stop button to restart \n\n")

    def stop_button(self):
        """ this stops whatever is set in the GUI wrt temp control"""
        if (self.temp_bool == True):
            self.temp_bool = False
            self.arduino_off(self.tempoutfileEntry, 0)
            self.arduino_off(self.tempoutfileEntry, 1)
        else:
            print("\n\n Nothing is running! \n\n")

    def getTempVec(self, peltnumber):
        """ returns the temperature vector in the correct format """
        ###### NEW
        config_file_path = self.configEntryList[peltnumber].get()
        pcr_object = ctrl.PhageBoxPCR(config_file_path) #instantiate
        tempvec, timevec = pcr_object.prepareTempVec()

        # correcting time and temperature vectors
        timevec2 = [ sum(timevec[:i]) for i in range(len(timevec)) ]
        tempvec2 = []
        for temp_index in range(len(tempvec)):
            for time_i in range(int(timevec[temp_index])): # TODO this is a hack..
                tempvec2.append(tempvec[temp_index])

        return tempvec2, timevec

    def arduino_on(self, outfileentry, peltnumber, two=False, const=False):
        """ turns the arduino on """
        print("Now starting the arduino")
        if not path.exists(outfileentry.get()):
            outfile = open(outfileentry.get(), "w+")
            outfile.close()

        print(f"here is ard: {self.ard_obj}")
        #self.ard[peltnumber] = ard_ctrl.arduino_controller(self.ser_port)
        # multiprocess
        if (const == False): # bang-bang
            ontrig, offtrig, parsestring = self.parse_cmds[peltnumber]
            tempvec2, timevec = self.getTempVec(peltnumber)
            # self.ard_process[peltnumber] = Process(target=self.ard_obj.bangbang,
            #                                        args=(tempvec2,range(len(tempvec2)),
            #                                        outfileentry.get(), ontrig, offtrig,
            #                                        parsestring, two))

            self.ard_process[peltnumber] = threading.Thread(target=self.ard_obj.bangbang,
                                                  args=(tempvec2,range(len(tempvec2)),
                                                        outfileentry.get(), ontrig, offtrig,
                                                        parsestring, two)
                                                    )
        else: # constant temperature
            print(f"here whats going in {outfileentry.get()}")
            # self.ard_process[peltnumber] = Process(target=self.ard_obj.setConstantTemp,
            #                                        args=( float(outfileentry.get()),
            #                                               self.tempoutfileEntry.get(),
            #                                             )
            #                                       )
            self.ard_process[peltnumber] = threading.Thread(target=self.ard_obj.setConstantTemp,
                                                            args=(float(outfileentry.get()),
                                                                  self.tempoutfileEntry.get(),
                                                        )
                                                    )

        self.ard_process[peltnumber].start()

    def arduino_off(self, outfileentry, peltnumber):
        """ turns the arduino off """
        print("Now stopping the arduino, if a process exists")
        if (self.ard_process[peltnumber] != None):
            print(f"stopping process for peltier: {peltnumber}")
            self.ard_process[peltnumber]._stop()
            #TODO: may need to call destructor like below
            #self.ard[peltnumber] = None
            self.ard_process[peltnumber] = None
            # Restart the object to call the destructor
            self.ard_obj = None
            self.ard_obj = ard_ctrl.arduino_controller(self.ser_port)
        else:
            print(f"there is no process for peltier: {peltnumber}")

    def temp_trigger(self, entryin):
        """
        This method controls plotting the config file for the PCR.
        """
        print(f" this is the entry: {entryin.get()}")
        # close old figs if any exist for efficient memory
        if (self.current_fig != None):
            plt.close('all')
            self.current_fig.get_tk_widget().destroy()

        config_file_path = entryin.get()
        pcr_object = ctrl.PhageBoxPCR(config_file_path) #instantiate
        tempvec, timevec = pcr_object.prepareTempVec()

        # displaying to tkinter
        fig, ax_array = self.plotTempTimeVec(tempvec, timevec)
        canvas = FigureCanvasTkAgg(fig, self.frame)
        self.current_fig = canvas
        canvas.draw()
        canvas.get_tk_widget().grid(row=self.ROWCURR, columnspan=6)

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

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def addImage(self, pic_path, pic_vec, gridvec):
        """
        If more images are addded, use this to make it clean.
        """
        load = Image.open(pic_path).resize(pic_vec)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self.frame, image=render)
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

General Usage:
python phagebox_v4.py <port for serial/UART communication>

if mac:
python phagebox_v4.py /dev/cu.usbserial-1440

if Windows:
python phagebox_v4.py COM2
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
