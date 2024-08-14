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
from pathlib import Path


def init_logger(config):
    assert config is not None

    # Logging 설정
    log_level = getattr(logging, config['logging']['level'].upper(), logging.INFO)
    log_file = config['logging']['file']

    # 로그 핸들러 설정
    try:
        if not os.path.exists(os.path.dirname(log_file)):
            os.makedirs(os.path.dirname(log_file))
        handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    except (PermissionError, FileNotFoundError):
        print(f"Failed to create log file at {log_file}. Using default log file at ~/MQTT_Client.log")
        log_file = os.path.expanduser('~/MQTT_Client.log')
        handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)

    logging.basicConfig(level=log_level, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            handler,
                            logging.StreamHandler()
                        ])
    logger = logging.getLogger('MQTT_Client')

    return logger