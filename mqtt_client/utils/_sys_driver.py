import os 
import threading
import time
import traceback
from collections import deque

from _config_manager import ConfigManager


class AssertPi:
    def __init__(self, func):    # 호출할 함수를 인스턴스의 초깃값으로 받음
        self.func = func         # 호출할 함수를 속성 func에 저장

        self.is_pi = self.gpio_avaliable()  # 데코레이터가 호출되면 라즈베리파이인지 확인
    
    def gpio_avaliable(self):
        try:
            with open("/proc/cpuinfo", "r") as f:
                cpuinfo = f.read()
                # "Raspberry Pi" 관련 문자열이나 BCM2835 등의 문자열을 찾음
                return "Raspberry Pi" in cpuinfo or "BCM" in cpuinfo
        except FileNotFoundError:
            return False  # 해당 파일이 없으면 라즈베리파이가 아님
        
    def __call__(self):
        if not self.is_pi:
            func_name = self.func.__name__
            print(f"[warn]This is not a Raspberry Pi, command '{func_name}' ignored")
            return None
        else:
            return self.func()

class GPIOController:
    def __init__(self, config_manager: ConfigManager):
        self.cm = config_manager
    
    @AssertPi
    def init_gpio(self):
        print("Initializing GPIO")
        import RPi.GPIO as GPIO

        if GPIO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            for pin in self.pins:
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
                self.pin_threads[pin] = None

    def build_pin_events(self, **kwargs):
        for key, value in kwargs.items():
            print(f"building: {key} to {value}")
            self.cm.config.update({key: value})        
        print(f"Config updated: {kwargs.keys()}")

    def start_pin_thread(self, pin):
        if self.pin_threads[pin] is None:
            self.pin_threads[pin] = threading.Thread(target=self.pin_thread, args=(pin,))
            self.pin_threads[pin].start()


    def pin_thread(self, pin):



if __name__ == "__main__":
    gc = GPIOController([16, 20, 21])
    gc.init_gpio()