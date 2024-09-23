from pathlib import Path
import os
import yaml 

# 기본 설정
default_config = {
    'gpio': {
        'jetson_pins': [12, 13, 18],
        'rpi_pins': [16, 20, 21]
    },
    'logging': {
        'file': '/logs/gpio_driver.log',
        'level': 'INFO'
    },
    'mqtt': {
        'broker': {
            'ip': '192.168.11.38',
            'port': 1883
        },
        'device_type': 'dss',
        'device_name': 'dss0'
    },
    'stat': {
        'topic': 'stat',
        'publish_rate': 5  # seconds
    },
    'cmd': {
        'topic': 'cmd'
    }
}

class ConfigManager:
    def __init__(self, config_path ='iodev.yaml'):
        self.path = config_path
        self.config : dict = self.load_config(self.path)

    def load_config(self,config_path):
        # 설정 파일 로드
        print(f"loading config - {config_path}")
        if not os.path.exists(config_path):
            print(f"[WARN]Default configuration file created at {config_path}")

            with open(config_path, 'w') as file:
                yaml.safe_dump(default_config, file)

        else:
            print(f"Config file exists at {config_path}")
            
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)

        return config

    def save_config(self):
        print(f"save to {self.path}")
        with open(self.path, 'w') as file:
                yaml.safe_dump(self.config, file)


if __name__ == "__main__":
    config = ConfigManager()

