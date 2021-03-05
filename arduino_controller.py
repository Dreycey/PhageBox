#!/usr/local/bin/python3
# in-house packages
import control_modules as ctrl
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
                                                                                
    def bangbang(self, tempvec, timevec, outpath, onstring, offstring, parse_cmd):                              
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
        while True:                            
             counter1 += 1                                                      
#             print(ser.readline()) # Read the newest output from the Arduino    
             temperature_i = str(ser.readline())                                
             print(temperature_i)                                                                   
             # parse the string                                                 
             if parse_cmd in temperature_i:        
                 temperature_i = float(temperature_i.split(" ")[1].rstrip("\\r\\n'"))             
                 print(temperature_i)
                 time_i += 1                                                    
             else:                                                              
                 continue                                                       
                                                                                
             # calculate the current temperature based on the current time
             currenttime_index = time_i 
             set_temp = tempvec[currenttime_index]                              
                                                                                
             # controller!!! BANG BANG!                                         
             if temperature_i > set_temp:                                       
                 #THEN TURN THE RELAY OFF                                       
                 ser.write(offstring)
                 sleep(2)                                                
                 relayon = False                                                
             else:                                                              
                 # make sure the RELAY IS ON AND CONTINUE                       
                 if relayon == False:                                           
                     ser.write(onstring) 
                     sleep(2)                                           
                     relayon = True                                             
                                                                                
             temp_vec.append(temperature_i)                                     
             counter_vec.append(counter1)                                       
             data_file = open(outpath, "a+")                                
             data_file.write(str(temperature_i) + "," + str(time_i))                        
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
        ard.bangbang(tempvec2, range(len(tempvec2)), 's2.txt', '1', '2','TEC_1:')
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
