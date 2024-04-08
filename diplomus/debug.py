import utils
import qlearning


if __name__ == '__main__':
    qtable = qlearning.init_qtable()
    qtable[:, 1] = 1
    print(qtable)
    print(qlearning.displ_qtable_as_bg_matrix(qtable))
