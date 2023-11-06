from typing import Tuple
import mss.tools
import cv2 as cv
import numpy as np
import keyboard
import random
import time


CHAR_DIMS = (24, 27)
CHAR_DIMS_CROUCH = (24, 12)
COMPRESS_COEFF = 3

cur_pos = (-1, -1)
new_pos = (-1, -1)

# environment globals
bounding_box = {'top': 40, 'left': 0, 'width': 955, 'height': 535}
template = cv.imread('char.png', cv.IMREAD_COLOR)
sct = mss.mss()
sct_img = sct.grab(bounding_box)  # screen capture
pixels = np.array(sct_img)
pixels = cv.cvtColor(pixels, cv.COLOR_RGB2BGR)

action_space = ['a', 'w', 'd', 's', 'space', 'shift', 'shift+w', 'shift+space', 'z', 'z+w']

# qlearning globals
eps = 1 # exploration rate
eps_decay_rate = 0.01 # delta between episodes
num_episodes = 1000
max_steps_per_episode = 200
learning_rate = 0.1 # alpha
discount_rate = 0.99 # gamma

rewards_all_episodes = []


def get_char_pos() -> Tuple[int, int]:
    """
    :return: maxloc // COMPRESS_COEFF
    """
    res = cv.matchTemplate(pixels, template, 2)
    coords = cv.minMaxLoc(res)[3]
    return coords[0] // COMPRESS_COEFF, coords[1] // COMPRESS_COEFF

def compose_bg_matrix(img):
    def set_border_rewards(matrix: list):
        REW_BORDER_WIDTH = 5 # since width of the collider is always greater than 5
        for y in range(REW_BORDER_WIDTH):
            for x in range(len(matrix[0])):
                matrix[y][x] = 2
        for y in range(len(matrix)-REW_BORDER_WIDTH, len(matrix)):
            for x in range(len(matrix[0])):
                matrix[y][x] = 2
        for y in range(len(matrix)):
            for x in range(REW_BORDER_WIDTH):
                matrix[y][x] = 2
        for y in range(len(matrix)):
            for x in range(len(matrix[0])-REW_BORDER_WIDTH, len(matrix[0])):
                matrix[y][x] = 2
        return matrix
        
    bg1 = []
    for y in range(bounding_box['height']//COMPRESS_COEFF):
        col_bg = []
        for x in range(bounding_box['width']//COMPRESS_COEFF):
            if img[y][x][0] == img[y][x][1] and img[y][x][1] == img[y][x][2]:
                col_bg.append(1) # for rewards: empty space
            else:
                col_bg.append(0) # obstacle
        bg1.append(col_bg)
    return set_border_rewards(bg1)


def init_qtable(matrix):
    return [[0]  * len(action_space)] * len(matrix) * len(matrix[0])

def move(key: str):
    keyboard.press(key)
    time.sleep(1)
    keyboard.release(key)

def check_if_done() -> bool:
    # if  
    return False

def act(qtable, cur_pos) -> int:
    """
    :return: 
    """
    buffer = []
    x = cur_pos[0]
    y = cur_pos[1]
    print(cur_pos)
    actions_for_cur_state = qtable[y * bounding_box['width']//COMPRESS_COEFF + x]
    print(actions_for_cur_state, len(actions_for_cur_state))
    if random.random() > eps:
        action_ind = actions_for_cur_state.index(max(actions_for_cur_state))
    else:
        action_ind = random.randint(0, len(actions_for_cur_state) - 1)
    print(action_space[int(action_ind)], action_ind)
    move(action_space[int(action_ind)])
    return int(action_ind)

def update_qtable(qtable, action: int, state: int, reward: int, new_state: int):
    """
    !! qtable might be rotated

    :param action: action index in action space;
    state = cur_pos (considering bg matrix is constant)
    reward = from bg matrix
    new_state = updated character state
    """
    qtable[state][action] = qtable[state][action] * (1 - learning_rate) + \
            learning_rate * (reward + discount_rate * np.max(qtable[new_state]))
    return qtable

def qlearning_loop(qtable, image_matrix):
    global eps, cur_pos, new_pos
    for episode in range(num_episodes):
        # init new episode params
        # update bg matrix
        # done = False
        # ??? reward_curr_episode = 0
        for _ in range(max_steps_per_episode):
            # take new action
            action_ind = act(qtable, cur_pos)
            new_pos = get_char_pos()
            print(new_pos)
            # update q-table
            qtable = update_qtable(
                    qtable=qtable,
                    action=action_ind,
                    state=cur_pos[1] * bounding_box['width']//COMPRESS_COEFF + cur_pos[0],
                    new_state=new_pos[1] * bounding_box['width']//COMPRESS_COEFF + new_pos[0],
                    reward=image_matrix[new_pos[0]][new_pos[1]]
                )
            cur_pos = new_pos
            # set new state: state = env.reset() / compose_bg_matrix()
            # add new reward
        eps = 0.01 + 0.99 * np.exp(-eps_decay_rate*episode)


def main():
    time.sleep(5)
    global cur_pos
    newimg2=cv.resize(pixels,(955//COMPRESS_COEFF,535//COMPRESS_COEFF),interpolation=cv.INTER_NEAREST)
    image_matrix = compose_bg_matrix(newimg2)

    qtable = []

    with open('qtable_save.txt') as f:
        for line in f.readlines():
            qtable.append(line.split(';'))

    if len(qtable) == 0:
        qtable = init_qtable(matrix=image_matrix)
    print(len(qtable), len(qtable[0]))
    cur_pos = get_char_pos()
    qlearning_loop(qtable, image_matrix)


if __name__ == "__main__":
    main()
