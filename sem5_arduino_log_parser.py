import matplotlib.pyplot as plt
import numpy as np
import pandas

FILE_NAME = 'log.txt'

# file format:
# YYYY-MM-DD HH temp hum
# delta = 1h

dates = []
mean_temp = []
mean_hum = []


file = open(FILE_NAME, 'r')
attr = [line.split(' ') for line in file]

# for elem in attr:

first_date = attr[0][0]
while attr and attr[0][0] == first_date:
    attr.pop(0)

last_date = attr[-1][0]
while attr and attr[-1][0] == last_date:
    del attr[-1]

for line in attr:
    line[3] = line[3][:-1]

for j in range(0, len(attr), 3):
    dates.append(attr[j][0])
    mean_hum.append(sum(float(attr[j+i][3]) for i in range(3))/3)
    mean_temp.append(sum(float(attr[j+i][2]) for i in range(3))/3)

print(dates)
print(mean_temp)
print(mean_hum)

x = np.array(dates)
# y = np.array(mean_temp)
fig, ax = plt.subplots()
ax.plot(x, np.array(mean_temp))
ax.plot(x, np.array(mean_hum))
plt.savefig('test.png')
