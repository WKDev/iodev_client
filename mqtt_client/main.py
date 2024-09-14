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

from utils._sys_driver import get_device_type, GPIOController
from utils._config_manager import ConfigManager
from utils._log import init_logger

hostname = socket.gethostname()
hostname = hostname.replace('.local', '')
print(f"Hostname: {hostname}")

config = ConfigManager()
logger = init_logger(config.config)

device_type = get_device_type()

gpio_pins = config.config['gpio']['default_pins']
if device_type == "rpi":
    gpio_pins = config.config['gpio']['rpi_pins']
elif device_type == "jetson":
    gpio_pins = config.config['gpio']['jetson_pins']

gpio_controller = GPIOController(gpio_pins, config.config['gpio']['release_time'])

# Callback for connection
def on_connect(client, userdata, flags, reason_code, properties):
    print("connected")
    if reason_code == 0:
        logger.info("Connected to MQTT broker")
        client.subscribe(f"{hostname}/time")
        client.subscribe(f"{hostname}/mode")
        client.subscribe(f"{hostname}/release_time")

        print(f"Subscribed to {hostname}/time")
        print(f"Subscribed to {hostname}/mode")
        print(f"Subscribed to {hostname}/release_time")
    else:
        logger.error(f"Failed to connect to MQTT broker, return code {rc}")

# Callback for received message
def on_message(client, userdata, msg):
    logger.info(f"Topic: {msg.topic}, Message: {msg.payload.decode()}")
    topic = msg.topic.split('/')[-1]

    
    if topic in ['mode', 'release_time', 'time']:
        config.config['mqtt'][topic] = msg.payload.decode()

        config.save_config()
        
        # If the topic is 'release_time', update GPIO release time
        if topic == 'release_time':
            gpio_controller.set_release_time(int(msg.payload.decode()))
        
        # If the topic is 'time', handle GPIO logic
        elif topic == 'time':   
            new_timestamp = int(msg.payload.decode())
            current_timestamp = int(time.time())
            if abs(current_timestamp - new_timestamp) <= 5:
                logger.info("Time is in sync")
                logger.info(f"Activating GPIO pins for {gpio_controller.GPIO_INTERVAL} seconds")

                gpio_controller.activate_pin(0)
                gpio_controller.activate_pin(1)
                gpio_controller.activate_pin(2)

# Initialize MQTT client
client_id = f'iodev_client_{random.randint(0, 1000)}'


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

# Read MQTT broker address and connect
mqtt_broker = config.config['mqtt']['broker']['ip']
mqtt_port = config.config['mqtt']['broker']['port']

while True:
    try:
        client.connect(mqtt_broker, mqtt_port, 60)
        break

    except Exception as e:
        logger.error(f"Failed to connect to MQTT broker at {mqtt_broker}:{mqtt_port}, retrying in 5 seconds")
        time.sleep(5)


# publish messages to the broker every 1 minute
def publish_time():
    while True:
        try:
            current_time = int(time.time())
            client.publish(f"{hostname}/stat/time", current_time)
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
