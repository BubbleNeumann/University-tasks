import qlearning as ql
import utils
import keyboard
import time


def main():

    # init qtable for the entire action space
    # action_space = ['space', 'd+x', 'z+w', 'd', 'a', 'a+x']
    action_space = ['a+space', 'a+x', 'z+w', 'a']
    # action_space = ['space+d', 'd+x', 'z+w']

    # print('INITIALIZING')
    qtable = ql.init_qtable(action_space)
    # qtable = ql.read_qtable()
    # starting_pos = utils.get_char_pos(utils.get_screen_capture())
    # ql.qlearning_loop(action_space, qtable,  starting_pos, num_episodes=1)
    # ql.no_eps_qlearning(qtable, action_space, starting_pos, num_episodes=1)
    # print(action_space[:3])

    for i in range(4, len(action_space)+1):
        # qtable = ql.normalize_qtable(ql.read_qtable())
        print(action_space[:i])
        starting_pos = utils.get_char_pos(utils.get_screen_capture())
        # ql.no_eps_qlearning(qtable, action_space[:i], starting_pos)
        ql.qlearning_loop(action_space[:i], qtable,  starting_pos)
        utils.restart()
        time.sleep(3)


if __name__ == '__main__':
    time.sleep(1)  # time to switch to the game window
    keyboard.press('space')
    time.sleep(1)
    keyboard.release('space')
    time.sleep(1)
    main()
