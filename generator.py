import itertools
import random

FILE_NAME = 'test.txt'

with open(FILE_NAME, 'w') as file:
    days = 15
    start_day = 5

    for day_n, hour in itertools.product(range(days), range(24)):
        file.write(
            # f'2022-12-{start_day+day_n} {hour} {random.uniform(20.3, 24.0)}\n')
            f'2022-12-{start_day+day_n} {hour} {"{:.1f}".format(random.uniform(20.3, 24.0))} {"{:.1f}".format(random.uniform(30.3, 42.0))}\n')
