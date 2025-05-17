'''
Written by: Ishaan Guha Chowdhary (33115303)
Last edited: 17/05/2025

Code for testing kalman filter on simulated data
'''

import numpy as np
import matplotlib.pyplot as plt
from kalman_filter import BreathRateKalmanFilter

# Simulated example

# Input data
time = np.linspace(0, 60, 300)  # 60 seconds at ~5Hz
true_breath_rate = 12 + 2 * np.sin(0.2 * time) # For comparison

# Add noise for sensor estimates
z_thermistor = true_breath_rate + np.random.normal(0, 0.4, size=time.shape)
z_rubber     = true_breath_rate + np.random.normal(0, 0.3, size=time.shape)

# Initialise Kalman Filter
kf = BreathRateKalmanFilter(dt=time[1] - time[0], sensor_vars=(0.4**2, 0.3**2))
fused_rate = []

for z1, z2 in zip(z_thermistor, z_rubber):
    z = np.array([z1, z2])
    fused = kf.update(z)
    fused_rate.append(fused)

# Plot results
plt.figure(figsize=(10, 5))
plt.plot(time, true_breath_rate, label='True Breath Rate', color='k', linewidth=2)
plt.plot(time, z_thermistor, label='Thermistor Estimate', alpha=0.5)
plt.plot(time, z_rubber, label='Rubber Estimate', alpha=0.5)
plt.plot(time, fused_rate, label='Fused Estimate (Kalman)', color='r', linewidth=2)
plt.xlabel('Time (s)')
plt.ylabel('Breaths per Minute (BPM)')
plt.title('Kalman Filter Fusion of Breathing Rate')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
