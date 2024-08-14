from pathlib import Path
import os
import yaml 
HOME = str(Path.home())

# 기본 설정
default_config = {
    'mqtt': {
        'broker': {
            'ip': '192.168.11.38',
            'port': 1883
        },
        'device_type': 'dss',
        'mode': 1,
    },
    'gpio': {
        'release_time': 3,
        'rpi_pins': [16,20,21],
        'jetson_pins': [12, 13, 18],
        'default_pins': [1, 2, 3]
    },
    'logging': {
        'level': 'INFO',
        'file': f'/logs/gpio_driver.log'
    }
}


class ConfigManager:
    def __init__(self, config_path ='/iodev/iodev.yaml'):
        self.path = config_path

        # check if config_path is absolute or relative
        if not os.path.isabs(self.path):
            self.path = os.path.join(HOME, self.path)

        else:
            self.path = config_path

            # check if the directory exists
            if not os.path.exists(os.path.dirname(self.path)):
                print(f"config_path is not exist, Creating directory {os.path.dirname(self.path)}")
                os.makedirs(os.path.dirname(self.path))

        self.config = self.load_config(self.path)


    def load_config(self,config_path):
        # 설정 파일 로드
        print(f"loading config - {config_path}")
        if not os.path.exists(config_path):
            print(f"Default configuration file created at {config_path}")

            with open(config_path, 'w') as file:
                yaml.safe_dump(default_config, file)
            
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        return config

    def save_config(self):
        with open(self.path, 'w') as file:
                yaml.safe_dump(self.config, file)



