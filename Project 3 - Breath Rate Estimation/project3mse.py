# File Name: project3mse.py
# Author: Emanuel Risso
# ID: 33123225
# Created: 2025/06/05
# Last Modified: 2025/06/05
# Python v. 3.13.2

''' Import Modules '''

import numpy as np

''' Format Data As Arrays '''

# Set the ground truth and arrays for each test condition
ground_truth = 19.00
normal_data = np.array([20.42, 19.83, 19.30, 19.97, 19.97, 20.06, 19.85, 19.73, 19.52, 19.34, 19.75, 19.00, 18.42])
talk_data = np.array([20.38, 20.29, 20.11, 19.90, 19.63, 19.55, 19.46, 19.35, 19.48, 19.55, 19.99, 20.44, 20.71])
walk_data = np.array([19.66, 20.96, 21.59, 22.06, 21.52, 21.33, 20.98, 20.18, 20.07, 19.99, 20.20, 19.54, 19.02])
run_data = np.array([16.20, 19.93, 21.61, 21.13, 19.67, 18.79, 18.38, 19.01, 18.59, 18.81, 18.90, 18.93, 17.74])

''' Find the Mean Squared Error '''

# Calculate the mean squared errors
normal_mean_squared_error = np.mean(np.square(ground_truth - normal_data))
talk_mean_squared_error = np.mean(np.square(ground_truth - talk_data))
walk_mean_squared_error = np.mean(np.square(ground_truth - walk_data))
run_mean_squared_error = np.mean(np.square(ground_truth - run_data))

# Print the mean squared errors
print(f'Normal MSE: {normal_mean_squared_error:.4f}')
print(f'Talk MSE: {talk_mean_squared_error:.4f}')
print(f'Walk MSE: {walk_mean_squared_error:.4f}')
print(f'Run MSE: {run_mean_squared_error:.4f}')