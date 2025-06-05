# File Name: project3mse.py
# Author: Emanuel Risso
# ID: 33123225
# Created: 2025/06/05
# Last Modified: 2025/06/05
# Python v. 3.13.2

''' Import Modules '''

import csv
import numpy as np

''' Store CSV Data Into Lists '''

# Specify the filename
fileName = 'data.csv' #####

# Create an empty list for the rows
rows = []
# Read the csv file
with open(fileName, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    # Put each row into the rows list
    for row in csvreader:
        rows.append(row)

# Create an empty list for the columns
columns = []
# For each column
for i in range(0, len(row)):
    # Reset the placeholder column list
    column = []
    # For each row
    for j in range(0, len(rows)):
        # Set the placeholder column to the column values
        column.append(rows[j][i])
    # Append the column to the list of columns
    columns.append(column)

''' Format Data Into Arrays '''

# Create a list for the predicted values
pred_values = []
# For each value in the column
for value in columns[0]: #####
    # Append the data into the list
    pred_values.append(float(value))
# Convert the list to an array
pred_values = np.array(pred_values)

''' Find the Mean Squared Error '''

# Calculate the squared error
squared_error = np.square(19 - pred_values) #####
# Take the mean of the squared error
mean_squared_error = np.mean(squared_error)
# Print the mean squared error
print(f'MSE: {mean_squared_error:.4f}')
