import qlearning as ql
import utils
import keyboard
import time


def main():
    qtable = ql.read_qtable()
    # qtable = ql.init_qtable()
    # if qtable is None:
    #     qtable = ql.init_qtable()

    starting_pos = utils.get_char_pos(utils.get_screen_capture())
    ql.qlearning_loop(qtable,  starting_pos)


if __name__ == '__main__':
    time.sleep(1)  # time to switch to the game window
    keyboard.press('space')
    time.sleep(1)
    keyboard.release('space')
    main()
