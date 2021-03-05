from time import sleep
import serial
import matplotlib.pyplot as plt
import numpy, sys


ser = serial.Serial('/dev/cu.usbserial-1440', 115200) # Establish the connection
counter = 32 # Below 32 everything in ASCII is gibberish

def help():
    """
    Print a help message. 
    """
    print("""
          +++++++++ temperature script +++++++++++
          How to use this script:
          
          (1) To make a data file
              python PlotTemps.py

          (2) To plot a data file
              python PlotTemps.py <data_file path>
          """
    )

def plot_data(file_path):
    """
    This function takes in a datafile as input, plots the data, and 
    returns a scatterplot of the data. 
    """
    file_lines = open(file_path).readlines()
    data_array = []
    for data_point in file_lines:
        data_array.append(float(data_point))
    # plot the data
    plt.scatter(range(len(data_array)), data_array, color='orange')
    plt.title("Kamthal Temperature Dynamics", size=10)
    plt.ylabel("Temperature (Celsius)")
    plt.xlabel("Time (Seconds)")
    plt.show()

def record_temperatures():
    """
    This function causes python to listen to the right serial port for the 
    arduino connected to the temperature sensor. This data is then
    appended into a data file.
    """
    temp_vec = [] # stores all of the temperatures
    counter_vec = []
    counter1 = 0
    while True:
         counter1 += 1
         print(ser.readline()) # Read the newest output from the Arduino
         temperature_i = str(ser.readline())
         if "is:" in temperature_i:
             temperature_i = float(temperature_i.split(" ")[2].rstrip("\\r\\n'"))
         else:
             continue
         temp_vec.append(temperature_i)
         counter_vec.append(counter1)
         sleep(.1) # Delay for one tenth of a second
         data_file = open("data_file", "a")
         data_file.write(str(temperature_i))
         data_file.write("\n")
    #    update_line(hl, temperature_i)
         if False:
             plt.scatter(counter_vec, temp_vec)
             plt.show()
             sleep()

def main():
    if len(sys.argv) == 1:
        record_temperatures()
    elif len(sys.argv) == 2:
        plot_data(sys.argv[1])
    else:
        print("you're including too many args..")
        help()

if __name__ == "__main__":
    main()
