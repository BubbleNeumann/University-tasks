import numpy as np


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


def displ_qtable_as_bg_matrix(qtable: np.ndarray, dims=DEFAULT_DIMS) -> np.ndarray:
    # return qtable[0].re
    # qtable[0].re
    return sum(np.reshape(row, dims) for row in qtable) / len(action_space) * np.ones(dims)


def qlearning_loop():
    pass
