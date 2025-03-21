import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load data from CSV
file_path = "data.csv"  # Change this to the actual file path
data = pd.read_csv(file_path)

# Extract relevant columns
ml_water = data.iloc[:, 0].values
mean_vsig = data.iloc[:, -1].values

# Fit a 4th-degree polynomial
coeffs = np.polyfit(ml_water, mean_vsig, 4)
poly_eq = np.poly1d(coeffs)

# Generate fitted values for plotting
x_fit = np.linspace(min(ml_water), max(ml_water), 100)
y_fit = poly_eq(x_fit)

# Plot data and regression curve
plt.scatter(ml_water, mean_vsig, color='red', label='Data')
plt.plot(x_fit, y_fit, label=f'4th Degree Fit', color='blue')
plt.xlabel('mL Water')
plt.ylabel('Mean Vsig')
plt.legend()
plt.title('4th Degree Polynomial Regression')
plt.grid()
plt.show()

# Print polynomial equation
print("Polynomial equation:")
print(poly_eq)
