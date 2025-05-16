'''
Written by: Ishaan Guha Chowdhary (33115303)
Last edited: 17/05/2025
'''

import numpy as np
import matplotlib.pyplot as plt

class BreathRateKalmanFilter:
    '''
    Kalman Filter for measuring breath rate from two sources (thermistor and conductive rubber)
    '''
    def __init__(self, dt, process_var=0.01, sensor_vars=(0.1, 0.1)):
        # Time step
        self.dt = dt

        # Initial state [breath rate, breath rate derivative]
        self.x = np.array([[12.0],  # Initial breath rate (e.g., 12 BPM) - To change to sphygmamometer reading ?
                           [0.0]])  # Initial change rate

        # Initial uncertainty
        self.P = np.eye(2)

        # State transition matrix
        self.F = np.array([[1, dt],
                           [0, 1]])

        # Process noise covariance (Q)
        q = process_var
        self.Q = q * np.array([[dt**4/4, dt**3/2],
                               [dt**3/2, dt**2]])

        # Observation model (H)
        self.H = np.array([[1, 0],   # Thermistor measures rate
                           [1, 0]])  # Rubber also measures rate

        # Measurement noise covariance (R)
        r1, r2 = sensor_vars
        self.R = np.array([[r1, 0],
                           [0, r2]])

        # Identity
        self.I = np.eye(2)

    def update(self, z):
        # Prediction
        x_pred = self.F @ self.x
        P_pred = self.F @ self.P @ self.F.T + self.Q

        # Kalman Gain
        S = self.H @ P_pred @ self.H.T + self.R
        K = P_pred @ self.H.T @ np.linalg.inv(S)

        # Update state
        y = z.reshape(2, 1) - self.H @ x_pred
        self.x = x_pred + K @ y

        # Update uncertainty
        self.P = (self.I - K @ self.H) @ P_pred

        return self.x[0, 0]  # Return estimated breath rate


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
