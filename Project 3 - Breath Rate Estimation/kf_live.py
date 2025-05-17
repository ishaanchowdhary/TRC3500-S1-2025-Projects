'''
Written by: Ishaan Guha Chowdhary (33115303)
Last edited: 17/05/2025

Method:
1. Read data from the sensors over Serial
2. Preprocess data into breath rate estimates (from thermistor & rubber)
3. Feed estimates into the Kalman filter in real time
4. Plot or log the result (TBD)
'''

import serial
import time
import numpy as np
from collections import deque
import matplotlib.pyplot as plt

# Kalman filter class (re-use from previous answer)
from kalman_filter import BreathRateKalmanFilter  # if saved in a separate file

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

def detect_breath_rate(signal, timestamps, last_peak):
    # Basic peak detection: detect when signal crosses threshold from below
    if len(signal) < 3:
        return None, last_peak

    # Smooth signal
    smoothed = np.convolve(signal, np.ones(5)/5, mode='valid')
    threshold = np.mean(smoothed) + 0.5 * np.std(smoothed)

    if signal[-2] < threshold <= signal[-1]:  # rising edge detected
        now = timestamps[-1]
        if last_peak is not None:
            interval = now - last_peak
            bpm = 60.0 / interval if interval > 1 else None
        else:
            bpm = None
        return bpm, now
    return None, last_peak

# Main loop
with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
    print("Listening on", SERIAL_PORT)
    try:
        while True:
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

            br_temp, last_peak_temp = detect_breath_rate(temp_data, time_data, last_peak_temp)
            br_rubber, last_peak_rubber = detect_breath_rate(rubber_data, time_data, last_peak_rubber)

            # Use most recent valid estimate or fallback
            est_temp = br_temp if br_temp else kf.x[0, 0]
            est_rubber = br_rubber if br_rubber else kf.x[0, 0]

            z = np.array([est_temp, est_rubber])
            fused_bpm = kf.update(z)

            print(f"Temp BPM: {br_temp}, Rubber BPM: {br_rubber}, Fused BPM: {fused_bpm:.2f}")

            time.sleep(DT) # Remove if not needed

    except KeyboardInterrupt:
        print("Terminating Program")