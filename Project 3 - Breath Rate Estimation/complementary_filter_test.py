'''
Written by: Ishaan Guha Chowdhary (33115303)
Last edited: 17/05/2025

Code for testing complementary filter on simulated data
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks

# Simulated time and signals
fs = 10  # Sampling frequency (Hz)
duration = 60  # seconds
t = np.linspace(0, duration, fs * duration)

# Simulated input signals (replace with your real sensor data)
thermistor_signal = 0.5 * np.sin(2 * np.pi * t / 5) + 0.15 * np.random.randn(len(t))
strain_signal = 0.6 * np.sin(2 * np.pi * t / 5 + 0.3) + 0.1 * np.random.randn(len(t))

# Define Filters
def low_pass(data, cutoff=0.3, fs=10, order=2):
    b, a = butter(order, cutoff / (0.5 * fs), btype='low')
    return filtfilt(b, a, data)

def high_pass(data, cutoff=0.3, fs=10, order=2):
    b, a = butter(order, cutoff / (0.5 * fs), btype='high')
    return filtfilt(b, a, data)

# Apply Complementary Filter
alpha = 0.6  # Weight for low-pass (strain), 1-alpha for high-pass (thermistor)

strain_low = low_pass(strain_signal, cutoff=0.3, fs=fs)
therm_high = high_pass(thermistor_signal, cutoff=0.3, fs=fs)

fused_signal = alpha * strain_low + (1 - alpha) * therm_high

# Peak Detection on Fused Signal
peaks, _ = find_peaks(fused_signal, height=0.3, distance=fs*2)
breath_rate_bpm = len(peaks) * (60 / duration)

# Output
print(f"Estimated Breath Rate: {breath_rate_bpm:.2f} BPM")

# Plot
plt.figure(figsize=(12, 6))
plt.plot(t, thermistor_signal, label="Thermistor", alpha=0.5)
plt.plot(t, strain_signal, label="Strain Sensor", alpha=0.5)
plt.plot(t, fused_signal, label="Fused Signal (Complementary Filter)", linewidth=2)
plt.plot(t[peaks], fused_signal[peaks], 'ro', label="Detected Breaths")
plt.title("Breath Signal Fusion with Complementary Filter")
plt.xlabel("Time (s)")
plt.ylabel("Signal")
plt.legend()
plt.grid(True)
plt.show()
