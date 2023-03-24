# Phagebox Scripts

## Description

This directory contains scripts for various tasks regarding the Phagebox. For one, it contains scripts that can be used for plotting data produced by both the magnetometer and by the on-device temperature sensors.

## Directory Structure

This directory contains scripts for the following:

1. **Magnetometer testing.**
    1. `magneto_meter_testing.py` - Parsing the data from the serial port of the arduino opoerating the magnetometer.
    2. `magnetic_control_analysis.py` - Plotting of the magnetic field tests.
    3. CSV Files - measurements performed on PhageBox magnetic module.
2. **Temperature testing.**
    1. `temperature_plotter.py` - Plotting of all the figures from a temperature test csv.
    2. `temperature_analysis.ipynb` - Plotting of all temperature measurements.
3. **Temperature error.**
    1. `hysteresis_analysis.ipynb` - Plotting measurements from downloaded CSV files.
    2. CSV Files - UART and embedded measurements from different temperatures.
4. **RE PCR.**
    1. `PCRcheck.ipynb` - Notebook for checking which restriction enzymes to use.
    2. `primer_db.csv` - CSV file containing the primers.
