from datetime import date, datetime

import numpy as np
import random
import utils
import time
import csv


# action_space = ['a', 'd', 'space', 'a+x', 'd+x', 'z+w']
action_space = ['space', 'd+x', 'z+w']

# qlearning globals
eps = 0.6  # exploration rate
eps_decay_rate = 0.01  # delta between episodes
num_episodes = 1000
max_steps_per_episode = 50  # owtherwise it becomes pointless
learning_rate = 0.2  # alpha
discount_rate = 0.9  # gamma

# DEFAULT_DIMS = (10, 18)  # (rows, cols)
DEFAULT_DIMS = (18, 10)  # (cols, rows) = (x, y)
exit_row = 0
exit_col = 17


def init_qtable(dims=DEFAULT_DIMS) -> np.ndarray:
    return np.zeros((len(action_space), np.multiply(*dims)))


def save_qtable(qtable, file_path='qtable.csv'):
    with open(file_path, 'w') as f:
        csv.writer(f, delimiter=';').writerows(np.round(qtable, 3))
    print('qtable saved')


def read_qtable(file_path='qtable.csv') -> np.ndarray | None:
    try:
        with open(file_path, 'r') as f:
            return np.genfromtxt(f, delimiter=';')
    except FileNotFoundError:
        return None


def act(qtable, dims, cur_pos: tuple[int, int]) -> int:
    """
    :param cur_pos: character pos relative to bg matrix
    :return: index of the taken action
    """

    global eps

    row = cur_pos[1]
    col = cur_pos[0]

    assert row >= 0 and row < dims[1] and col >= 0 and col < dims[0]

    actions_for_cur_state = qtable[:, row * dims[1] + col]
    # allows to cut 'bad' actions on random iterations
    # actions_for_cur_state = list(filter(lambda e: e >= 0, qtable[:, row * dims[1] + col]))
    # actions_for_cur_state = qtable[:, row * dims[1] + col] if not actions_for_cur_state else actions_for_cur_state
    print(actions_for_cur_state)

    if random.random() > eps:
        if isinstance(actions_for_cur_state, list):
            action_ind = actions_for_cur_state.index(max(actions_for_cur_state))
        else:
            action_ind = actions_for_cur_state.tolist().index(max(actions_for_cur_state))
    else:
        action_ind = random.randrange(len(actions_for_cur_state))

    print(action_space[int(action_ind)], action_ind)

    # perform the actual movement
    utils.press_key(action_space[int(action_ind)])
    return int(action_ind)


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

    # normalize to avoid int overflow into 'inf'
    # return qtable / (np.ones(qtable.shape) * max([np.max(qtable), 1]))
    return qtable


def is_done(cur_pos: tuple[int, int]) -> bool:
    terminate_pos = [(0, 15), (0, 16), (0, 17)]
    return cur_pos in terminate_pos


def calc_reward(is_dead: bool, cur_pos: tuple[int, int], new_pos: tuple[int, int]) -> int:
    # wheather or not the character is getting closer to the exit
    progress = abs(exit_col - cur_pos[0]) > abs(exit_col - new_pos[0]) \
            or abs(exit_row - cur_pos[1]) > abs(exit_row - new_pos[1])
    return 1 if not is_dead and progress else -2


def qlearning_loop(
        qtable: np.ndarray,
        starting_pos: tuple[int, int],
        dims=DEFAULT_DIMS
        ) -> None:
    """
    Main logic of the qlearning.
    TODO: extract logging logic?
    :param starting_pos: charater pos captured before starting the loop
    :param dims: bg matrix dims
    """
    from utils import bounding_box_default as bb

    global eps, eps_decay_rate, num_episodes, max_steps_per_episode

    h_block = bb['height'] // dims[1]
    w_block = bb['width'] // dims[0]
    print(w_block, h_block)

    cur_pos = (starting_pos[0] // h_block, starting_pos[1] // w_block)

    for episode in range(num_episodes):
        print(f'ep {episode}')

        route = []  # allows to track actions taken in the current run
        for step in range(max_steps_per_episode):

            print(cur_pos)
            action_ind = act(qtable, dims, cur_pos)  # take new action

            # get the updated state of the environment
            bg_pixels = utils.get_screen_capture()
            new_pos = utils.get_char_pos(bg_pixels)
            route.append([cur_pos, action_ind])

            print(f'new_pos before cast: {new_pos}')
            # make char pos relative to bg matrix
            new_pos = (new_pos[0] // h_block, new_pos[1] // w_block)
            print(f'new_pos after cast: {new_pos}')

            if is_done(new_pos):
                print('OMG!!')
                save_qtable(qtable)
                return

            is_dead = new_pos == (-1, -1)

            qtable = update_qtable(
                    qtable=qtable,
                    action=action_ind,
                    state=cur_pos[1] * dims[1] + cur_pos[0],
                    # new_state=new_pos[0] * dims[1] + new_pos[1],
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

        eps = 0.01 + 0.99 * np.exp(-eps_decay_rate * episode)

        print(f'eps = {eps}')
        utils.restart()

        # save route
        time_n = datetime.now().strftime('%H:%M:%S')
        with open(f'routes/{date.today()}{time_n}_ep{episode}.csv', 'a') as f:
            csv.writer(f).writerows(route)

        time.sleep(2)
