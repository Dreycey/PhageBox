"""
Author: Dreycey Albin

Description:
------------
    This module contains the front end GUI for the phagebox. This 
    interacts with the backend arduino controller.

Design Patterns:
----------------
    1. Composite Pattern - used for the TKinter frames. Each is of type 'BaseView'

Useful Methods/Classes
----------------------
    1. BaseView - base class for the TK frames [enforces a create_view() method]
        (layer 1)
        2. PhageBoxGUI - most outer frame ordering inner frames (layer 1)
            (layer 2)
            3. LogoFrame - frame for displaying the logo (layer 2)
            4. MiscFrame - frame for displaying mag, light, theme buttons (layer 2)
            5. DisplayFrame - frame for displaying the PCR progress in real time (layer 2)
            6. PCRFrame -  frame for displaying the PCR buttons (layer 2)
            (layer 3)
                7. PCRStateFrame - frame for PCR states (layer 3)
"""
# standard library
from sys import float_repr_style
from tkinter import NONE, ttk
import tkinter as tk
from tkinter.filedialog import asksaveasfile
from abc import abstractmethod
from turtle import color
import numpy as np
import time
import webbrowser
# matplotlib imports
import matplotlib
matplotlib.use("TkAgg")
from functools import partial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
# non-standard library
from PIL import ImageTk, Image
import customtkinter
# in-house packages
from src.phagebox_modules.arduino_controller import ArduinoController




class BaseFrame_original(tk.Frame):
    """
    Description:
        Base class acting as template for inherited classes
    """

    corner_radius = 10
    border_width = 1

    def __del__(self):
        """
        Description:
            destuctor added to prevent clashes with
            the custom tkinter package
        """
        print(f"destructor called for original frame: {self}")

    @abstractmethod
    def create_view():
        raise NotImplementedError

    @property
    def phagebox_adapter(self):
        """
        Description:
            If controller exists, use. If not, use parents.
            Propogates the delegation up the class with the 
            delegated controller.
        """
        if self._phagebox_adapter:
            return self._phagebox_adapter
        else:
            return self.parent.phagebox_adapter

    @phagebox_adapter.setter
    def phagebox_adapter(self, phagebox_adapter):
        self._phagebox_adapter = phagebox_adapter
        
    def pelt2chip_temp(self, pelt_temp):
        """
        Description:
            Converts a peliter temperature to the predicted
            chip temperature
        """
        chip_temp = pelt_temp * self.slope + self.y_int
        return chip_temp

    def chip2pelt_temp(self, chip_temp):
        """
        Description:
            Converts a chip temperature to the predicted
            peltier temperature
        """
        pelt_temp = (chip_temp - self.y_int) / self.slope
        return pelt_temp

    @property
    def y_int(self):
        """
        Description:
            If y_intercept exists, use. If not, use parents.
        """
        if self._y_int != None:
            return self._y_int
        else:
            return self.parent.y_int

    @y_int.setter
    def y_int(self, y_intercept):
        self._y_int = y_intercept

    @property
    def slope(self):
        """
        Description:
            If slope attribute exists, use. If not, use parents.
        """
        if self._slope != None:
            return self._slope
        else:
            return self.parent.slope

    @slope.setter
    def slope(self, slope):
        self._slope = slope


class BaseFrame(customtkinter.CTkFrame):
    """
    Description:
        Base class acting as template for inherited classes
    """
    corner_radius = 10
    border_width = 1

    def __del__(self):
        """
        Description:
            destuctor added to prevent clashes with
            the custom tkinter package
        """
        print("destructor called")
        print(f"destructor called for custom frame: {self}")

    @abstractmethod
    def create_view():
        raise NotImplementedError

    def pelt2chip_temp(self, pelt_temp):
        """
        Description:
            Converts a peliter temperature to the predicted
            chip temperature
        """
        chip_temp = pelt_temp * self.slope + self.y_int
        return chip_temp

    def chip2pelt_temp(self, chip_temp):
        """
        Description:
            Converts a chip temperature to the predicted
            peltier temperature
        """
        pelt_temp = (chip_temp - self.y_int) / self.slope
        return pelt_temp

    @property
    def y_int(self):
        """
        Description:
            If y_intercept exists, use. If not, use parents.
        """
        if self._y_int != None:
            return self._y_int
        else:
            return self.parent.y_int

    @y_int.setter
    def y_int(self, y_intercept):
        self._y_int = y_intercept

    @property
    def slope(self):
        """
        Description:
            If slope attribute exists, use. If not, use parents.
        """
        if self._slope != None:
            return self._slope
        else:
            return self.parent.slope

    @slope.setter
    def slope(self, slope):
        self._slope = slope

    @property
    def phagebox_adapter(self):
        """
        Description:
            If controller exists, use. If not, use parents.
            Propogates the delegation up the class with the 
            delegated controller.
        """
        if self._phagebox_adapter != None:
            return self._phagebox_adapter
        else:
            return self.parent.phagebox_adapter

    @phagebox_adapter.setter
    def phagebox_adapter(self, phagebox_adapter):
        self._phagebox_adapter = phagebox_adapter

    def callback(self, url):
        #webbrowser.get('chrome').open("https://github.com/Dreycey/PhageBox", new=0, autoraise=True)
        print("called")
        webbrowser.open(url)


class PhageBoxGUI(BaseFrame):
    """
    Description:
        This class inherets from the abstract-like BaseView class
        for instantiating a tkinter frame.
    Specific Description:
        This class contains the outer-most layer. This is used to control the 
        design of gui and works to organize the overall layout.
    """

    def __init__(self, parent, phagebox_adapter, y_int, slope):
        self.parent : BaseFrame = parent
        self.y_int = y_int
        self.slope = slope
        self.phagebox_adapter : ArduinoController = phagebox_adapter
        super().__init__(parent, background="blue")
        self.start_time = time.time()
        self.temperature_history = [[], [], []]
        self.set_temperature_history = [[], []] #front, back
        self.time_history = []
        # super().grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.pose_predict_state = False
        for row in range(3):
            if row == 1: # skip column 0, only allow stretching column 1
                self.rowconfigure(row, weight=1)
        for col in range(2):
            if col != 0: # skip column 0, only allow stretching column 1
                self.columnconfigure(col, weight=1)
        self.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.create_view()

    def update_temperatures(self):
        """
        Description:
            Updates the temperatures and time information
        """
        # save time
        self.time_history.append(float(time.time() - self.start_time))
        # save temps
        self.temperature_history[0].append(self.pelt2chip_temp(self.phagebox_adapter.current_temperatures[0]))
        self.temperature_history[1].append(self.pelt2chip_temp(self.phagebox_adapter.current_temperatures[1]))
        self.temperature_history[2].append(self.pelt2chip_temp(self.phagebox_adapter.current_temperatures[2]))
        # save set temps
        self.set_temperature_history[0].append(self.pelt2chip_temp(self.phagebox_adapter.set_temperatures[0]))
        self.set_temperature_history[1].append(self.pelt2chip_temp(self.phagebox_adapter.set_temperatures[1]))
        # update time left
        self.pcr_frame.update_time_remaining()

    def create_view(self):
        """
        Description:
            Implemented/concrete abstract method for element display.
        Specific Description:
            This method creates all of the subframes for the GUI. These subframes
            are each considered independnt, giving rise to 'composite pattern' utilized
            here. This view creates the top-most layer (layer 1).
        """
        # create frame for the logo (layer 1)
        misc_frame = LogoFrame(self, None)
        misc_frame.grid(row=0, column=0, rowspan=1, columnspan=2, sticky=tk.W + tk.E)

        # Create frame for misc control (layer 1)
        options_frame = MiscFrame(self, None)
        options_frame.grid(row=1, column=0, pady=2, padx=2, rowspan=1, columnspan=1, sticky=tk.N + tk.S + tk.E + tk.W)

        # Display Frame (layer 1)
        displayFrame = DisplayFrame(self, None)
        displayFrame.grid(row=1, column=1, pady=4, padx=4, rowspan=1, columnspan=1, sticky=tk.N + tk.S + tk.E + tk.W)

        # PCR frame (layer 1)
        self.pcr_frame = PCRFrame(self, None)
        self.pcr_frame.grid(row=2, column=0, pady=2, padx=2, rowspan=1, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)

        # # set the controller
        # self.controller = None

    # def set_controller(self, controller):
    #     """
    #     Set the controller for the view
    #     """
    #     self.phagebox_adapter = controller


class LogoFrame(BaseFrame):
    """
    Description:
        This class inherets from the abstract-like BaseView class
        for instantiating a tkinter frame.
    Specific Description:
        Used for displaying logo.
    """
    
    def __init__(self, parent, phagebox_adapter=None, y_int=None, slope=None):
        self.parent : BaseFrame = parent
        self.y_int = y_int
        self.slope = slope
        self.phagebox_adapter : ArduinoController = phagebox_adapter
        width, height = (100, 30)
        super().__init__(parent, height=height, 
                                 width=width,
                                #  fg_color=("#0E6BA8", "gray38"),
                                 corner_radius=1,
                                 border_color="black",
                                 border_width=0)
        self.create_view()

    def create_view(self):
        """
        Description:
            Implemented/concrete abstract method for element display.
        Specific Description:
            1. Displays the logo (layer 2)
        """
        # =======> GUI widget: logo <=======
        image = Image.open("./figures/logo.png").resize((198,72))
        self.bg_image = ImageTk.PhotoImage(image)
        self.image_label = customtkinter.CTkLabel(master=self, image=self.bg_image)
        self.image_label.grid(row=0, column=0, columnspan=1, pady=2, padx=10, sticky="w")
        self.URL_label = customtkinter.CTkLabel(master=self, text="LINK TO SOURE CODE", text_font=("Roboto Medium", 10), cursor="hand1")
        self.URL_label.grid(row=1, column=0, columnspan=1, pady=0, padx=0, sticky="w")
        self.URL_label.bind("<Button-1>", lambda a: self.callback("https://github.com/Dreycey/PhageBox"))
        
        # =======> GUI widget: empty row for spacing <=======
        self.grid_columnconfigure(1, minsize=20)   # empty row with minsize as spacing

        # =======> GUI widget: text for description <=======
        self.label_radio_group = customtkinter.CTkLabel(master=self,
                                                        text="PhageBox: A DIY Digital Microfluidic Platform for Automated Phage Control",
                                                        text_font=("Roboto Medium", 20))
        self.label_radio_group.grid(row=0, column=1, columnspan=1, pady=2, padx=10, sticky="ew")
        self.columnconfigure(1, weight=1, minsize=2) # allow for expanding/etc


class MiscFrame(BaseFrame):
    """
    Description:
        This class contains the frame that holds buttons for general GPIO,
        as well as buttons for changing the theme of the GUI. Any misc buttons
        will go into this frame.
    """

    def __init__(self, parent, phagebox_adapter=None, y_int=None, slope=None):
        self.parent : BaseFrame = parent
        self.y_int = y_int
        self.slope = slope
        self.phagebox_adapter : ArduinoController = phagebox_adapter
        width, height = (100, 200)
        super().__init__(parent, height=height, 
                                 width=width,
                                #  fg_color=("#0E6BA8", "gray38"),
                                 corner_radius=super().corner_radius,
                                 border_color="black",
                                 border_width=super().border_width)
        self.create_view()

    def toggle_magnet(self):
        """
        Description:
            Used to toggle on/off the magnet using the adapter module
            to the PhageBox.
        """
        print("toggle mag")
        self.phagebox_adapter.toggleMagnet()
        if self.button.text == "Turn OFF":
            # self.button.hover_color = "light green"
            self.button.set_text("Turn ON")
        else:
            # self.button2.hover_color = "red"
            self.button.set_text("Turn OFF")

    def toggle_light(self):
        """
        Description:
            Used to toggle on/off the magnet using the adapter module
            to the PhageBox.
        """
        print("toggle light")
        self.phagebox_adapter.toggleBacklight()
        if self.button2.text == "Turn OFF":
            # self.button2.hover_color = "light green"
            self.button2.set_text("Turn ON")
        else:
            # self.button2.hover_color = "red"
            self.button2.set_text("Turn OFF")

    def change_mode(self):
        """
        Description:
            copied from example in customtkinter.
        """
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def create_view(self):
        """
        Description:
            Implemented/concrete abstract method for element display.
        Specific Description:
            1. Displays the magnetic toggle (layer 2)
            2. Displays the magnetic toggle (layer 2)
            3. Expandable space (layer 2)
            4. Theme switch - customTK (layer 2)
        """
        # =======> GUI widget: magnetic toggle <=======
        self.label_radio_group = customtkinter.CTkLabel(master=self,
                                                        text="Electromagnet Control",
                                                        text_font=("Roboto Medium", 20))
        self.label_radio_group.grid(row=0, column=0, columnspan=1, pady=2, padx=10, sticky="ew")
        self.button = customtkinter.CTkButton(master=self, 
                                              text="Turn ON", 
                                              command=self.toggle_magnet,
                                              width=100,
                                              height=50,
                                            #   fg_color="#0E6BA8",
                                              border_width=1)
                                              #hover_color="red")
        self.button.grid(row=1, column=0, rowspan=1, columnspan=1, padx=1, pady=10, sticky="ew")

        # =======> GUI widget: backlight toggle <=======
        self.label_radio_group2 = customtkinter.CTkLabel(master=self,
                                                        text="Backlight Control",
                                                        text_font=("Roboto Medium", 20))
        self.label_radio_group2.grid(row=2, column=0, columnspan=1, pady=2, padx=10, sticky="ew")
        self.button2 = customtkinter.CTkButton(master=self, 
                                              text="Turn ON", 
                                              command=self.toggle_light,
                                              width=100,
                                              height=50,
                                            #   fg_color="#0E6BA8",
                                              border_width=1)
                                              #hover_color="red")
        self.button2.grid(row=3, column=0, rowspan=1, columnspan=1, padx=1, pady=10, sticky="ew")

        # =======> GUI widget: spacing <=======
        self.grid_rowconfigure(4, minsize=50)   # empty row with minsize as spacing
        self.rowconfigure(4, weight=1, minsize=2) # allow to stretch

        # =======> GUI widget: theme toggle <=======
        self.switch_2 = customtkinter.CTkSwitch(master=self,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_2.grid(row=5, column=0, pady=30, padx=20, sticky="s")


class DisplayFrame(BaseFrame_original):
    """
    Description:
        This class contains the frame that hold the plot showing
        the realtime temperature of the front and back PCR.
    Note:
        Could not use the custom tkinter library here. Functionality 
        for handling matplot lib has not yet been added.
    """

    def __init__(self, parent, phagebox_adapter=None, y_int=None, slope=None):
        self.parent : BaseFrame = parent
        self.y_int = y_int
        self.slope = slope
        self.phagebox_adapter : ArduinoController = phagebox_adapter
        width, height = (100, 200)
        super().__init__(parent, height=height, 
                                 width=width,
                                #  fg_color=("#0E6BA8", "gray38"),
                                #  corner_radius=super().corner_radius,
                                #  border_color="black",
                                #  border_width=super().border_width
                                 )
        # for col in range(3):
        #     self.columnconfigure(col, weight=1, minsize=2)
        self.create_view()


    def init_window(self):

        def animate(i):
            """ this sub function updates the GUI. axis is cm^3 """
            while (len(self.ax.lines) >= 1): 
                self.ax.lines.pop(0)
            # update values
            self.parent.update_temperatures()
            # get temperatures
            metal_temps = self.parent.temperature_history[0]
            front_temps = self.parent.temperature_history[1]
            back_temps = self.parent.temperature_history[2]
            set_front_temps = self.parent.set_temperature_history[0]
            set_back_temps = self.parent.set_temperature_history[1]
            # plot temperatures
            self.ax.plot(self.parent.time_history, metal_temps, color='blue')
            self.ax.plot(self.parent.time_history, front_temps, color='green')
            self.ax.plot(self.parent.time_history, back_temps, color='red')
            self.ax.plot(self.parent.time_history, set_front_temps, color='black')
            self.ax.plot(self.parent.time_history, set_back_temps, color='grey')
            # plot temperatures
            self.ax.legend(['Metal Temps', 'Front Temperature (est.)', 'Back Temperature (est.)', 'Front Temp Set', 'Back Temp Set'])
            return self.ax,

        # init figure
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("PCR temperature")
        self.ax.set_ylabel("Temperature (Celsius)")
        self.ax.set_xlabel("Time (Seconds)")

        # continue
        self.x = np.arange(0, 2*np.pi, 0.01)
        self.line, = self.ax.plot(self.x, np.sin(self.x))         
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        toolbar = NavigationToolbar2Tk(self.canvas, self)                                    
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.ani = animation.FuncAnimation(self.fig, animate, interval=1000, blit=False)

    def create_view(self):
        """
        Description:
            Implemented/concrete abstract method for element display.
        Specific Description:
            1. Displays the PCR information.
        """
        self.init_window()
        None


class PCRFrame(BaseFrame):
    """
    Description:
        This class contains the frame containing buttons and attributes
        for performing PCR. 
    """

    def __init__(self, parent, phagebox_adapter=None, y_int=None, slope=None):
        self.parent : BaseFrame = parent
        self.y_int = y_int
        self.slope = slope
        self.phagebox_adapter : ArduinoController = phagebox_adapter
        self.width, self.height = (400, 400)
        self.pcr_start_time = [0, 0] # keeps track of PCR start time.
        self.time_for_pcr = [0, 0] # keeps track of time needed for PCR.
        super().__init__(parent, height=self.height, 
                                 width=self.width,
                                #  fg_color=("#0E6BA8", "gray38"),
                                 corner_radius=super().corner_radius,
                                 border_color="black",
                                 border_width=super().border_width)
        for col in [2,3,4]:
            self.columnconfigure(col, weight=1, minsize=2)
        self.create_view()

    def update_time_remaining(self):
        """
        Description:
            This method updates the time remaining during a PCR.  
        """
        # calculate time remaining.
        time_remaining_arr = [0,0]
        time_remaining_arr_m = [0,0]
        for pelt_index in [0,1]: # front and back pelt
            if (self.pcr_start_time[pelt_index] != 0):
                time_lapsed =  float(self.parent.time_history[-1]) - float(self.pcr_start_time[pelt_index])
                time_remaining = self.time_for_pcr[pelt_index] - time_lapsed
                time_remaining_arr[pelt_index] = int(time_remaining) # round
                time_remaining_arr_m[pelt_index] = int(time_remaining/60) # round
            else:
                time_remaining_arr[pelt_index] = "OFF"
                time_remaining_arr_m[pelt_index] = "OFF"
        # update text.

        self.label_time_remaining.set_text(f"Time Remaining - Front: {time_remaining_arr[0]} s ({time_remaining_arr_m[0]} m), Back: {time_remaining_arr[1]} s ({time_remaining_arr_m[1]} m)")

    def save_data(self):
        """
        Description:
            This method saves the data to a specified file.
        """
        # open file
        Files = [('Text Document', '*.csv')]
        file = asksaveasfile(filetypes = Files, defaultextension = Files)
        # get data to save (time, temperatures, set temperatures)
        times = self.parent.time_history
        metal_temps = self.parent.temperature_history[0]
        front_temps = self.parent.temperature_history[1]
        back_temps = self.parent.temperature_history[2]
        set_front_temps = self.parent.set_temperature_history[0]
        set_back_temps = self.parent.set_temperature_history[1]
        # save to file
        file.write(f"Time,Front-temp,Front-temp Setting,Back-temp,Back-temp Setting,Metal Temp\n")
        for ind in range(len(times)):
            file.write(f"{times[ind]},")
            file.write(f"{front_temps[ind]},{set_front_temps[ind]},") # front temps
            file.write(f"{back_temps[ind]},{set_back_temps[ind]},") # back temps
            file.write(f"{metal_temps[ind]}\n") # metal temps

    def stop_pcr(self):
        """
        Description:
            This method stops PCR for a chosen peliter.
        """
        peltier = self.radio_var.get()
        self.phagebox_adapter.start_pcr(peltier=self.radio_var.get(), 
                                        cycles=0,
                                        d_temp=0, 
                                        d_time=0, 
                                        a_temp=0,
                                        a_time=0, 
                                        e_temp=0, 
                                        e_time=0
                                        )
        # stop PCR timing
        if peltier == 3: # if both.
            self.pcr_start_time[0] = 0
            self.pcr_start_time[1] = 0
            self.time_for_pcr[0] = 0
            self.time_for_pcr[1] = 0
        else:
            self.pcr_start_time[peltier-1] = 0
            self.time_for_pcr[peltier-1] = 0
                            
    def toggle_pcr(self):
        """
        Description:
            This method starts PCR for a chosen peliter.
        """
        # start the pcr.
        peltier = self.radio_var.get()
        num_cyles=float(self.cycle_count.get())
        d_temp=self.chip2pelt_temp(float(self.denaturation_state.temp_set.get()))
        d_time=float(self.denaturation_state.time_set.get())
        a_temp=self.chip2pelt_temp(float(self.annealing_state.temp_set.get()))
        a_time=float(self.annealing_state.time_set.get())
        e_temp=self.chip2pelt_temp(float(self.extension_state.temp_set.get()))
        e_time=float(self.extension_state.time_set.get())
        # start the PCR
        self.phagebox_adapter.start_pcr(peltier=peltier, 
                                        cycles=num_cyles, 
                                        d_temp=d_temp, 
                                        d_time=d_time, 
                                        a_temp=a_temp, 
                                        a_time=a_time, 
                                        e_temp=e_temp, 
                                        e_time=e_time
                                        )
        # add start time and time it will take.
        total_time_for_pcr =  num_cyles * (d_time + a_time + e_time)
        if peltier == 3: # if both.
            self.pcr_start_time[0] = self.parent.time_history[-1]
            self.pcr_start_time[1] = self.parent.time_history[-1]
            self.time_for_pcr[0] = total_time_for_pcr
            self.time_for_pcr[1] = total_time_for_pcr
        else:
            self.pcr_start_time[peltier-1] = self.parent.time_history[-1]
            self.time_for_pcr[peltier-1] = total_time_for_pcr
            
    def create_view(self):
        """
        Description:
            Implemented/concrete abstract method for element display.
        Specific Description:
            1. Displays the PCR controls
        """
        self.radio_var = tk.IntVar(value=1)

        # # =======> GUI widget: label for choosing peliter <=======
        # self.label_radio_group = customtkinter.CTkLabel(master=self,
        #                                                 text="Choose a PCR location:",
        #                                                 text_font=("Roboto Medium", 20))
        # self.label_radio_group.grid(row=0, column=0, columnspan=1, pady=1, padx=10, sticky="s")

        # =======> GUI widget: radio button for front peliter <=======
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self,
                                                           variable=self.radio_var,
                                                           text="Front Peliter",
                                                           value=1)
        self.radio_button_1.grid(row=0, column=0, pady=10, padx=3, sticky="n")

        # =======> GUI widget: radio button for back peliter <=======
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self,
                                                           variable=self.radio_var,
                                                           text="Back Peliter",
                                                           value=2)
        self.radio_button_2.grid(row=1, column=0, pady=3, padx=3, sticky="n")

        # =======> GUI widget: radio button for both peliter <=======
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self,
                                                           variable=self.radio_var,
                                                           text="Both Peliter",
                                                           value=3)
        self.radio_button_2.grid(row=2, column=0, pady=3, padx=3, sticky="n")

        # =======> GUI widget: Start/Stop PCR <=======
        self.label_radio_group2 = customtkinter.CTkLabel(master=self,
                                                        text="PCR Control",
                                                        text_font=("Roboto Medium", 20))
        self.label_radio_group2.grid(row=0, column=1, columnspan=1, pady=2, padx=10, sticky="ewn")
        self.button2 = customtkinter.CTkButton(master=self, 
                                              text="START PCR", 
                                              command=self.toggle_pcr,
                                              width=100,
                                              height=20,
                                              border_width=1)
        self.button2.grid(row=1, column=1, rowspan=2, columnspan=1, padx=1, pady=1, sticky="ewn")
        self.button3 = customtkinter.CTkButton(master=self, 
                                              text="STOP PCR", 
                                              command=self.stop_pcr,
                                              width=100,
                                              height=20,
                                              border_width=1)
        self.button3.grid(row=2, column=1, rowspan=2, columnspan=1, padx=1, pady=1, sticky="ewn")

        # =======> GUI widget: Set Number of cycles <=======
        self.label_radio_group = customtkinter.CTkLabel(master=self,
                                                        text_font=("Roboto Medium", 20),
                                                        text="Set the cycle count")
        self.label_radio_group.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        self.cycle_count = customtkinter.CTkEntry(master=self,
                                                  placeholder_text="32",
                                                  width=120,
                                                  height=30)
        self.cycle_count.grid(row=3, column=0, columnspan=2, pady=1, padx=1, sticky="new")

        # =======> GUI widget: button for chooing output file <=======
        # self.label_radio_group2 = customtkinter.CTkLabel(master=self,
        #                                                 text="Choose file to store data",
        #                                                 text_font=("Roboto Medium", 20))
        # self.label_radio_group2.grid(row=3, column=0, columnspan=2, pady=1, padx=1, sticky="ew")
        self.button2 = customtkinter.CTkButton(master=self, 
                                              text="Open file to store data", 
                                              command=self.save_data,
                                              width=100,
                                              height=50,
                                              border_width=1)
        self.button2.grid(row=4, column=0, rowspan=1, columnspan=2, padx=1, pady=1, sticky="ewn")

        # =======> GUI widget: Label for PCR desription <=======
        self.label_radio_group = customtkinter.CTkLabel(master=self,
                                                        width=200,
                                                        height=20,
                                                        text_font=("Roboto Medium", 20),
                                                        text="Set PCR parameters")
        self.label_radio_group.grid(row=0, column=2, rowspan=1, columnspan=3, pady=1, padx=1, sticky="ns")

        # =======> GUI widget: Time remaining for PCR <=======
        self.label_time_remaining = customtkinter.CTkLabel(master=self,
                                                        width=200,
                                                        height=20,
                                                        text_font=("Roboto Medium", 15),
                                                        text="Time Remaining: X")
        self.label_time_remaining.grid(row=1, column=2, rowspan=1, columnspan=3, pady=0, padx=0, sticky="ns")

        # =======> GUI widget: Denaturing <=======
        self.denaturation_state : PCRStateFrame = PCRStateFrame(self, "Denaturation", 
                                                                      default_time=15,
                                                                      default_temp=90)
        self.denaturation_state.grid(row=2, column=2, rowspan=3, pady=10, padx=2, sticky="ns")

        # =======> GUI widget: Annealing <=======
        self.annealing_state : PCRStateFrame = PCRStateFrame(self, "Annealing",
                                                                      default_time=20,
                                                                      default_temp=50)
        self.annealing_state.grid(row=2, column=3, rowspan=3, pady=10, padx=2, sticky="ns")

        # =======> GUI widget: Extension <=======
        self.extension_state : PCRStateFrame = PCRStateFrame(self, "Extension",
                                                                      default_time=60,
                                                                      default_temp=72)
        self.extension_state.grid(row=2, column=4, rowspan=3, pady=10, padx=2, sticky="ns")


class PCRStateFrame(BaseFrame):
    """
    Description:
        This class contains a frame for controlling the state
        of PCR. It assumes each temperature of PCR can be can 
        be assumed to have a state.
    """

    def __init__(self, parent, state_name, default_time, default_temp, phagebox_adapter=None):
        self.parent : BaseFrame = parent
        self.phagebox_adapter : ArduinoController = phagebox_adapter
        self.state_name = state_name
        self.default_time = default_time
        self.default_temp = default_temp
        self.width, self.height = (300, 400)
        super().__init__(parent, height=self.height, 
                                 width=self.width,
                                #  fg_color=("#0E6BA8", "gray38"),
                                 corner_radius=super().corner_radius,
                                 border_color="black",
                                 border_width=super().border_width
                                 )
        self.create_view()

    def create_view(self):
        """
        Description:
            Implemented/concrete abstract method for element display.
        Specific Description:
            1. Displays the PCR controls
        """
        # =======> GUI widget: Label <=======
        self.label_radio_group = customtkinter.CTkLabel(master=self,
                                                        width=200,
                                                        height=50,
                                                        text_font=("Roboto Medium", 20),
                                                        text=self.state_name)
        self.label_radio_group.grid(row=0, column=0, columnspan=1, pady=1, padx=10, sticky="s")

        # =======> GUI widget: Time <=======
        self.label_radio_group = customtkinter.CTkLabel(master=self,
                                                        width=120,
                                                        height=25,
                                                        text="Set the time (Seconds)")
        self.label_radio_group.grid(row=1, column=0, columnspan=1, pady=0, padx=0, sticky="s")
        self.time_set = customtkinter.CTkEntry(master=self,
                                               placeholder_text=self.default_time,
                                               width=120,
                                               height=30)
        self.time_set.grid(row=2, column=0, columnspan=1, pady=10, padx=10, sticky="n")

        # =======> GUI widget: Temp <=======
        self.label_radio_group = customtkinter.CTkLabel(master=self,
                                                        width=120,
                                                        height=25,
                                                        text="Set the temperature (Celsius)")
        self.label_radio_group.grid(row=3, column=0, columnspan=1, pady=0, padx=0, sticky="s")
        self.temp_set = customtkinter.CTkEntry(master=self,
                                               placeholder_text=self.default_temp,
                                               width=120,
                                               height=30)
        self.temp_set.grid(row=4, column=0, columnspan=1, pady=10, padx=10, sticky="n")