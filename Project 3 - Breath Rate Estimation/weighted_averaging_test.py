'''
Written by: Ishaan Guha Chowdhary (33115303)
Last edited: 17/05/2025

Code for testing weighted averaging sensor fusion on simulated data
'''

import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

# Simulated example signals (you'd replace with actual data)
# Assume 60 seconds of data at 10 Hz
fs = 10  # Hz
duration = 60  # seconds
t = np.linspace(0, duration, fs * duration)

# Simulated thermistor signal: sine waves + noise
thermistor_signal = 0.5 * np.sin(2 * np.pi * t / 5) + 0.1 * np.random.randn(len(t))  # ~12 BPM

# Simulated strain signal: similar but slightly offset
strain_signal = 0.6 * np.sin(2 * np.pi * t / 5 + 0.5) + 0.1 * np.random.randn(len(t))  # ~12 BPM

# Weights for sensor reliability
weight_therm = 0.6 # Hard code this
weight_strain = 0.4 # Hard code this

# Peak Detection to Count Breaths

# Thermistor peaks (detects exhalation)
therm_peaks, _ = find_peaks(thermistor_signal, height=0.3, distance=fs*2)
therm_breaths = len(therm_peaks)
therm_bpm = therm_breaths * (60 / duration)

# Strain peaks (detects expansion)
strain_peaks, _ = find_peaks(strain_signal, height=0.3, distance=fs*2)
strain_breaths = len(strain_peaks)
strain_bpm = strain_breaths * (60 / duration)

# Weighted Averaging
fused_bpm = weight_therm * therm_bpm + weight_strain * strain_bpm

# Output Results
print(f"Thermistor BPM: {therm_bpm:.2f}")
print(f"Strain Sensor BPM: {strain_bpm:.2f}")
print(f"Fused BPM (weighted average): {fused_bpm:.2f}")

# Plot trends and results
plt.figure(figsize=(12, 5))
plt.plot(t, thermistor_signal, label='Thermistor')
plt.plot(t[therm_peaks], thermistor_signal[therm_peaks], 'ro', label='Therm Peaks')

plt.plot(t, strain_signal, label='Strain')
plt.plot(t[strain_peaks], strain_signal[strain_peaks], 'go', label='Strain Peaks')

plt.title('Breath Detection from Sensors')
plt.xlabel('Time (s)')
plt.ylabel('Signal')
plt.legend()
plt.grid(True)
plt.show()
