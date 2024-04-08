import utils
import qlearning
import numpy as np


if __name__ == '__main__':

    bg_matrix = np.zeros((10, 18))
    bg_matrix[:, 0] = 1
    bg_matrix[:, 1] = 2
    bg_matrix[:, -1] = 3
    qtable = qlearning.compose_qtable_from_bg_matrix(bg_matrix.copy())

    print(qtable)
    bg_matrix_new = qlearning.displ_qtable_as_bg_matrix(qtable)
    print(bg_matrix_new)
