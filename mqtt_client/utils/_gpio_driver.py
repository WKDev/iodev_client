import os
import threading
import time
import traceback
from collections import deque
import datetime
import functools
from random import randint
class AssertPi:
    def __init__(self, func):
        self.func = func
        self.is_pi = self.gpio_avaliable()
        functools.update_wrapper(self, func)

    def gpio_avaliable(self):
        try:
            with open("/proc/cpuinfo", "r") as f:
                cpuinfo = f.read()
            return "Raspberry Pi" in cpuinfo or "BCM" in cpuinfo
        except FileNotFoundError:
            return False

    def __get__(self, obj, objtype=None):
        return functools.partial(self.__call__, obj)

    def __call__(self, *args, **kwargs):
        if not self.is_pi:
            func_name = self.func.__name__
            print(f"[warn]This is not a Raspberry Pi, command '{func_name}' ignored")
            return None
        else:
            # print(f"[debug]Executing {self.func.__name__} on Raspberry Pi")
            return self.func(*args, **kwargs)

class GPIOController:
    def __init__(self, **kwargs):
        self.pins = kwargs.get('pins', [16,20,21])
        self.run_on_high = kwargs.get('run_on_high', False)
        self.duration = kwargs.get('duration', 10)
        self.mode = kwargs.get('mode', 0)
        self.GPIO = None
        self.is_running = False
        self.init_gpio()  # GPIO 초기화를 스레드 시작 전에 수행


    @AssertPi
    def init_gpio(self):
        print("Initializing GPIO")
        import RPi.GPIO as GPIO
        self.GPIO = GPIO
        if self.GPIO:
            self.GPIO.setmode(GPIO.BCM)
            self.GPIO.setwarnings(False)
            print(f"GPIO initialized: {self.pins}")
            for pin in self.pins:
                self.GPIO.setup(pin, self.GPIO.OUT)
                # 핀 상태 확인
                initial_state = self.GPIO.input(pin)
                print(f"Pin {pin} initial state: {'HIGH' if initial_state else 'LOW'}")
        else:
            print("GPIO module not found")

    def run_gpio(self):
        if not self.is_running:
            t = threading.Thread(target=self.gpio_thread)
            t.start()
        else:
            print("[warn] GPIO is already running, ignore last cmd.")
        return

    @AssertPi
    def gpio_thread(self):

        self.is_running = True
        print(f"running gpio thread")
        print(f"time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, mode: {'all(0)' if self.mode == 0 else 'random(1)'}")
        try:
            run_sig = self.GPIO.HIGH if self.run_on_high else self.GPIO.LOW
            stop_sig = self.GPIO.LOW if self.run_on_high else self.GPIO.HIGH
            print(f"pins: {self.pins}, trigger on: {'HIGH' if run_sig == self.GPIO.HIGH else 'LOW'}")

            self.write_all(run_sig)
            time.sleep(self.duration)
            self.write_all(stop_sig)
            print(f"\nGPIO done, time {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"Error in GPIO thread: {e}")
            traceback.print_exc()
        finally:
            self.is_running = False
            # GPIO cleanup은 여기서 수행하지 않음

    def write_all(self, level):
        for pin in self.pins:
            self.GPIO.output(pin, level)
            # 핀 상태 확인 및 출력
            actual_state = self.GPIO.input(pin)
            print(f"Pin {pin} set to {'HIGH' if level == self.GPIO.HIGH else 'LOW'}, actual state: {'HIGH' if actual_state else 'LOW'}")

    def cleanup(self):
        if self.GPIO:
            self.GPIO.cleanup()
            print("GPIO cleaned up")

if __name__ == "__main__":

    
    gc = GPIOController(pins=[16, 20, 21])
    time.sleep(1)
    print("--------------")
    for i in range(2):
        sleeptime = randint(0,20)

        print(f"sleep: {sleeptime}")
        gc.run_gpio()
        time.sleep(sleeptime/10)
        print("-----")