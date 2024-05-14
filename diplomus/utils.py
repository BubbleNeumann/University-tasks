from typing import Sequence
from numpy import ndarray

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import mss.tools
import numpy as np
import cv2 as cv
import keyboard
import time
import os

bounding_box_default = {'top': 70, 'left': 0, 'width': 950, 'height': 530}  # msi display
# bounding_box_default = {'top': 130, 'left': 0, 'width': 940, 'height': 520}  # laptop / dell display


def logging(coords, chosen_action, qtable):
    """
    Helps to mannuly track the decisions making progress.
    Only makes sense to call this function if the taken action is not random.
    :param random: whether or not the random action was taken (depends on eps)
    """

    from qlearning import DEFAULT_DIMS

    log_str = ''
    action_space = ['space', 'd+x', 'z+w', 'd', 'a', 'a+x']
    match coords:
        case (0, 7):
            log_str += 'A'
        case (4, 6):
            log_str += 'B'
        case (8, 3):
            log_str += 'C'
    row = coords[1]
    col = coords[0]
    dims = DEFAULT_DIMS
    actions_for_cur_state = qtable[:, row * dims[1] + col]
    # print(actions_for_cur_state, action_space[chosen_action])
    log_str += f'{coords} {action_space[chosen_action]} {actions_for_cur_state}'
    with open('log.txt', 'a') as f:
        f.write(log_str + '\n')


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


def press_key(key, duration=0.2):
    if key == 'z+w':
        duration = 0.9
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)


def restart():
    print('restart')
    press_key('r')
    press_key('c')


def demo(route: list):
    action_space = ['space', 'd+x', 'z+w', 'd', 'a', 'a+x']
    for pos, act in route:
        press_key(action_space[act])


def visualize_progress(route_file=''):
    routes = []

    if route_file == '':
        for file in os.listdir('routes'):
            with open(f'routes/{file}', 'r') as f:
                x = []
                y = []
                for line in f.readlines():
                    col, row, action = line.split(',')
                    y.append(int(row.replace('"', '').replace(')', '')) * 52)
                    x.append(int(col.replace('"', '').replace('(', '')) * 52)
                routes.append((x, y))
    else:
        with open(f'routes/{route_file}', 'r') as f:
            x = []
            y = []
            for line in f.readlines():
                col, row, action = line.split(',')
                y.append(int(row.replace('"', '').replace(')', '')) * 52)
                x.append(int(col.replace('"', '').replace('(', '')) * 52)
            routes.append((x, y))

    img = plt.imread('image.png')
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(plticker.MultipleLocator(base=52))
    ax.yaxis.set_major_locator(plticker.MultipleLocator(base=52))

    ax.grid(which='major', axis='both')
    ax.imshow(img)
    for n in routes:
        ax.scatter(*n, color='y', )
        ax.set_xticklabels(range(-1, 18))
        ax.set_yticklabels(range(-1, 18))
    plt.show()

