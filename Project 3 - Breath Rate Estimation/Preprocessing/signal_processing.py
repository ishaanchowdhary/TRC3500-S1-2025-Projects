'''
Written by: Ishaan Guha Chowdhary (33115303)
Last edited: 29/05/2025

Functions to calculate Breath Rates from sensors, including Sphygmomanometer, Strain sensor and Thermistor.
'''

import numpy as np
from scipy.signal import firwin, lfilter
import matplotlib.pyplot as plt


# Calculate Live Breath Rate

# Constants
FS = 10  # Sampling frequency in Hz (1 every 100ms)
CUTOFF = 3  # Low-pass filter cutoff frequency in Hz
FILTER_ORDER = 30  # FIR filter order
WINDOW_SIZE = 30  # Bigger window for smoother slope estimate
HYSTERESIS = 0.0005  # Smaller hysteresis for smoother signals
BREATH_HISTORY_SIZE = 5  # Number of breaths to average

# 1. Low-pass FIR filter NOT USED
def lowpass_filter(signal, fs, cutoff, order):
    fir_coeff = firwin(order + 1, cutoff / (fs / 2))
    return lfilter(fir_coeff, [1.0], signal)

# 2. Gradient estimation via linear regression
def compute_gradient(window):
    x = np.arange(len(window))
    y = np.array(window)
    A = np.vstack([x, np.ones(len(x))]).T
    slope, _ = np.linalg.lstsq(A, y, rcond=None)[0]
    return slope

# 3. Detect breaths by rising slope over hysteresis threshold
def detect_breaths(signal, fs, window_size, hysteresis):
    breath_timestamps = []
    state = "waiting_for_rise"

    for i in range(window_size, len(signal)):
        window = signal[i - window_size:i]
        gradient = compute_gradient(window)

        if state == "waiting_for_rise" and gradient > hysteresis:
            breath_timestamps.append(i / fs)
            state = "waiting_for_fall"
        elif state == "waiting_for_fall" and gradient < -hysteresis:
            state = "waiting_for_rise"

    return breath_timestamps

# 4. Calculate weighted average breath rate
def calculate_breath_rate(breath_times, history_size):
    if len(breath_times) < 2:
        return 0
    intervals = np.diff(breath_times)[-history_size:]
    if len(intervals) == 0:
        return 0
    weights = np.linspace(1, 2, len(intervals))
    weighted_avg = np.average(intervals, weights=weights)
    return 60 / weighted_avg  # BPM

# 5. Full pipeline
def process_breath_signal(raw_signal):
    #filtered = lowpass_filter(raw_signal, FS, CUTOFF, FILTER_ORDER)
    breaths = detect_breaths(raw_signal, FS, WINDOW_SIZE, HYSTERESIS)
    rate = calculate_breath_rate(breaths, BREATH_HISTORY_SIZE)
    return rate, breaths