'''
Written by: Emille Enriquez
Last edited: 29/05/2025

Calculates Breath Rate from recorded csv file.
'''

import numpy as np
from scipy.signal import firwin, lfilter
import matplotlib.pyplot as plt
from SensorFusion.kalman_filter import BreathRateKalmanFilter
# Constants
FS = 10  # Sampling frequency in Hz (1 every 100ms)
CUTOFF = 3  # Low-pass filter cutoff frequency in Hz
FILTER_ORDER = 30  # FIR filter order
WINDOW_SIZE = 30  # Bigger window for smoother slope estimate
HYSTERESIS = 0.0005  # Smaller hysteresis for smoother signals
BREATH_HISTORY_SIZE = 5  # Number of breaths to average

FILENAME = 'data/sensor_log_talk.csv'

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


if __name__ == "__main__":
    data = np.loadtxt(FILENAME, delimiter=',')
    thermo = data[:, 0]
    rubber = data[:, 1] # 200:400
    time = data[200:400, 2] / 1000
    time_start = time[0]

    # Simulated time axis
    #t = np.arange(len(thermo)) / FS

    # Init Kalman filter
    kf = BreathRateKalmanFilter(dt=0.2, process_var=0.9, sensor_vars=(0.5, 0.5), initial_rate=0.0)

    # Weighted Averaging Fusion
    # Weights for sensor reliability
    weight_therm = 0.4 # Hard code this
    weight_strain = 0.6 # Hard code this

    fused_rates = []
    times = []

    # Simulate live reading
    print("Simulating live readings...\n")
    for i in range(0, len(thermo) - 49, 50):  # step by 2 for dt = 0.2s
        br_therm, _ = process_breath_signal(thermo[:i+50])
        br_strain, _ = process_breath_signal(rubber[:i+50])
        #print(len(thermo[:i+50]))
        z = np.array([br_therm, br_strain])
        fused = kf.update(z)

        fused_rates.append(fused)
        times.append(i / FS)
        fused_weighted = weight_therm * br_therm + weight_strain * br_strain
        print(f"Time {i/FS:.1f}s | Sensor1: {br_therm:.3f} | Sensor2: {br_strain:.3f} | Kalman Fused: {fused:.2f} BPM | W_A Fused: {fused_weighted:.2f}")
        
        # Simulate live delay (optional for real-time feel)
        # time.sleep(0.2)  # Uncomment this line if running live
