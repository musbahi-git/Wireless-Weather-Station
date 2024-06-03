# Written by Al-Musbahi for CUOL Rocket Society
# This script reads temperature and humidity data from a DHT11 sensor and plots it in real-time


import Adafruit_DHT
import time
import matplotlib.pyplot as plt
import csv
import os

# Set sensor type : DHT11
sensor = Adafruit_DHT.DHT11

# Set GPIO sensor is connected to
gpio = 4

# File to save data
data_file = 'dht11_data.csv'

# Check if the file exists
file_exists = os.path.isfile(data_file)

# Initialize CSV file with headers if it doesn't exist
if not file_exists:
    with open(data_file, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Temperature (C)', 'Humidity (%)'])

# Use lists to store the readings for plotting
temperature_data = []
humidity_data = []
time_data = []

try:
    print("Press Ctrl+C to stop the program.")
    while True:
        # Use read_retry method. This will retry up to 15 times to
        # get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)

        # Reading data
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
            timestamp = time.time()
            temperature_data.append(temperature)
            humidity_data.append(humidity)
            time_data.append(timestamp)

            # Append data to CSV file
            with open(data_file, mode='a') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, temperature, humidity])
        else:
            print('Failed to get reading. Try again!')

        # Wait before repeating loop
        time.sleep(2)

except KeyboardInterrupt:
    # Plot the data
    plt.figure()
    plt.plot(time_data, temperature_data, label='Temperature (C)')
    plt.plot(time_data, humidity_data, label='Humidity (%)')
    plt.xlabel('Time (s)')
    plt.ylabel('Value')
    plt.legend()
    plt.show()
