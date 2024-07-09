import pandas as pd
import matplotlib.pyplot as plt

# Assuming your dataframe is named 'df'
# Replace 'df' with the actual name of your dataframe
df = pd.read_csv('trials/mal_puesto_01_cami_09_07.csv')

# Extracting the data from the dataframe
# Convert time strings to datetime objects
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Subtract the first time to reset to zero
df['time_seconds'] = (df['Timestamp'] - df['Timestamp'].iloc[0]).dt.total_seconds()

# Display the result
print(df)
time = df['time_seconds']
temperature = df['Temperature (C)']
humidity = df['Humidity (%)']
pressure = df['Pressure (hPa)']

fig, ax = plt.subplots(3, 1, sharex=True)

# Plotting the data
ax[0].plot(time, temperature, label='Temperatura')
ax[0].set_title('Temperatura en función del tiempo')
ax[0].set_ylabel('Temperatura (°C)')
ax[0].set_ylim([10, 35])  # Set the y-axis limits
ax[0].grid(True)
ax[1].plot(time, humidity, label='Humedad')
ax[1].set_title('Humedad en función del tiempo')
ax[1].set_ylabel('Humedad (%)')
ax[1].set_ylim([0, 100])  # Set the y-axis limits
ax[1].grid(True)
ax[2].plot(time, pressure, label='Presión')
ax[2].set_title('Presión en función del tiempo')
ax[2].set_ylabel('Presión (hPa)')
ax[2].set_ylim([900, 1000])  # Set the y-axis limits
ax[2].set_xlabel('Tiempo (s)')
ax[2].grid(True)

# Adding vertical red lines at specific times (replace with your desired times)
redline_times = [120, 180]  # example times in seconds

redline_labels = ['Event 1', 'Event 2']  # labels for the vertical lines
already_plotted = False
for ax in ax:
    for redline_time, redline_label in zip(redline_times, redline_labels):
        ax.axvline(x=redline_time, color='red', linestyle='--', linewidth=1)
        

# Displaying the plot
plt.show()
