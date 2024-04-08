import qlearning


def main():
    qtable = qlearning.read_qtable()
    if qtable is None:
        qtable = qlearning.init_qtable()
    qlearning.qlearning_loop(qtable)


if __name__ == '__main__':
    main()
