import Adafruit_DHT
import time

# Sensor configuration
sensor = Adafruit_DHT.DHT11
sensor_pin = 4

while True:
    # Try to grab a sensor reading. Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)

    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        time.sleep(1)
    else:
        print('Failed to get reading. Check the pin numbering and connections!')
