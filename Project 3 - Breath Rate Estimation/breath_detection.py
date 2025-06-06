'''
Written by: Emille Enriquez
Last edited: 29/05/2025

Calculates Breath Rate from recorded csv file.
'''

import numpy as np
from scipy.signal import firwin, lfilter
import matplotlib.pyplot as plt

# Constants
FS = 10  # Sampling frequency in Hz (1 every 100ms)
CUTOFF = 3  # Low-pass filter cutoff frequency in Hz
FILTER_ORDER = 30  # FIR filter order
WINDOW_SIZE = 30  # Bigger window for smoother slope estimate
HYSTERESIS = 0.0005  # Smaller hysteresis for smoother signals
BREATH_HISTORY_SIZE = 5  # Number of breaths to average

FILENAME = 'data/sensor_log_GRAPH_ONLY.csv'

def smooth_signal(signal):
    return np.convolve(signal, np.ones(5)/5, mode='valid')

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
def process_breath_signal(signal):
    #filtered = lowpass_filter(signal, FS, CUTOFF, FILTER_ORDER) # Makes it worse
    signal = smooth_signal(signal)
    breaths = detect_breaths(signal, FS, WINDOW_SIZE, HYSTERESIS)
    rate = calculate_breath_rate(breaths, BREATH_HISTORY_SIZE)
    return rate, breaths

# 6. Simulate test signal
if __name__ == "__main__":
    t = np.linspace(0, FS*200/100, 200)
    # frequency = 0.25  # 15 BPM
    # amplitude = 1.0
    # clean_breaths = amplitude * np.sin(2 * np.pi * frequency * t)
    # noise = 0.05 * np.random.randn(len(t))
    # signal = clean_breaths + noise
    # import signal
    
    data = np.loadtxt(FILENAME, delimiter=',')
    signal = data[200:400,0]
    # Run processing
    rate, breath_times = process_breath_signal(signal)
    print(f"Estimated Breath Rate: {rate:.2f} BPM")
    print(f"Detected breaths: {len(breath_times)}")
    print(breath_times)
    # Plotting
    plt.figure(figsize=(12, 4))
    plt.plot(t, signal, label='Raw Signal')
    plt.plot(smooth_signal(t), smooth_signal(signal), label='Filtered Signal')
    plt.scatter(breath_times, [signal[int(bt * FS)] for bt in breath_times], color='red', label='Breaths')
    plt.xlabel("Time (s)")
    plt.ylabel("Signal")
    plt.title(f"Estimated Breath Rate: {rate:.2f} BPM")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
