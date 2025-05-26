'''
Written by: Ishaan Guha Chowdhary (33115303)
Last edited: 26/05/2025

Program for getting live input of initial sphygmamometer readings and calibrating the setup
'''

import serial
import time
from collections import deque
import csv
import os

# Serial configuration
SERIAL_PORT = 'COM5'      # e.g., '/dev/ttyUSB0' for Linux, 'COM3' for Windows
BAUD_RATE = 115200
WINDOW_SIZE = 100         # Keep last 100 samples
DT = 0.2                  # Sampling interval in seconds
#hellloooooooo my naem is .... hwo r us 
# CSV file setup
CSV_FILENAME = "data/sensor_sphyg_log.csv"
CSV_HEADERS = ["Sphygmomameter", "Timestamp"]

# Initialize deques to hold recent values
sphyg_vals = deque(maxlen=WINDOW_SIZE)
timestamps = deque(maxlen=WINDOW_SIZE)

def parse_line(line):
    """Parses a line like '23.4,102.1,12.5' into floats."""
    try:
        parts = line.strip().split(',')
        if len(parts) != 2:
            return None
        sphyg, ts = map(float, parts)
        return sphyg, ts
    except ValueError:
        return None

def ensure_csv_file():
    """Creates the CSV file with headers if it doesn't exist."""
    if not os.path.exists(CSV_FILENAME):
        with open(CSV_FILENAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)
        print(f"[INFO] Created CSV file: {CSV_FILENAME}")

def log_to_csv(row):
    """Appends a row of data to the CSV file."""
    with open(CSV_FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)

def main():
    ensure_csv_file()

    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"[INFO] Reading from {SERIAL_PORT} at {BAUD_RATE} baud... Logging to {CSV_FILENAME}")

            while True:
                if ser.in_waiting:
                    line = ser.readline().decode('utf-8', errors='ignore')
                    parsed = parse_line(line)
                    if parsed:
                        sphyg, ts = parsed
                        sphyg_vals.append(sphyg)
                        timestamps.append(ts)

                        log_to_csv([sphyg,ts])
                        print(f"sphyg: {sphyg:.2f} | Time: {ts:.2f}")
                # time.sleep(DT)

    except serial.SerialException as e:
        print(f"[ERROR] Serial port error: {e}")
    except KeyboardInterrupt:
        print("\n[INFO] Serial reading stopped by user.")

if __name__ == "__main__":
    main()
