import os
import sys
import json
import logging
import time
import datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import Adafruit_DHT

# Change it to 11 or 22 based on your sensor
DHT_TYPE = Adafruit_DHT.DHT22
DHT_PIN = 4

# AWS IoT Configuration
useWebsocket = False
host = "xxxxxxxx.amazonaws.com"
rootCAPath = "root-CA.pem"
certificatePath = "xxxxx-certificate.pem.crt"
privateKeyPath = "xxxxx-private.pem.key"
Client_ID = "RaspberryPi"
AWS_IOT_MY_THING_NAME = "Your Thing Name"

# Configure logging
logger = logging.getLogger("core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Initialize AWSIoTMQTTClient
myShadowClient = AWSIoTMQTTClient(Client_ID)
myShadowClient.configureEndpoint(host, 8883)
myShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myShadowClient.connect()

# Topic configuration
topic = "awsiot/dht22"
delay_sec = 10
sensor_id = 'DHT22_xxx'

try:
    while True:
        humidity, temperature = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)
        timestamp = datetime.datetime.now()

        if humidity is not None and temperature is not None:
            print('\n--------------------------------------------------------')
            print(f" Output is here\n Time: {timestamp}\n Temperature: {temperature} C  Humidity: {humidity} timestamp: {timestamp}")

            msg = f'"Pi_timestamp": "{timestamp}","Sensor": "{sensor_id}", "Temperature": "{temperature}","Humidity": "{humidity}"'
            msg = f'{{{msg}}}'

            print(msg)
            print('--------------------------------------------------------\n')

            status = myShadowClient.publish(topic, msg, 1)
            if status:
                print(f"Updated {status}")
            print(f'Sleeping for {delay_sec} ...')
            time.sleep(delay_sec)
        else:
            pass

except KeyboardInterrupt:
    pass

finally:
    print('Exiting the loop')
    myShadowClient.disconnect()
    print('Disconnected from AWS')
