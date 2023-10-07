with open('input.txt', 'r') as inp:
    lines = inp.readlines()
    x_train_set = []
    y_train_set = []
    test_set = []

    for line in lines[1:]:
        line_list = line.split(',')
        if line_list[-1] == 'train\n':
            if line_list[-2] == '0':
                x_train_set.append(line_list[:-2])
            else:
                y_train_set.append(line_list[:-2])
        else:
            test_set.append(line_list[:-1])
        break

# --- train ---

losses_train = []
losses_test = []


