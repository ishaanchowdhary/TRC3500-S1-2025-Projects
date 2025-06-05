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
normal_data = np.array([18.17, 20.42, 21.54, 20.42, 19.83, 19.30, 19.97, 19.97, 20.06, 19.85, 19.73, 19.52])
talk_data = np.array([17.50, 13.02, 10.23, 8.80, 7.96, 7.71, 7.90, 8.36, 8.83, 9.35, 9.58, 10.00])
walk_data = np.array([15.88, 17.55, 18.73, 20.00, 20.53, 20.70, 20.13, 19.16, 18.57, 17.91, 18.05, 18.14])
run_data = np.array([14.19, 16.19, 17.95, 18.85, 19.57, 19.12, 18.07, 17.18, 16.44, 15.71, 16.96, 17.77])

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