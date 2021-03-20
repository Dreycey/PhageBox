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

    def uniformTempVec(self, tempVecIn, timeVecIn):
        """
        This method works to turn the temperature vector Output
        from the prepareTempVec() function and turn it into a vector
        that spans the time of the time vector.
        """
        # The below should become a method.
        timeVecOut = [ sum(timeVecIn[:i]) for i in range(len(timeVecIn)) ]
        tempVecOut = []
        for temp_index in range(len(tempVecIn)):
            for time_i in range(int(timeVecOut[temp_index])): # TODO this is a hack..
                tempVecOut.append(tempVecIn[temp_index])

        return tempVecOut

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

def main():
    # testing PCR module
    pcr_object = PhageBoxPCR("tempconfig.py")
    tempvec, timevec = pcr_object.prepareTempVec()
    global tempvec2
    tempvec2 = pcr_object.uniformTempVec(tempvec, timevec)

    #####
    # Figures
    #####
    global ax_array
    pcr_fig, ax_array = plt.subplots()
    print(ax_array, type(ax_array))
    ax_array.plot(range(len(tempvec2)), tempvec2)
    ax_array.set_title("Temperature Regulation of the PhageBox", size=15)
    ax_array.set_ylabel("Temperature (Celsius)")
    ax_array.set_xlabel("Time (minutes)")

    ani = animation.FuncAnimation(pcr_fig, animate, interval=1000)
    plt.show()

if __name__ == "__main__":
    main()
