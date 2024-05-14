import utils
import qlearning as ql
import numpy as np
import time
import os
import matplotlib.pyplot as plt


if __name__ == '__main__':
    # time.sleep(2)  # time to switch to the game window
    # action_space = ['space', 'd+x', 'z+w', 'd', 'a', 'a+x']
    # print(action_space[:3])
    # qtable = ql.read_qtable()
    # starting_pos = utils.get_char_pos(utils.get_screen_capture())
    # ql.demo(qtable,  action_space[:3], starting_pos)
    # qtable = ql.read_qtable()
    # qtable = ql.normalize_qtable(qtable)
    # ql.save_qtable(qtable)
    # starting_pos = utils.get_char_pos(utils.get_screen_capture())
    # ql.demo(qtable, starting_pos)
    # utils.visualize_progress()
    utils.visualize_progress('2024-05-0619:06:03_ep386_las4.csv')
    # bg = utils.get_screen_capture()
    # utils.get_char_pos_with_debug(bg, show_pic=True)
    # utils.get_screen_capture_with_debug()
    # qtable = ql.init_qtable()
    # print(qtable)
    # route = []
    # with open(f'successroutes/2024-04-3014:05:01_ep8_las4.csv', 'r') as f:
    #     for line in f.readlines():
    #         col, row, action = line.split(',')
    #         route.append((None, int(action)))
    #
    # # print(route)
    # time.sleep(2)
    # img = plt.imread('image.png')
    # y = [33.1,98.2,504.1,6010]
    #
    # x = range(3,7)
    # fig, ax = plt.subplots()
    # ax.scatter(x, y)
    #
    # import math
    # x = [x / 10.0 for x in range(3, 70, 1)]
    # ax.set_ylim([-200, 10000])
    # ax.plot(x, [math.exp(i*1.4) for i in x], linestyle='--', color='r')
    # plt.ylabel('Среднее количество итераций обучения')
    # plt.xlabel('Размерность пространства состояний')
    # plt.show()


    # ax.xaxis.set_major_locator(plticker.MultipleLocator(base=52))
    # ax.yaxis.set_major_locator(plticker.MultipleLocator(base=52))

    # ax.grid(which='major', axis='both')
    # ax.imshow(img)
    # for n in routes:
    #     ax.scatter(*n, color='y', )
    #     ax.set_xticklabels(range(-1, 18))
    #     ax.set_yticklabels(range(-1, 18))
    # plt.show()
    # utils.demo(route)
