import numpy as np
import random
import utils
import time
import csv


action_space = ['a', 'd', 'space', 'a+x', 'd+x', 'z+w']

# qlearning globals
eps = 1  # exploration rate
eps_decay_rate = 0.01  # delta between episodes
num_episodes = 1000
max_steps_per_episode = 50
learning_rate = 0.1  # alpha
discount_rate = 0.99  # gamma

DEFAULT_DIMS = (10, 18)  # (rows, cols)


def compose_bg_matrix(dims=DEFAULT_DIMS):
    return np.zeros(shape=dims)


def init_qtable(dims=DEFAULT_DIMS) -> np.ndarray:
    return np.zeros((len(action_space), np.multiply(*dims)))


def displ_qtable_as_bg_matrix(
        qtable: np.ndarray, dims=DEFAULT_DIMS) -> np.ndarray:
    return sum(np.reshape(row, dims) for row in qtable) / len(action_space) * np.ones(dims)


def compose_qtable_from_bg_matrix(
        bg_matrix: np.ndarray, dims=DEFAULT_DIMS) -> np.ndarray:
    res = np.ndarray(shape=(len(action_space), np.multiply(*dims)))
    for i in range(len(action_space)):
        res[i] = bg_matrix.flatten()
    return res


def save_qtable(qtable, file_path='qtable.csv'):
    with open(file_path, 'w') as f:
        csv.writer(f, delimiter=';').writerows(np.round(qtable, 3))


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

    row = cur_pos[0]
    col = cur_pos[1]

    actions_for_cur_state = qtable[:, row * dims[0] + col]
    print(actions_for_cur_state)

    if random.random() > eps:
        if isinstance(actions_for_cur_state, list):
            action_ind = actions_for_cur_state.index(max(actions_for_cur_state))
        else:
            action_ind = actions_for_cur_state.tolist().index(max(actions_for_cur_state))
    else:
        action_ind = random.randint(0, len(actions_for_cur_state) - 1)
    print(action_space[int(action_ind)], action_ind)
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

    # Bellman equation:
    qtable[state][action] = qtable[state][action] + learning_rate * (reward + discount_rate * np.max(qtable[new_state]))
    return qtable


def qlearning_loop(qtable: np.ndarray, bg_matrix, dims=DEFAULT_DIMS):

    global eps, cur_pos, new_pos, route, eps_decay_rate

    for episode in range(num_episodes):
        print(f'ep {episode}')

        route = []  # allows to track actions taken in the current run
        # prev_coord_delta = [0] * 5  # remember 5 prev coordinate changes
        for step in range(max_steps_per_episode):

            # make char pos relative to bg matrix
            cur_pos = cur_pos[0]//dims[0], cur_pos[1]//dims[1]

            action_ind = act(qtable, cur_pos)  # take new action
            route.append([cur_pos, action_ind])
            new_pos = utils.get_char_pos(bg_matrix)

            # if char not found => update qtable manually, reset env
            if new_pos == (-1, -1):
                print('char not found')
                qtable[:, (cur_pos[0] * dims[0] + cur_pos[1])] -= 1
                save_qtable(qtable)
                break

            # make char pos relative to bg matrix
            new_pos = (new_pos[0]//dims[0], new_pos[1]//dims[1])

            print(new_pos)
            # TODO rewrite is_done check
            # if image_matrix[new_pos[0]][new_pos[1]] == 2:  # check if done
            #     save_qtable(qtable)
            #     return
            qtable = update_qtable(
                    qtable=qtable,
                    action=action_ind,
                    state=cur_pos,
                    new_state=new_pos,
                    reward=bg_matrix[new_pos],
                    )
            # print(route)
            cur_pos = new_pos

        # here goes the end of episode
        if episode % 5 == 0:
            # TODO save qtable in separate execution thread (import threading)
            save_qtable(qtable)
            print('qtable saved')
        eps = 0.01 + 0.99 * np.exp(-eps_decay_rate * episode)
        print(f'eps = {eps}')
        utils.restart()
        # save route
        # with open(f'route{episode}.csv', 'a') as f:
        #     csv.writer(f).writerows(route)

        time.sleep(3)
