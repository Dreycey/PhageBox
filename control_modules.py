from time import sleep
import serial
import numpy, sys
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation
#from matplotlib.figure import Figure

def animate(i):
    pullData = open("s2.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            y, x = eachLine.split(',')
            xList.append(float(x))
            yList.append(float(y))
    ax_array.clear()
    ax_array.plot(range(len(tempvec2)), tempvec2)
    ax_array.plot(xList, yList)

class arduino_controller():
    """
    This class contains methods for controlling the arduino.
    """
     
    def __init__(self, port_in):
        """
        initialization for the class for controlling the arduino
        """
        self.ser = serial.Serial('/dev/tty.usbmodem141101', 9600)

    def bangbang(self, tempvec, timevec, outpath):
        """
        This method impliments the bang bang controller for controlling the
        temperature of the peltier modules conected to the arduino. 
        """ 
        temp_vec = [] # stores all of the temperatures
        counter_vec = []
        counter1 = 0
        time_i = 0
        
        relayon = True
        ser.write(b'1')

        while True:
             counter1 += 1
             print(ser.readline()) # Read the newest output from the Arduino
             temperature_i = str(ser.readline())
         
             # parse the string
             if "is:" in temperature_i:
                 temperature_i = float(temperature_i.split(" ")[2])
                 time_i += 1
             else:
                 continue
             
             # calculate the current temperature based on the current time
             for time_bin in range(len(timevec)):
                 if time_i > timevec[time_bin]:
                     set_temp = tempvec[time_bin]
                     

             # controller!!! BANG BANG!
             if temperature_i > set_temp:
                 #THEN TURN THE RELAY OFF
                 ser.write(b'2')
                 relayon = False
             else:
                 # make sure the RELAY IS ON AND CONTINUE
                 if relayon == False:
                     ser.write(b'1')
                     relayon = True

             temp_vec.append(temperature_i)             
             counter_vec.append(counter1)
             data_file = open(output_path, "w+")
             data_file.write(str(temperature_i), time_i)
             data_file.write("\n")

             sleep(.1) #delay for 10th of a second







class PhageBoxPCR():
    """
    The PhageBoxPCR class regulates the backend processes for regulating
    the PCR module for the PhageBox. Each method contains a descriptive 
    doc string, and if necessary, also contains information regarding both
    the input and output datastructures. 
    """
    
    def __init__(self, inputfile):
        self.configFilePath = str(inputfile)
   
    def setConfigPath(self, inputfilepath):
        """
        This method is used for setting the file path 
        for the config file. This will allow other methods
        to find the correct location for the config file.
        """
        self.configFilePath = str(inputfilepath)
        
    def prepareTempVec(self):  
        """
        This function takes in a config file path, parses the
        file  and returns a data structure that can thereafter
        be used for running PCR on the PhageBox.
        """
        # create a path to the config file if there isn't already one. 
        if len(self.configFilePath) < 2:
            self.setConfigPath(configfile)

        # open the file and parse line by line
        configfile = open(self.configFilePath).read().split("\n")
        tempVec = [] # stores the  temp
        timeVec = [] # stores the time per temp
        cycleOn_bool = False 
        for line in configfile: 
            if len(line.strip()) > 1:
                if "#" == line[0]:
                    continue
                else:
                    if "--" == line[:2]:
                        if line[0:7] == "--CYCLE":
                            #print("\n cycle start found.. \n")
                            listelements = [i.strip() for i in line.split(",")]
                            if listelements[2] == "loops": # TODO allow for time
                                cyclecount = int(listelements[1])
                                cycleOn_bool = True
                                cycle_temps = [] # initialize vec storing temps
                                cycle_times = [] # init vec for storing times
                        elif line[0:10] == "--ENDCYCLE":
                            #print("\n cycle end found.. \n")
                            for tempcycle_i in range(cyclecount):
                                for tempTime_i in range(len(cycle_temps)):
                                    tempVec.append(cycle_temps[tempTime_i])
                                    timeVec.append(cycle_times[tempTime_i])
                            cycleOn_bool = False
                        else:
                            print(""" WARNING: Ensure the config contains the 
                                  correct formatting. """)
                    else:
                        temperature_i = float(line.split(",")[0])
                        time_i = float(line.split(",")[1])
                        if cycleOn_bool == True:
                            cycle_temps.append(temperature_i)
                            cycle_times.append(time_i)
                            continue

                        else:
                            tempVec.append(temperature_i)
                            timeVec.append(time_i)
        return tempVec, timeVec
       
        def bangbang_ctrl(self, output_path):
            """ 
            The bangbang_ctrl method is used to communicate with the arduino,
            and the primary goal is to regulate the temperature according the 
            config file.
            """
            tempoout_file = open(output_path, "w+")
            ser = serial.Serial('/dev/tty.usbmodem141101', 9600)          

            #####
            # TODO: old code! Try to use this for listening to the arduino 
            #       serial port. 
            #####
            temp_vec = [] # stores all of the temperatures
            counter_vec = []
            counter1 = 0
            while True:
                 counter1 += 1
                 print(ser.readline()) # Read the newest output from the Arduino
                 temperature_i = str(ser.readline())
                 if "is:" in temperature_i:
                     temperature_i = float(temperature_i.split(" ")[2])
                 else:
                     continue
                 temp_vec.append(temperature_i)
                 counter_vec.append(counter1)
                 sleep(.1) # Delay for one tenth of a second
                 data_file = open(output_path, "w+")
                 data_file.write(str(temperature_i))
                 data_file.write("\n")


def main():
    # testing PCR module
    pcr_object = PhageBoxPCR("tempconfig.py")
    tempvec, timevec = pcr_object.prepareTempVec()
    global tempvec2
    timevec2 = [ sum(timevec[:i]) for i in range(len(timevec)) ]
    tempvec2 = []
    for temp_index in range(len(tempvec)): 
        for time_i in range(int(timevec[temp_index])): # TODO this is a hack..
            tempvec2.append(tempvec[temp_index])
    tempvec3 = [ tempvec2[i] + random.randint(-10,10) for i in range(len(tempvec2)) ] 

    #####
    # Controlling the temperature
    #####
    #ard = arduino_controller()
    #ard.bangbang(tempvec2, range(len(tempvec2)), 's.txt')
 

    #####
    # Figures
    #####
    global ax_array
    pcr_fig, ax_array = plt.subplots()
    print(ax_array, type(ax_array))
    ax_array.plot(range(len(tempvec2)), tempvec2) 
    #plt.plot(range(len(tempvec3)), tempvec3)
    ax_array.set_title("Temperature Regulation of the PhageBox", size=15)
    ax_array.set_ylabel("Temperature (Celsius)")
    ax_array.set_xlabel("Time (minutes)") 
    
    ani = animation.FuncAnimation(pcr_fig, animate, interval=1000)
    plt.show()    

if __name__ == "__main__":
    main()

