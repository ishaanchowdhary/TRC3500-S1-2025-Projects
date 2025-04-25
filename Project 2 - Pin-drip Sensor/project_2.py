'''
Written By: Ishaan Chowdhary
Last modified: 25/04/2025
Last Modifier: Ishaan Chowdhary
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import serial

ser = serial.Serial("COM5", 115200, timeout=1)

debounce_duration = 5000000  # micro seconds
last_peak_time = 0     # initialize last peak detection time

threshold_voltage = 3.2  # Adjust this threshold based on your needs
while True:
    data = ser.readline().decode("utf-8").strip().split(",")

    adc_value = float(data[0])
    time_value = float(data[1])
    voltage = adc_value * 3.3 /4096
    # Debouncing signal
    if last_peak_time + debounce_duration > time_value:
        print(f"Time: {time_value:.2f} Voltage: {voltage:.2f}")
        pass
    # Detect Signal
    if voltage >= threshold_voltage:
        print("-------------------------------------")
        print("EVENT DETECTED")
        print("-------------------------------------")
        last_peak_time = time_value
    print(f"Time: {time_value:.2f} Voltage: {voltage:.2f}")
