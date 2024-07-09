import serial
import pandas as pd
from datetime import datetime

# Configure the serial connection (change 'COM3' to your specific port)
ser = serial.Serial('COM3', 115200, timeout=1)

# Initialize an empty DataFrame with appropriate columns
df = pd.DataFrame(columns=['Timestamp', 'Temperature (C)', 'Humidity (%)', 'Pressure (hPa)'])

# Function to parse the serial data
def parse_serial_data(line):
    # Assuming the line format is "Temperature:XX.XX C Humidity:XX.XX% Pressure:XX.XX hPa"
    parts = line.strip().split()
    print("PARTS ", parts)  # Print the parts for debugging
    temperature = parts[1]
    humidity = parts[4]
    pressure = parts[7]
    return float(temperature), float(humidity), float(pressure)

# Main loop to read data and append to the DataFrame
try:
    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            print("LINE THAT ENTERS ", line)  # Print the line for debugging
            if line.startswith("Temperature:"):
                try:
                    temperature, humidity, pressure = parse_serial_data(line)
                    timestamp = datetime.now()
                    # Create a new row as a dictionary
                    new_row = {'Timestamp': timestamp, 'Temperature (C)': temperature, 'Humidity (%)': humidity, 'Pressure (hPa)': pressure}
                    # Append the new row to the DataFrame
                    new_row_df = pd.DataFrame([new_row])
                    df = pd.concat([df, new_row_df], ignore_index=True)
                    # Save the DataFrame to a CSV file
                    df.to_csv('trials/mal_puesto_01_cami_09_07.csv', index=False)
                except Exception as e:
                    print(f"Error parsing line: {e}")
except KeyboardInterrupt:
    # Close the serial connection when interrupted
    ser.close()
    print("Serial connection closed.")
