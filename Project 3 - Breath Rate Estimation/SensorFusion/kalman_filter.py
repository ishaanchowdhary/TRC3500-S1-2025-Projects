'''
Written by: Ishaan Guha Chowdhary (33115303)
Last edited: 17/05/2025

Class definition for Breath Rate Kalman Filter
'''

import numpy as np

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
