import os 
import threading
import time
import traceback
from collections import deque
def get_device_type():
    uname = str(os.uname())
    if "rpi" in uname:
        return 'rpi'
    elif "tegra" in uname:
        return "jetson"
    elif "x86_64" in uname:
        return "x86"
    elif "Darwin" in uname:
        return "darwin"
    else:
        return None

device_type = get_device_type()


try:
    if device_type == "rpi":
        import RPi.GPIO as GPIO
    elif device_type == "jetson":
        import Jetson.GPIO as GPIO
    else:
        raise RuntimeError("Unsupported device type")
except Exception as e:
    print(traceback.format_exc())
    print(f"Error occurred in importing GPIO Library: {str(e)}. Ensure you have the necessary privileges (use 'sudo' to run the script).")
    GPIO = None


class GPIOController:
    def __init__(self, pins, release_time=3):
        self.GPIO_INTERVAL = release_time
        self.pins = pins
        self.pin_threads = {}
        self.pin_events = {}

        if GPIO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            for pin in self.pins:
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
                self.pin_threads[pin] = None  # 초기화 시 각 핀의 스레드 관리
                self.pin_events[pin] = threading.Event()  # 스레드 상태를 관리할 Event 생성

    def set_release_time(self, release_time):
        self.GPIO_INTERVAL = release_time

    def activate_pin(self, pin_index):
        if GPIO and pin_index < len(self.pins):
            pin = self.pins[pin_index]

            if not self.pin_events[pin].is_set():  # 기존 스레드가 실행 중인지 확인
                self.pin_events[pin].set()  # 스레드가 실행 중임을 표시
                self.pin_threads[pin] = threading.Thread(target=self._activate_pin_thread, args=(pin,))
                self.pin_threads[pin].start()

            else:
                print(f"warn : Pin {pin} is currently in use")

    def _activate_pin_thread(self, pin):
        try:
            GPIO.output(pin, GPIO.LOW)
            time.sleep(self.GPIO_INTERVAL)
            GPIO.output(pin, GPIO.HIGH)
        finally:
            self.pin_events[pin].clear()  # 스레드가 종료되었음을 표시
            print(f"Pin {pin} released")