import serial
import pandas as pd
from datetime import datetime

# Configure the serial connection (change 'COM3' to your specific port)
ser = serial.Serial('COM3', 115200, timeout=1)

# Initialize an empty DataFrame with appropriate columns
df = pd.DataFrame(columns=['Timestamp', 'Temp mean (C)', 'Temp max (C)', 'Hum mean (%)', 'Hum max (%)',
                           'Pres mean (hPa)', 'Pres max (hPa)', 'Pres dev mean (hPa)', 'Pres dev max (hPa)'])

# Function to parse the serial data
def parse_serial_data(line):
    # Assuming the line format is "Temperature:XX.XX C Humidity:XX.XX% Pressure:XX.XX hPa"
    parts = line.strip().split()
    print("PARTS ", parts)  # Print the parts for debugging
    temp_mean = parts[1]
    temp_max = parts[3]
    hum_mean = parts[5]
    hum_max = parts[7]
    pres_mean = parts[9]
    pres_max = parts[11]
    pres_dev_mean = parts[13]
    pres_dev_max = parts[15]
    return  float(temp_mean), float(temp_max), \
            float(hum_mean), float(hum_max), \
            float(pres_mean), float(pres_max), \
            float(pres_dev_mean), float(pres_dev_max)

# Main loop to read data and append to the DataFrame
try:
    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            print("LINE THAT ENTERS ", line)  # Print the line for debugging
            if line.startswith("Temp_mean:"):
                try:
                    temp_mean, temp_max, \
                    hum_mean, hum_max, \
                    pres_mean, pres_max, \
                    pres_dev_mean, pres_dev_max = parse_serial_data(line)
                    timestamp = datetime.now()
                    # Create a new row as a dictionary
                    new_row = {'Timestamp': timestamp, 'Temp mean (C)': temp_mean, 'Temp max (C)': temp_max,
                               'Hum mean (%)': hum_mean, 'Hum max (%)': hum_max,
                               'Pres mean (hPa)': pres_mean, 'Pres max (hPa)': pres_max,
                               'Pres dev mean (hPa)': pres_dev_mean, 'Pres dev max (hPa)': pres_dev_max}
                    # Append the new row to the DataFrame
                    new_row_df = pd.DataFrame([new_row])
                    df = pd.concat([df, new_row_df], ignore_index=True)
                    # Save the DataFrame to a CSV file
                    df.to_csv('trials/prueba_buffers_cami_12_07.csv', index=False)
                except Exception as e:
                    print(f"Error parsing line: {e}")
except KeyboardInterrupt:
    # Close the serial connection when interrupted
    ser.close()
    print("Serial connection closed.")
