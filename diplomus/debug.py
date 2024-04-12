import utils
import qlearning as ql
import numpy as np
import time


if __name__ == '__main__':
    qtable = ql.init_qtable()
    bg_matrix = ql.compose_bg_matrix()
    # bg_pixels = utils.get_screen_capture()
    # starting_pos = utils.get_char_pos(bg_pixels)
    # qtable = ql.compose_qtable_from_bg_matrix(bg_matrix)
    # time.sleep(2)
    # utils.press_key('space', 1)
    # time.sleep(1)
    #
    # print('start')
    # ql.qlearning_loop(qtable, bg_matrix, starting_pos)

    # qtable = ql.read_qtable()
    # bg = ql.displ_qtable_as_bg_matrix(qtable)
    # bg = ql.compose_bg_matrix()
    # np.set_printoptions(threshold=np.inf, linewidth=np.inf, precision=1)
    # print(qtable)
