from datetime import date, datetime

import numpy as np
import random
import utils
import time
import csv


# action_space = ['a', 'd', 'space', 'a+x', 'd+x', 'z+w']
# action_space = ['space', 'd+x', 'z+w']
# action_space = ['space', 'd+x', 'z+w', 'd']

# qlearning globals
eps = 1  # exploration rate
eps_decay_rate = 0.001  # delta between episodes
# num_episodes = 10000
max_steps_per_episode = 100  # owtherwise it becomes pointless
learning_rate = 0.2  # alpha
discount_rate = 0.9 # gamma

DEFAULT_DIMS = (18, 10)  # (cols, rows) = (x, y)
# exit_row = 0
# exit_col = 16


def init_qtable(action_space, dims=DEFAULT_DIMS) -> np.ndarray:
    return np.zeros((len(action_space), np.multiply(*dims)))


def save_qtable(qtable, file_path='qtable.csv'):
    with open(file_path, 'w') as f:
        csv.writer(f, delimiter=';').writerows(np.round(qtable, 3))
    # print('qtable saved')


def read_qtable(file_path='qtable.csv') -> np.ndarray | None:
    try:
        with open(file_path, 'r') as f:
            return np.genfromtxt(f, delimiter=';')
    except FileNotFoundError:
        return None


def act(qtable, dims, cur_pos: tuple[int, int], action_space, previous_action: int = None) -> tuple[int, bool]:
    """
    :param cur_pos: character pos relative to bg matrix
    :return: index of the taken action and whether or not the random action was taken
    """

    global eps

    row = cur_pos[1]
    col = cur_pos[0]

    assert row >= 0 and row < dims[1] and col >= 0 and col < dims[0]

    actions_for_cur_state = qtable[:, row * dims[1] + col]
    actions_for_cur_state = actions_for_cur_state[:len(action_space)]

    if random.random() > eps:
        rand = False
        action_ind = actions_for_cur_state.tolist().index(max(actions_for_cur_state))
    else:
        rand = True
        action_ind = random.randrange(len(actions_for_cur_state))

    # perform the actual movement
    utils.press_key(action_space[int(action_ind)])
    return int(action_ind), rand


def normalize_qtable(qtable):
    """
    Normalizes each column independently, keeps the proportions for each state.
    Helps to avoid overflow into 'inf'.
    """
    # Find the maximum element for each column
    max_values = np.max(qtable, axis=0)

    # Avoid division for the small values
    max_values[max_values < 100] = 1

    # Normalize each column independently
    normalized_matrix = qtable / max_values
    return normalized_matrix

#
def update_qtable(qtable, action: int, state: int, reward: int, new_state: int):
    """
    :param new_state: updated character state
    :param reward: from bg matrix
    :param state: cur_pos (considering bg matrix is constant)
    :param qtable:
    :param action: action index in action space;
    """
    global learning_rate, discount_rate

    print(f'action: {action}, state: {state}, reward: {reward}, new_state: {new_state}')

    # Bellman equation:
    qtable[action, state] = qtable[action, state] + learning_rate * (reward + discount_rate * np.max(qtable[:, new_state]))

    return qtable


def is_done(cur_pos: tuple[int, int]) -> bool:
    # terminate_pos = [(15, 0), (16, 0), (17, 0)]
    terminate_pos = [(0, 5), (1, 5)]
    return cur_pos in terminate_pos


def calc_reward(
        is_dead: bool,
        cur_pos: tuple[int, int],
        new_pos: tuple[int, int]
        ) -> int:

    diff_y = new_pos[1] - cur_pos[1]  # should be negative
    diff_x = new_pos[0] - cur_pos[0]  # should be positive

    # progress = diff_x - diff_y
    progress = - diff_x
    # print(diff_rows, diff_cols, progress)
    # print(diff_rows)

    if progress != 0 and not is_dead:
        rew = progress
    else:
        rew = -1
    return rew
    # progress = abs(exit_col - cur_pos[0]) > abs(exit_col - new_pos[0]) \
    #         or abs(exit_row - cur_pos[1]) > abs(exit_row - new_pos[1])
    # return 1 if not is_dead and progress else -2


def qlearning_loop(
        action_space: list[str],
        qtable: np.ndarray,
        starting_pos: tuple[int, int],
        dims=DEFAULT_DIMS,
        num_episodes=10000,
        ) -> None:
    """
    Main logic of the qlearning.
    TODO: extract logging logic?
    :param starting_pos: charater pos captured before starting the loop
    :param dims: bg matrix dims
    """
    from utils import bounding_box_default as bb

    # global eps, eps_decay_rate, num_episodes, max_steps_per_episode
    global eps, eps_decay_rate, max_steps_per_episode

    h_block = bb['height'] // dims[1]
    w_block = bb['width'] // dims[0]
    # print(w_block, h_block)

    cur_pos = (starting_pos[0] // h_block, starting_pos[1] // w_block)

    prev_action = None

    for episode in range(num_episodes):
        print(f'ep {episode}')

        route = []  # allows to track actions taken in the current run
        for step in range(max_steps_per_episode):

            # print(cur_pos)
            # take new action
            action_ind, rand = act(qtable, dims, cur_pos, action_space, prev_action)

            # DEBUG Logging
            if not rand:
                utils.logging(cur_pos, action_ind, qtable)

            prev_action = action_ind

            # get the updated state of the environment
            bg_pixels = utils.get_screen_capture()
            new_pos = utils.get_char_pos(bg_pixels)
            route.append([cur_pos, action_ind])

            # print(f'new_pos before cast: {new_pos}')
            # make char pos relative to bg matrix
            new_pos = (new_pos[0] // h_block, new_pos[1] // w_block)

            if is_done(new_pos):
                print('OMG!!')
                save_qtable(qtable)

                # save route
                time_n = datetime.now().strftime('%H:%M:%S')
                with open(f'routes/{date.today()}{time_n}_ep{episode}_las{len(action_space)}.csv', 'a') as f:
                    csv.writer(f).writerows(route)
                with open(f'successroutes/{date.today()}{time_n}_ep{episode}_las{len(action_space)}.csv', 'a') as f:
                    csv.writer(f).writerows(route)
                return

            is_dead = new_pos == (-1, -1)

            qtable = update_qtable(
                    qtable=qtable,
                    action=action_ind,
                    state=cur_pos[1] * dims[1] + cur_pos[0],
                    new_state=new_pos[1] * dims[1] + new_pos[0],
                    reward=calc_reward(is_dead, cur_pos, new_pos),
                    )

            if is_dead:
                print('dead')
                break

            cur_pos = new_pos

        # here goes the end of episode:
        # only happends when steps limit is reached or character is dead
        if episode % 5 == 0:
            save_qtable(qtable)

        if episode % 10 == 0:
            print('normalizing qtable')
            qtable = normalize_qtable(qtable)

        eps = 0.01 + 0.99 * np.exp(-eps_decay_rate * episode)

        print(f'eps = {eps}')
        # utils.restart()

        # save route
        time_n = datetime.now().strftime('%H:%M:%S')
        with open(f'routes/{date.today()}{time_n}_ep{episode}_las{len(action_space)}.csv', 'a') as f:
            csv.writer(f).writerows(route)

        time.sleep(2)
