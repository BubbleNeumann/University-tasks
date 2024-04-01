from typing import Sequence
from numpy import ndarray

import os
import mss.tools
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

bounding_box_default = {'top': 140, 'left': 360, 'width': 380, 'height': 380}
action_space = ['a', 'd', 'space', 'a+x', 'd+x', 'z+w']

COMPRESS_COEFF = 4


def get_screen_capture(
        bounding_box: dict = bounding_box_default,
        cc=COMPRESS_COEFF,
        grayscale=True
        ) -> np.ndarray:
    """
    :param cc: compress coefficient
    :param bounding_box: part of the screen to capture
    :return: resized by COMPRESS_COEFF grayscale image of the game screen
    """
    with mss.mss() as sct:
        im = np.array(sct.grab(bounding_box_default))
        pixels = cv.cvtColor(im, cv.COLOR_BGRA2GRAY if grayscale else cv.COLOR_BGRA2RGB)
        return cv.resize(
            pixels,
            (bounding_box['width'] // cc,
             bounding_box['height'] // cc)
        )


def get_screen_capture_with_debug(
        bounding_box: dict = bounding_box_default,
        # cc=COMPRESS_COEFF
        ) -> np.ndarray:
    """
    Shows the captured part of the screen.
    :param cc: compress coefficient
    :param bounding_box: part of the screen to capture
    :return: grayscale image of the game screen
    """
    pixels = get_screen_capture(bounding_box)
    cv.imshow('', pixels)
    print(pixels.shape)
    return pixels


def get_char_pos(
        bg: np.ndarray,
        cc=COMPRESS_COEFF,
        grayscale=True,
        ) -> Sequence[int]:
    """
    :return: max_loc value, which is the upper left corner of the match
    """
    max_val = (0, None)
    for file in os.listdir('templates/'):
        template = cv.cvtColor(
                np.array(cv.imread(file)),
                cv.COLOR_BGRA2GRAY if grayscale else cv.COLOR_BGRA2RGB)
        w, h = template.shape[:2]  # crop extra dimensions if present
        template = cv.resize(template, (w // cc, h // cc))
        w, h = template.shape[:2]
        res = cv.matchTemplate(bg, template, cv.TM_CCOEFF_NORMED)
        _minVal, _maxVal, _minLoc, _maxLoc = cv.minMaxLoc(res, None)
        if _maxVal > max_val[0]:
            max_val = (_maxVal, _maxLoc)
    return max_val[1]


def get_char_pos_with_debug(
        bg: np.ndarray,
        cc=COMPRESS_COEFF,
        template_filepath='template.png',
        show_pic=False
        ) -> tuple[Sequence[int], ndarray]:
    """
    :param show_pic: whether or not to display the found char on the canvas
    :return: max_loc value and the image of the found character
    """
    template = cv.cvtColor(np.array(cv.imread(template_filepath)), cv.COLOR_BGRA2GRAY)

    w, h = template.shape
    template = cv.resize(template, (w // cc, h // cc))
    w, h = template.shape

    res = cv.matchTemplate(bg, template, cv.TM_CCOEFF_NORMED)
    _minVal, _maxVal, _minLoc, _maxLoc = cv.minMaxLoc(res, None)

    top_left = _maxLoc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    if show_pic:
        w, h = template.shape
        cv.rectangle(bg, top_left, bottom_right, 255, 2)
        plt.imshow(bg)
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.show()

    # frame = frame[y1:y2,x1:x2]
    # char_img = bg[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]]
    char_img = bg[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

    return top_left, char_img


if __name__ == '__main__':
    pixels = get_screen_capture_with_debug()
    char_pos, _ = get_char_pos_with_debug(pixels, show_pic=True)
