import mss.tools
import cv2 as cv
import numpy as np
from PIL import Image
import keyboard
import pandas as pd
import random
import time


CHAR_DIMS = (24, 27)
CHAR_DIMS_CROUCH = (24, 12)
COMPRESS_COEFF = 3

cur_pos = new_pos = (-1, -1)

bounding_box = {'top': 40, 'left': 0, 'width': 955, 'height': 535}
template = cv.imread('char.png', cv.IMREAD_COLOR)
sct = mss.mss()
sct_img = sct.grab(bounding_box)  # screen capture
pixels = np.array(sct_img)
pixels = cv.cvtColor(pixels, cv.COLOR_RGB2BGR)

eps = 1

action_space = ['', 'd']

def get_char_pos():
    res = cv.matchTemplate(pixels, template, 2)
    return cv.minMaxLoc(res)[3]  # return maxloc

def compose_bg_matrix(img):
    bg1 = []
    for y in range(bounding_box['height']):
        col_bg = []
        for x in range(bounding_box['width']):
            if img[y][x][0] == img[y][x][1] and img[y][x][1] == img[y][x][2]:
                col_bg.append(0)
            else:
                col_bg.append(1)
        bg1.append(col_bg)
    return bg1


def init_qtable(matrix):
    return [[1] * len(matrix) * len(matrix[0])] * len(action_space)

def move(key: str):
    keyboard.press(key)
    time.sleep(1)
    keyboard.release(key)

def act(qtable, cur_pos):
    buffer = []
    x = cur_pos[0]
    y = cur_pos[1]
    actions_for_cur_state = qtable[y * bounding_box['width']//COMPRESS_COEFF + x]

    if random.random() > eps:
        action_ind = actions_for_cur_state.index(max(actions_for_cur_state))
    else:
        action_ind = actions_for_cur_state[random.randint(0, len(actions_for_cur_state))]

    move(action_space[action_ind])


def main():
    newimg2=cv.resize(pixels,(955//COMPRESS_COEFF,535//COMPRESS_COEFF),interpolation=cv.INTER_NEAREST)
    image_matrix = compose_bg_matrix(newimg2)
    qtable = init_qtable(image_matrix)
    act(qtable, get_char_pos())


if __name__ == "__main__":
    main()
