#!/usr/local/bin/python3
# in-house packages
import phagebox_modules.control_modules as ctrl
# std-packages
from time import sleep
import serial
import numpy, sys
import time

class arduino_controller():
    """
    This class contains methods for controlling the arduino.
    """

    def __init__(self, port_in):
        """
        initialization for the class for controlling the arduino
        """
        self.ser = serial.Serial(port_in, 9600)
        sleep(2)
        self.backlightOn = False
        self.magnetOn = False

    def __del__(self):
        # body of destructor
        print("arduino destructor being called")
        self.turnEverythingOff()

    def turnEverythingOff(self):
        """turns all of the components off"""
        ser = self.ser
        ser.write(bytes("1", 'ascii')) # turn lights off
        ser.write(bytes("3", 'ascii')) # turn lights off
        ser.write(bytes("8", 'ascii')) # turn lights off
        ser.write(bytes("6", 'ascii')) # turn magnets off
        offstring2 = bytes("3", 'ascii')
        offstring2 = bytes("1", 'ascii')

    def toggleBacklight(self):
        """turns the backlight on and off"""
        ser = self.ser
        print("light toggle is being called")
        if (self.backlightOn):
            ser.write(bytes("8", 'ascii'))
            self.backlightOn = False
        else:
            ser.write(bytes("7", 'ascii'))
            self.backlightOn = True

    def toggleMagnet(self):
        """turns the magnet on and off"""
        ser = self.ser
        print("magnet toggle is being called")
        if (self.magnetOn):
            ser.write(bytes("6", 'ascii'))
            self.magnetOn = False
        else:
            ser.write(bytes("5", 'ascii'))
            self.magnetOn = True

    def setConstantTemp(self, tempSet, outpath):
        """sets a constant temperature for the chip"""
        print("Starting to set a constant temp")
        ser = self.ser
        # What is the temp supposed to be
        set_temp = float(tempSet)

        counter1 = 0
        time_i = 0

        # on and off strings for the relays
        onstring1 = bytes("2", 'ascii')
        offstring1 = bytes("1", 'ascii')
        onstring2 = bytes("4", 'ascii')
        offstring2 = bytes("3", 'ascii')

        relayon = True # start heating the chip.
        def turnRelaysOn():
            """ turns both relays on """
            ser.write(onstring1)
            ser.write(onstring2)
            sleep(2) # let it turn change relays

        def turnRelaysOff():
            """ turns both relays off """
            ser.write(offstring1)
            ser.write(offstring2)
            sleep(2) # let it turn change relays

        tempArray = [0,0,0]
        while True:
            # print(ser.readline()) # Read the newest output from the Arduino
            temperature_i = str(ser.readline())
            print(temperature_i)
            ###
            # Save temp in diff vectors
            ###
            if 'TEC_1:' in temperature_i:
                temperature_i = float(temperature_i.split(" ")[1].rstrip("\\r\\n'"))
                tempArray[0] = temperature_i
                print(f'TEC 1 is {temperature_i}')
            elif 'TEC_2:' in temperature_i:
                temperature_i = float(temperature_i.split(" ")[1].rstrip("\\r\\n'"))
                tempArray[1] = temperature_i
                print(f'TEC 2 is {temperature_i}')
            elif 'TEC_MET' in temperature_i:
                temperature_i = float(temperature_i.split(" ")[1].rstrip("\\r\\n'"))
                tempArray[2] = temperature_i
                print(f'TEC MET is {temperature_i}')
            else:
                print('The temperature parse string {temperature} does not contain:')
                print('TEC_1, TEC_2, or TEC_MET so the arduino code needs updated')
                continue
                #exit(1)

            avg_temp = float(numpy.mean(tempArray))
            #print(f"The average is: {avg_temp}")

            if counter1 > 3:
                 # controller!!! BANG BANG!
                 if avg_temp > set_temp:
                    # THEN TURN THE RELAYS OFF
                    turnRelaysOff()
                    sleep(2)
                    relayon = False
                    print(f"Is the relay on: {relayon}")
                 else:
                    # make sure the RELAY IS ON AND CONTINUE
                    turnRelaysOn()
                    sleep(2)
                    relayon = True
                    print(f"Is the relay on: {relayon}")

            # keep track of the temps
            #temp_vec.append(avg_temp)
            #counter_vec.append(counter1)
            counter1 += 1 # increment loop counter
            sleep(.1) #delay for 10th of a second

            data_file = open(outpath, "a+")
            data_file.write(str(counter1) + "," + str(tempArray[0]) + "," +
                            str(tempArray[1]) + "," + str(tempArray[2]))
            data_file.write("\n")

    def bangbang(self, tempvec, timevec, outpath, onstring, offstring, parse_cmd, two=False):
        """
        This method impliments the bang bang controller for controlling the
        temperature of the peltier modules conected to the arduino.
        """
        print("Starting the bangbang controller")
        ser = self.ser
        temp_vec = [] # stores all of the temperatures
        counter_vec = []
        counter1 = 0
        time_i = 0

        onstring = bytes(onstring, 'ascii')
        offstring = bytes(offstring, 'ascii')
        relayon = True
        ser.write(onstring)
        sleep(2)
        tempArray = [0,0,0]
        while True:
            counter1 += 1

            if (two == False):
                temperature_i = str(ser.readline())
                ###
                # Save temp in diff vectors
                ###
                if 'TEC_1:' in temperature_i:
                    temperature_j = float(temperature_i.split(" ")[1].rstrip("\\r\\n'"))
                    tempArray[0] = temperature_j
                    print(f'TEC 1 is {temperature_j}')
                elif 'TEC_2:' in temperature_i:
                    temperature_j = float(temperature_i.split(" ")[1].rstrip("\\r\\n'"))
                    tempArray[1] = temperature_j
                    print(f'TEC 2 is {temperature_j}')
                elif 'TEC_MET' in temperature_i:
                    temperature_j = float(temperature_i.split(" ")[1].rstrip("\\r\\n'"))
                    tempArray[2] = temperature_j
                    print(f'TEC MET is {temperature_j}')
                else:
                    print('The temperature parse string {temperature} does not contain:')
                    print('TEC_1, TEC_2, or TEC_MET so the arduino code needs updated')
                    continue

                # parse the string
                if parse_cmd in temperature_i:
                    temperature_i = float(temperature_i.split(" ")[1].rstrip("\\r\\n'"))
                    print(temperature_i)
                    time_i += 1
                else:
                    continue
            else:
                openedfile = open(outpath, "r").readlines()
                if len(openedfile) == 0:
                    continue
                else:
                    temperature_list = openedfile[-1].strip("\n").split(",")
                    time_i += 1
                    #time_i = float(temperature_list[0])
                    if (parse_cmd == "TEC_1:"):
                        temperature_i = float(temperature_list[1])
                    elif (parse_cmd == "TEC_2:"):
                        temperature_i = float(temperature_list[2])
                    elif (parse_cmd == "TEC_MET:"):
                        temperature_i = float(temperature_list[3])
                    else:
                        print("The parse command is not correct")


            # calculate the current temperature based on the current time
            currenttime_index = time_i
            set_temp = tempvec[currenttime_index]

            # controller!!! BANG BANG!
            print(f"temp i : {temperature_i}")
            if temperature_i > set_temp:
                #THEN TURN THE RELAY OFF
                ser.write(offstring)
                sleep(2)
                relayon = False
                print(f"Is the relay on: {relayon}")
            else:
                # make sure the RELAY IS ON AND CONTINUE
                #if relayon == False:
                ser.write(onstring)
                sleep(2)
                print(f"Is the relay on: {relayon}")
                relayon = True

            if (two == False):
                temp_vec.append(temperature_i)
                counter_vec.append(counter1)
                data_file = open(outpath, "a+")
                data_file.write(str(time_i) + "," + str(tempArray[0]) + "," +
                                str(tempArray[1]) + "," + str(tempArray[2]))
                data_file.write("\n")

            sleep(.1) #delay for 10th of a second

def main():
    #####
    # Controlling the temperature
    #####

    if int(sys.argv[1]) == 1:
        print("Using only 1 relay")
        # importing the config file into the ctrl module
        pcr_object = ctrl.PhageBoxPCR("tempconfig.py")
        tempvec, timevec = pcr_object.prepareTempVec()
        # modifying the output vec from the ctrl package
        tempvec2 = []
        for temp_index in range(len(tempvec)):
            for time_i in range(int(timevec[temp_index])): # TODO this is a hack..
                tempvec2.append(tempvec[temp_index])
        # controlling the arduino
        ard = arduino_controller('/dev/cu.usbserial-1440')
        ard.bangbang(tempvec2, range(len(tempvec2)), 's2.txt', '2', '1','TEC_1:')

    elif int(sys.argv[1]) == 2:
        # importing the config file into the ctrl module
        pcr_object = ctrl.PhageBoxPCR("tempconfig.py")
        tempvec, timevec = pcr_object.prepareTempVec()
        # modifying the output vec from the ctrl package
        tempvec2 = []
        for temp_index in range(len(tempvec)):
            for time_i in range(int(timevec[temp_index])): # TODO this is a
                tempvec2.append(tempvec[temp_index])
        # controlling the arduino
        ard = arduino_controller('/dev/cu.usbserial-1440')
        ard.bangbang(tempvec2, range(len(tempvec2)), 's1.txt', '5', '6', 'TEC_2:')

if __name__ == "__main__":
    main()
