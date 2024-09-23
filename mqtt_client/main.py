import os
import socket
import paho.mqtt.client as mqtt
import yaml
import time
import threading
import traceback
import logging
from logging.handlers import RotatingFileHandler
import random

from utils._gpio_driver import GPIOController
from utils._config_manager import ConfigManager
from utils._log import init_logger

cm = ConfigManager()
logger = init_logger(cm.config)

device_name = cm.config['mqtt'].get("device_name","dss0")

gpio_config = cm.config['gpio']

print(gpio_config)

gpio_controller = GPIOController(pins = gpio_config['rpi_pins'], 
                                 inverse =gpio_config['inverse'],
                                 release_time = gpio_config['duration'],
                                 mode= gpio_config['mode'])

# Callback for connection
def on_connect(client, userdata, flags, reason_code, properties):
    print("connected")
    if reason_code == 0:
        logger.info("Connected to MQTT broker")
        client.subscribe(f"{device_name}/cmd/time")
        client.subscribe(f"{device_name}/cmd/mode")
        client.subscribe(f"{device_name}/cmd/duration")

        print(f"Subscribed to {device_name}/cmd/time")
        print(f"Subscribed to {device_name}/cmd/mode")
        print(f"Subscribed to {device_name}/cmd/duration")
    else:
        logger.error(f"Failed to connect to MQTT broker")

# Callback for received message
def on_message(client, userdata, msg):
    logger.info(f"Topic: {msg.topic}, Message: {msg.payload.decode()}")
    topic = msg.topic.split('/')[-1]
    print(topic)
    
    if topic != 'time':
        print("saving config...")
        cm.config['gpio'][topic] = msg.payload.decode()
        cm.save_config()
        

# Initialize MQTT client
client_id = f'{device_name}_{random.randint(0, 1000)}'


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

# Read MQTT broker address and connect
mqtt_broker = cm.config['mqtt']['broker']['ip']
mqtt_port = cm.config['mqtt']['broker']['port']

while True:
    try:
        client.connect(mqtt_broker, mqtt_port, 60)
        break

    except Exception as e:
        logger.error(f"Failed to connect to MQTT broker at {mqtt_broker}:{mqtt_port}, retrying in 5 seconds")
        print(e)
        time.sleep(5)


# publish messages to the broker every 1 minute
def publish_time():
    while True:
        try:
            current_time = int(time.time())
            client.publish(f"{device_name}/stat/time", current_time)
            logger.info(f"Published time: {current_time}")
            time.sleep(60)
        except Exception as e:
            logger.error(f"Failed to publish time: {e}")
            time.sleep(5)

# Start the thread for publishing time
publish_thread = threading.Thread(target=publish_time)
publish_thread.start()

# Loop forever, handling reconnects and messages
client.loop_forever()
