# File Name: project_2.py
# Authors: Ishaan Chowdhary, Emanuel Risso
# Created: 25/04/2025
# Last Modified: 25/04/2025
# Python v. 3.13.2

''' File Overview '''

# This program reads live ADC values from the STM through a serial connection
# and converts them to voltage. If a HIGH signal is received, a vibration
# event is started (lasting 3 seconds). During this event, the real time and
# magnitude of all vibrations (bounces) will be printed to the terminal.

''' Module Imports '''

import serial
from datetime import datetime

''' Receive, format, and print the data from the STM ADC '''

# Set the serial connection to use the correct port and baud rate
ser = serial.Serial('COM5', 115200, timeout=1)
# Set the debounce delay (ms) to specify one event for multiple bounces
debounce_duration = 3000
# Set the initial last peak detection time to 0 (ms)
last_peak_time = 0.0
# Set the voltage threshold (V) to qualify as a HIGH signal from the STM
threshold_voltage = 3.24

# Initiate an infinite loop
while True:
    # Set the current time
    current_time = datetime.now()
    # Set the current time (ms) for logic use
    now = current_time.timestamp() * 1000
    # Format the time to print
    print_time = (current_time.strftime('%H:%M:%S:%f')[:-3])
    # Read each line from the ADC serial connection output
    data = ser.readline().decode('utf-8').strip()
    # Convert the data to float type
    adc_value = float(data)
    # Convert the ADC data to a specified voltage range
    voltage = ((adc_value / 4095) * 3.3)

    # If the current time minus the last peak time is less than 3 seconds
    if ((now - last_peak_time) < debounce_duration):
        # Exit the if elif statement
        pass
    # If the voltage reading is above the threshold
    elif voltage >= threshold_voltage:
        # Print that a vibration event has been detected
        print('-------------------------------------------------')
        print('VIBRATION EVENT DETECTED')
        print('-------------------------------------------------')
        # Set the most recent peak time  to the current time
        last_peak_time = now
    # If the voltage is HIGH in this event (lasting 3 seconds max)
    if voltage != 0:
        # Print the current time and voltage
        print(f'Time: {print_time} H:MM:SS:ms --- Voltage: {voltage:.2f} V')
