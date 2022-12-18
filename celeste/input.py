import time
from pynput.keyboard import Controller

keyboard = Controller()
time.sleep(10)
keyboard.press('a')
time.sleep(1)
keyboard.release('a')

