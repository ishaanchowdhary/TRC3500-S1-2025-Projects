'''
Written by: Ishaan Guha Chowdhary (33115303)
Last edited: 26/05/2025

Run time code for Final Submission
'''

import serial
import time
import numpy as np
from collections import deque
import matplotlib.pyplot as plt

from Preprocessing.calculate_BPM import * # Functions for calculating BPM from Sphyg, Strain and Thermistor Sensor Data
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
kf = BreathRateKalmanFilter(dt=DT, sensor_vars=(0.4**2, 0.3**2))

# Smooths Signal
def smooth_signal(signal):
    return np.convolve(signal, np.ones(5)/5, mode='valid')

# Main loop
with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
    print("Listening on port", SERIAL_PORT)
    time.sleep(5)
    try:
        while True:
            # Recieve and decode data
            line = ser.readline().decode().strip() # expecting line = 'temp_val,rubber_val' as float
            if not line:
                continue # skip invalid input
            try:
                temp_val, rubber_val = map(float, line.split(','))
            except ValueError:
                continue  # skip malformed lines

            t = time.time()
            temp_data.append(temp_val)
            rubber_data.append(rubber_val)
            time_data.append(t)

            # TODO: Calculate Breath Rate
            br_therm = calc_therm_bpm()
            br_strain = calc_strain_bpm()

            # Use most recent valid estimate or fallback
            est_temp = br_therm if br_therm else kf.x[0, 0]
            est_rubber = br_strain if br_strain else kf.x[0, 0]

            # Update Kalman Filter and record latency
            fused_bpm = kf.update(np.array([est_temp, est_rubber])) # Breaths per minute
            latency = time.time() - t # seconds

            # Print outputs
            print(f"Temp BPM: {br_therm}, Rubber BPM: {br_strain}, Fused BPM: {fused_bpm:.2f}")
            print(f"Latency: {latency:.2f} s")

            time.sleep(DT) # Remove if not needed

    except KeyboardInterrupt:
        print("Terminating Program")