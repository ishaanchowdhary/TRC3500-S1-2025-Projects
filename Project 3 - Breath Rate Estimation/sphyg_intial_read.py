'''
Written by: Ishaan Guha Chowdhary (33115303)
Last edited: 19/05/2025

Program for getting live input of initial sphygmamometer readings and calibrating the setup
'''

import serial
import time
import numpy as np
from collections import deque
import matplotlib.pyplot as plt

# Serial configuration
SERIAL_PORT = 'COM5'      # Replace with your port, e.g., '/dev/ttyUSB0' or 'COM3'
BAUD_RATE = 115200
WINDOW_SIZE = 100         # Number of samples to keep
DT = 0.2                  # Sampling interval (e.g., 5 Hz)
