import matplotlib.pyplot as plt

n_proc = [950, 1900, 3800]

seq = [8.99, 53.26750, 462.27583]
gpu = [0.03997, 0.06608, 0.23972]
cpu = [0.06608, 0.19329, 0.77432]


plt.figure(figsize=(8, 5), dpi=80)
p1, = plt.plot(n_proc, gpu, label='gpu', marker='o')
p2, = plt.plot(n_proc, cpu, label='cpu', marker='o')
plt.ylabel('time (sec)')
plt.xlabel('n_proc')
plt.legend(handles=[p1, p2])
plt.savefig('pic2.jpg')


acc_gpu = [round(a / b, 6) for a, b in zip(seq, gpu)]
acc_cpu = [round(a / b, 6) for a, b in zip(seq, cpu)]

plt.figure(figsize=(8, 5), dpi=80)
p1, = plt.plot(n_proc, acc_gpu, label='gpu', marker='o')
p2, = plt.plot(n_proc, acc_cpu, label='cpu', marker='o')
plt.ylabel('acc.')
plt.xlabel('n_proc')
plt.legend(handles=[p1, p2])
plt.savefig('pic3.jpg')

print(acc_gpu)
print(acc_cpu)
