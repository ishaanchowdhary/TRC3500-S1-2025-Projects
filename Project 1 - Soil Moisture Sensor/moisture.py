# File Name: moisture.py
# Authors: Ishaan Chowdhary, Emanuel Risso
# Created: 20/03/2025
# Last Modified: 23/03/2025
# Last Modifier: Emanuel Risso
# Python v. 3.13.2

''' File Overview '''

# This program fits a 4th degree polynomial model to the specified calibration data.
# It then maps the live ADC values passed through a serial connection to the polynomial.
# The percentage of moisture is then passed to the terminal.

''' Module Imports '''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import serial

''' Calculate the fitted exponential transfer function from calibration data '''

# Load the calibration data from the CSV
filePath = "calibration_data.csv"
data = pd.read_csv(filePath)

# Extract the necessary columns' data
mlWater = data.iloc[:, 0].values
meanVsig = data.iloc[:, 1].values

# Take the log of the water values for exponential fitting
mlWaterLog = np.log(mlWater)

# Fit a linear model to ln(mlWater) = ln(a) + b * meanVsig
b, log_a = np.polyfit(meanVsig, mlWaterLog, 1)

# Convert back to exponential form
a = np.exp(log_a)
expEqu = lambda x: a * np.exp(b * x)

# Generate fitted values for plotting
xFit = np.linspace(min(meanVsig), max(meanVsig), 100)
yFit = expEqu(xFit)

''' Plot the data and regression curve '''

plt.scatter(mlWater, meanVsig, color='red', label='Calibration Data')
plt.plot(yFit, xFit, label=f'Exponential Fit', color='blue')
plt.xlabel('Water (mL)')
plt.ylabel('Mean Voltage (V)')
plt.legend()
plt.title('Moisture Sensor Exponential Regression & Calibration Data')
plt.grid()
plt.show()

# Print the polynomial equation
print(f"Exponential equation: y = {a:.3f} * e^({b:.3f}x)")
print("--------------------------------------------------")

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
        print(f'ADC Value: {adcValue}')
        # Convert the ADC data to a specified voltage range
        voltage = ((adcValue / 4095) * 3.3)
        print(f'Voltage: {voltage:.2f} V')
        # Fit the voltage against the transfer function
        # moisture = polyEqu(voltage)
        moisture = expEqu(voltage)
        moisturePercent = (moisture / 20) * 100
        # Print the moisture percentage
        if (voltage >= max(meanVsig)):
            print(f"Moisture: 0 mL")
            print('Moisture: 0 %\n')
        elif (voltage <= min(meanVsig)):
            print(f"Moisture: 20 mL")
            print('Moisture: 100 %\n')
        else:
            print(f"Moisture: {moisture:.2f} mL")
            print(f"Moisture: {moisturePercent:.2f} %\n")
    except ValueError:
        pass
