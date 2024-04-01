import random
import keyboard
import time
import cv2

from pico import get_char_pos, action_space, get_screen_capture


def press_key(key: str, duration=0.1):
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)


def get_char_images(bg, num_of_samples=10):
    time.sleep(2)
    for num in range(num_of_samples):
        # key = action_space[random.randint(0, len(action_space)-1)]
        # keyboard.press_and_release(key)
        # keyboard.press(key)
        # time.sleep(0.1)
        cv2.imwrite(f'char_pics/{num}.jpg', get_char_pos(bg, cc=1, grayscale=False)[1])
        # keyboard.release(key)


if __name__ == '__main__':
    bg = get_screen_capture(cc=1, grayscale=False)
    cv2.imwrite('char_pics/0.jpg', get_char_pos(bg, cc=1, grayscale=False)[1])
