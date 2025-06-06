# File Name: project3jnd.py
# Author: Emanuel Risso
# ID: 33123225
# Created: 2025/06/06
# Last Modified: 2025/06/06
# Python v. 3.13.2

''' Import Modules '''

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

''' Plot the measured data '''

# Set the data
target_BPM = 18
threshold = 50
breath_change = np.array([0.5, 0.75, 1.0, 1.5, 2.0])
breath_rates = np.array([20, 20, 60, 80, 100])

# Plot the data
plt.scatter(breath_change, breath_rates, c='k', marker='x', label='Measured Data')

''' Fit the logistic curve '''

# Define a function for the logistic equation
def logistic_func(x, k, x0):
    return 100 / (1 + np.exp(-k * (x - x0)))
# Set the input and output values
X = breath_change
Y = breath_rates
# Fit the logistic model and the initial guesses for parameters
params, _ = curve_fit(logistic_func, X, Y, p0=[10, 1])
# Set the intercept and slope as the parameters
k, x0 = params
# Print the logistic trendline
print(f'Logistic Trendline: f(x) = 100 / (1 + e^(-{k:.4f} * (x - {x0:.4f})))')
# Create input data for plotting the trendline
X_range = np.linspace(0, max(X), 100)
# Create the output prediction for plotting the trendline
Y_pred = logistic_func(X_range, k, x0)
# Plot the logistic trendline
plt.plot(X_range, Y_pred, 'b-', label=f'Logistic Trendline: f(x) = 100 / (1 + e^(-{k:.4f} * (x - {x0:.4f})))')

''' Find the JND '''

plt.axhline(threshold, c='r', linestyle='dashed', label=f'{threshold}% Threshold (JND)')
plt.axvline(x0, c='r', linestyle='dashed')
plt.annotate(f'JND = {x0:.2f}', xy=(x0, threshold), xytext=(x0 + 0.1, threshold + 2.5), c='r')
print(f'Just-Noticeable Difference (JND): {x0:.4f}')

''' Style the graph and show it '''

# Set the plot labels and title
plt.xlabel('Stimulus Difference')
plt.ylabel('Proportion Judged As Different (%)')
plt.title('Just-Noticeable Difference (JND) Measurement')
plt.yticks([0,20,40,60,80,100])
# Show the legend and graph
plt.legend(prop={'size': 8})
plt.tight_layout()
plt.show()