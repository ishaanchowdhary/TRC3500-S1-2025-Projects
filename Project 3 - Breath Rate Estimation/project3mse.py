# File Name: project3mse.py
# Author: Emanuel Risso
# ID: 33123225
# Created: 2025/06/05
# Last Modified: 2025/06/06
# Python v. 3.13.2

''' Import Modules '''

import numpy as np

''' Format Data As Arrays '''

# Set the ground truth and arrays for each test condition
ground_truth = 19.00
normal_data = np.array([20.42, 19.83, 19.30, 19.97, 19.97, 20.06, 19.85, 19.73, 19.52, 19.34, 19.75, 19.00, 18.42])
talk_data = np.array([20.38, 20.29, 20.11, 19.90, 19.63, 19.55, 19.46, 19.35, 19.48, 19.55, 19.99, 20.44, 20.71])
walk_data = np.array([20.00, 20.53, 20.70, 20.13, 19.16, 18.57, 17.91, 18.05, 18.14])
run_data = np.array([16.20, 19.93, 21.61, 21.13, 19.67, 18.79, 18.38, 19.01, 18.59, 18.81, 18.90, 18.93, 17.74])
single_normal_data = np.array([19.19, 18.868, 18.848, 19.376, 18.538, 19.108, 18.73, 19.715, 18.349, 19.272, 18.75, 19.088, 19.088])
single_talk_data = np.array([19.31, 20.16, 19.42, 19.52, 18.75, 19.65, 19.44, 19.36, 20.13, 19.42, 20.04, 21.20, 20.91])
single_walk_data = np.array([18.97, 17.77, 18.71, 18.71, 18.61, 18.77, 18.26, 18.37, 18.07])
single_run_data = np.array([21.01, 20.76, 19.59, 15.53, 14.68, 15.44, 16.56, 18.73, 15.82, 16.30, 17.32, 18.54, 16.25])


''' Find the Mean Squared Error '''

# Calculate the mean squared errors
normal_mean_squared_error = np.mean(np.square(ground_truth - normal_data))
talk_mean_squared_error = np.mean(np.square(ground_truth - talk_data))
walk_mean_squared_error = np.mean(np.square(ground_truth - walk_data))
run_mean_squared_error = np.mean(np.square(ground_truth - run_data))
single_normal_mean_squared_error = np.mean(np.square(ground_truth - single_normal_data))
single_talk_mean_squared_error = np.mean(np.square(ground_truth - single_talk_data))
single_walk_mean_squared_error = np.mean(np.square(ground_truth - single_walk_data))
single_run_mean_squared_error = np.mean(np.square(ground_truth - single_run_data))

# Print the mean squared errors
print(f'Normal MSE: {normal_mean_squared_error:.4f}')
print(f'Talk MSE: {talk_mean_squared_error:.4f}')
print(f'Walk MSE: {walk_mean_squared_error:.4f}')
print(f'Run MSE: {run_mean_squared_error:.4f}')
print(f'Strain Normal MSE: {single_normal_mean_squared_error:.4f}')
print(f'Strain Talk MSE: {single_talk_mean_squared_error:.4f}')
print(f'Strain Walk MSE: {single_walk_mean_squared_error:.4f}')
print(f'Strain Run MSE: {single_run_mean_squared_error:.4f}')