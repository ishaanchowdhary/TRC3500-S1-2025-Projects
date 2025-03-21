# File Name: moisture.py
# Authors: Ishaan Chowdhary, Emanuel Risso
# Created: 20/03/2025
# Last Modified: 22/03/2025
# Last Modifier: Emanuel Risso
# Python v. 3.13.2

''' File Overview '''

# This program fits a 4th-degree polynomial model to the specified calibration data.
# It then maps the live ADC values passed through a serial connection to the polynomial.
# The percentage of moisture is then passed to the terminal.

''' Module Imports '''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import serial

''' Calculate the fitted 4th-degree polynomial transfer function from calibration data '''

# Load data from the CSV
filePath = "data.csv"  # Change this to the actual file path
data = pd.read_csv(filePath)

# Extract the necessary columns' data
mlWater = data.iloc[:, 0].values
meanVsig = data.iloc[:, -1].values

# Fit a 4th-degree polynomial using the data
coeffs = np.polyfit(meanVsig, mlWater, 4)
polyEqu = np.poly1d(coeffs)

# Generate fitted values for plotting
xFit = np.linspace(min(mlWater), max(mlWater), 100)
yFit = polyEqu(xFit)

''' Plot the data and regression curve '''

plt.scatter(mlWater, meanVsig, color='red', label='Data')
plt.plot(xFit, yFit, label=f'4th Degree Fit', color='blue')
plt.xlabel('mL Water')
plt.ylabel('Mean Vsig')
plt.legend()
plt.title('4th Degree Polynomial Regression')
plt.grid()
plt.show()

# Print the polynomial equation
print("Polynomial equation:")
print(polyEqu)
print("-----------------------------------------------------------------------------------")

''' Calibrate the live ADC values to the transfer function and print the moisture data '''

# Set the serial connection to use the correct port and baud rate
ser = serial.Serial("COM5", 115200, timeout=1)
# Initiate an infinite loop
while True:
    # Read each line from the ADC serial connection output
    data = ser.readline().decode("utf-8").strip()
    try:
        # Convert the data to float type
        adcValue = float(data)
        # print(f'ADC Value: {adcValue}')
        # Convert the ADC data to a specified voltage range
        voltage = (adcValue / 4095) * 3.3
        # print(f'Voltage: {voltage:.2f} V')
        # Fit the voltage against the transfer function
        moisture = polyEqu(voltage)
        moisturePercent = (moisture / 20) * 100
        # Print the moisture percentage
        # if (voltage > 3.11):
        #     print('Moisture: 0%')
        # elif (voltage < 2.21):
        #     print('Moisture: 100%')
        # else:
        # print(f"Moisture: {moisture:.2f} mL")
        print(f"Moisture: {moisturePercent:.2f}%\n")
    except ValueError:
        pass
