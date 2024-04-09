from typing import Sequence
from numpy import ndarray

import mss.tools
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import keyboard
import time

bounding_box_default = {'top': 70, 'left': 0, 'width': 940, 'height': 520}


def get_screen_capture(
        bounding_box: dict = bounding_box_default) -> np.ndarray:
    """
    :param bounding_box: part of the screen to capture
    :return: image of the game screen
    """
    with mss.mss() as sct:
        im = np.array(sct.grab(bounding_box_default))
        return cv.cvtColor(im, cv.COLOR_BGRA2BGR)


def get_screen_capture_with_debug(
        bounding_box: dict = bounding_box_default) -> np.ndarray:
    """
    Shows the captured part of the screen. Press 'enter' to close.
    :param bounding_box: part of the screen to capture
    :return: image of the game screen
    """
    pixels = get_screen_capture(bounding_box)
    cv.imshow('', pixels)
    cv.waitKey(0)
    print(pixels.shape)
    return pixels


def get_char_pos(bg: np.ndarray) -> Sequence[int]:
    """
    :return: max_loc value, which is the upper left corner of the match
    """
    template = cv.cvtColor(
            np.array(cv.imread('template.png')), cv.COLOR_BGRA2BGR)
    w, h = template.shape[:2]  # crop extra dimensions if present
    res = cv.matchTemplate(bg, template, cv.TM_CCOEFF_NORMED)
    _minVal, _maxVal, _minLoc, _maxLoc = cv.minMaxLoc(res, None)
    return _maxLoc if _maxVal > 0.8 else (-1, -1)


def get_char_pos_with_debug(
        bg: np.ndarray,
        template_filepath='template.png',
        show_pic=False
        ) -> tuple[Sequence[int], ndarray]:
    """
    :param show_pic: whether or not to display the found char on the canvas
    :return: max_loc value and the image of the found character
    """
    template = cv.cvtColor(cv.imread(template_filepath), cv.COLOR_BGRA2BGR)
    h, w = template.shape[:2]

    res = cv.matchTemplate(bg, template, cv.TM_CCOEFF_NORMED)
    _minVal, _maxVal, _minLoc, _maxLoc = cv.minMaxLoc(res, None)
    print(f'minVal: {_minVal}, maxVal: {_maxVal}, minLoc: {_minLoc}, maxLoc: {_maxLoc}')

    # if not certain enough, return char not found
    if _maxVal < 0.8:
        return (-1, -1), None

    top_left = _maxLoc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    if show_pic:
        w, h = template.shape[:2]
        cv.rectangle(bg, top_left, bottom_right, 255, 2)
        plt.imshow(bg)
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.show()

    char_img = bg[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    return top_left, char_img


def press_key(key: str, duration=0.2):
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)


def restart():
    print('restart')
    press_key('r')
    press_key('c')
