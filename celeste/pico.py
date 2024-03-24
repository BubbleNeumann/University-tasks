import mss.tools
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


bounding_box_default = {'top': 140, 'left': 360, 'width': 380, 'height': 380}
action_space = [
    'a',
    'd',
    'space',
    'a+x',
    'd+x'
]


def get_screen_capture(
        bounding_box: dict = bounding_box_default) -> np.ndarray:
    """
    :param bounding_box: part of the screen to capture
    :return: grayscale image of the game screen
    """
    with mss.mss() as sct:
        im = np.array(sct.grab(bounding_box_default))
        return cv.cvtColor(im, cv.COLOR_BGRA2GRAY)


def get_screen_capture_with_debug(
        bounding_box: dict = bounding_box_default) -> np.ndarray:
    """
    Shows the captured part of the screen.
    :param bounding_box: part of the screen to capture
    :return: grayscale image of the game screen
    """
    pixels = get_screen_capture(bounding_box)
    cv.imshow('', pixels)
    return pixels


def get_char_pos(
        bg: np.ndarray, template_filepath='template.png') -> tuple[int, int]:
    """
    :return: max_loc value, which is the upper left corner of the match
    """
    template = cv.cvtColor(
        np.array(
            cv.imread(template_filepath)),
        cv.COLOR_BGRA2GRAY)
    return cv.matchTemplate(pixels, template, cv.TM_CCOEFF_NORMED)[3]


def get_char_pos_with_debug(
        bg: np.ndarray, template_filepath='template.png') -> tuple[int, int]:
    """
    :return: max_loc value, which is the upper left corner of the match
    """
    template = cv.cvtColor(
        np.array(
            cv.imread(template_filepath)),
        cv.COLOR_BGRA2GRAY)

    res = cv.matchTemplate(pixels, template, cv.TM_CCOEFF_NORMED)
    _minVal, _maxVal, _minLoc, _maxLoc = cv.minMaxLoc(res, None)

    top_left = _maxLoc
    w, h = template.shape
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv.rectangle(pixels, top_left, bottom_right, 255, 2)
    plt.imshow(pixels)
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.show()
    return top_left


if __name__ == '__main__':
    pixels = get_screen_capture_with_debug()
    char_pos = get_char_pos_with_debug(pixels)
