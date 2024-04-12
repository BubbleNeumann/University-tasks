import qlearning as ql
import utils
import time


def main():
    qtable = ql.read_qtable()
    # qtable = ql.init_qtable()
    if qtable is None:
        qtable = ql.init_qtable()

    bg_matrix = ql.compose_bg_matrix()
    starting_pos = utils.get_char_pos(utils.get_screen_capture())
    ql.qlearning_loop(qtable, bg_matrix, starting_pos)


if __name__ == '__main__':
    time.sleep(1)  # time to switch to the game window
    main()
