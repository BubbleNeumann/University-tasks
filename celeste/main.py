import mss.tools
import cv2 as cv
import numpy as np
# from PIL import Image
import keyboard
# import pandas as pd
import random
import time


CHAR_DIMS = (24, 27)
CHAR_DIMS_CROUCH = (24, 12)
COMPRESS_COEFF = 3

cur_pos = new_pos = (-1, -1)

# environment globals
bounding_box = {'top': 40, 'left': 0, 'width': 955, 'height': 535}
template = cv.imread('char.png', cv.IMREAD_COLOR)
sct = mss.mss()
sct_img = sct.grab(bounding_box)  # screen capture
pixels = np.array(sct_img)
pixels = cv.cvtColor(pixels, cv.COLOR_RGB2BGR)

action_space = ['', 'd']

# qlearning globals
eps = 1 # exploration rate
eps_decay_rate = 0.01 # delta between episodes
num_episodes = 1000
max_steps_per_episode = 200
learning_rate = 0.1 # alpha
discount_rate = 0.99 # gamma


rewards_all_episodes = []


def get_char_pos():
    res = cv.matchTemplate(pixels, template, 2)
    return cv.minMaxLoc(res)[3]  # return maxloc

def compose_bg_matrix(img):
    bg1 = []
    for y in range(bounding_box['height']):
        col_bg = []
        for x in range(bounding_box['width']):
            if img[y][x][0] == img[y][x][1] and img[y][x][1] == img[y][x][2]:
                col_bg.append(1) # for rewards: empty space
            else:
                col_bg.append(0) # obstacle
        bg1.append(col_bg)
    # TODO manually find exit poing from the level
    # set reward in the exit area = 2
    return bg1


def init_qtable(matrix):
    return [[1] * len(matrix) * len(matrix[0])] * len(action_space)

def move(key: str):
    keyboard.press(key)
    time.sleep(1)
    keyboard.release(key)

def check_if_done() -> bool:
    # if  
    return False

def act(qtable, cur_pos) -> tuple:
    buffer = []
    x = cur_pos[0]
    y = cur_pos[1]
    actions_for_cur_state = qtable[y * bounding_box['width']//COMPRESS_COEFF + x]

    if random.random() > eps:
        action_ind = actions_for_cur_state.index(max(actions_for_cur_state))
    else:
        action_ind = actions_for_cur_state[random.randint(0, len(actions_for_cur_state))]

    move(action_space[action_ind])
    return (action_ind, )

def update_qtable(qtable, action: int, state: tuple, reward: int, new_state: tuple):
    """
    !! qtable might be rotated

    :param action: action index in action space;
    state = cur_pos (considering bg matrix is constant)
    reward = from bg matrix
    new_state = updated character state
    """
    qtable[state, action] = qtable[state, action] * (1 - learning_rate) + \
            learning_rate * (reward + discount_rate * np.max(qtable[new_state, :]))
    return qtable

def qlearning_loop(qtable):
    for episode in range(num_episodes):
        # init new episode params
        # update bg matrix
        # done = False
        # ??? reward_curr_episode = 0
        for step in range(max_steps_per_episode):
            # take new action
            act(qtable, cur_pos)
            # update q-table
            # qtable = update_qtable(qtable, )
            # set new state: state = env.reset() / compose_bg_matrix()
            # add new reward
        eps = 0.01 + 0.99 * np.exp(-eps_decay_rate*episode)


def main():
    newimg2=cv.resize(pixels,(955//COMPRESS_COEFF,535//COMPRESS_COEFF),interpolation=cv.INTER_NEAREST)
    image_matrix = compose_bg_matrix(newimg2)
    qtable = init_qtable(image_matrix)
    act(qtable, get_char_pos())


if __name__ == "__main__":
    main()
