'''
Written by: Ishaan Guha Chowdhary (33115303)
Last edited: 30/05/2025

Run time code for Final Submission
'''

import serial
import time
import numpy as np
from collections import deque
import matplotlib.pyplot as plt

from Preprocessing.signal_processing import * # Functions for calculating BPM from Sphyg, Strain and Thermistor Sensor Data
# from Preprocessing.super_imposed_state import * # Functions for calculating super-imposed state
from SensorFusion.kalman_filter import BreathRateKalmanFilter

# Serial configuration
SERIAL_PORT = 'COM5'      # Replace with your port, e.g., '/dev/ttyUSB0' or 'COM3'
BAUD_RATE = 115200
WINDOW_SIZE = 100         # Number of samples to keep
DT = 0.2                  # Sampling interval (e.g., 5 Hz)

# Signal history
temp_data = deque(maxlen=WINDOW_SIZE)
rubber_data = deque(maxlen=WINDOW_SIZE)
time_data = deque(maxlen=WINDOW_SIZE)

# Breath interval buffer
last_peak_temp = None
last_peak_rubber = None

# Kalman filter
kf = BreathRateKalmanFilter(dt=DT, process_var=0.9, sensor_vars=(0.5, 0.5), initial_rate=0.0)

# To make live time initiate from 0
initial_ts = None

# Weights for Weighted Averaging Fusion
THERMISTOR_WEIGHT = 0.4
STRAIN_WEIGHT = 0.6

# Weighted Averaging Fusion
def weighted_average(br_therm, br_strain, weight_therm, weight_strain):
    return br_therm*weight_therm + br_strain+weight_strain

# Main loop
with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
    print("Listening on port", SERIAL_PORT)
    time.sleep(5)
    try:
        while True:
            # print('cheese')
            start_time = time.time()
            # Recieve and decode data
            line = ser.readline().decode().strip() # expecting line = 'temp_val,rubber_val,time_stamp' as float
            if not line:
                # print("chips")
                continue # skip invalid input
            try:
                temp_val, rubber_val, time_stamp = map(float, line.split(','))
            except ValueError:
                # print("crackers")
                continue  # skip malformed lines

            # Get Initial Timestamp if nonexistent
            if initial_ts == None:
                initial_ts = time_stamp
            
            time_stamp -= initial_ts
            temp_data.append(temp_val)
            rubber_data.append(rubber_val)
            time_data.append(time_stamp)

            # TODO: Calculate Breath Rate
            br_therm, _ = process_breath_signal(temp_data, window_size = 30)
            br_strain, _ = process_breath_signal(rubber_data, window_size = 25)

            # Use most recent valid estimate or fallback
            est_temp = br_therm if br_therm else kf.x[0, 0]
            est_rubber = br_strain if br_strain else kf.x[0, 0]

            # Update Kalman Filter and record latency
            fused_bpm = kf.update(np.array([est_temp, est_rubber])) # Breaths per minute
            latency = time.time() - start_time # seconds

            # Weighted Averaging Fusion for comparison
            wa_fused = weighted_average(br_therm,br_strain,THERMISTOR_WEIGHT,STRAIN_WEIGHT)
            # Print outputs
            print(f"Temp BPM: {br_therm:.2f}, Rubber BPM: {br_strain:.2f}, Fused BPM: {fused_bpm:.2f}, W_A Fused BPM: {wa_fused:.2f}")
            print(f"Latency: {latency:.2f} s")

            time.sleep(DT) # Remove if not needed

    except KeyboardInterrupt:
        print("Terminating Program")