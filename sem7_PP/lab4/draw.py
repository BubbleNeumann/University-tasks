import matplotlib.pyplot as plt

N = 4500000
n_vector_dims = [N, N//10, N//15]


_2048_512 = [0.000737,0.0001500,0.000127]
_512_512 = [0.000688,0.000097,0.000076]
_2048_128 = [0.000692,0.000100,0.000077]
_512_128 = [0.000701,0.000089,0.000065]
_2048_32 = [0.001633,0.000186,0.000133]
_512_32 = [0.001710,0.000186,0.000130]

#
# plt.figure(figsize=(8, 5), dpi=80)
# p1, = plt.plot(n_vector_dims, _2048_512, label='2048_512', marker='o')
# p2, = plt.plot(n_vector_dims, _512_512, label='512_512', marker='o')
# p3, = plt.plot(n_vector_dims, _2048_128, label='2048_128', marker='o')
# p4, = plt.plot(n_vector_dims, _512_128, label='512_128', marker='o')
# p5, = plt.plot(n_vector_dims, _2048_32, label='2048_32', marker='o')
# p6, = plt.plot(n_vector_dims, _512_32, label='512_32', marker='o')
# plt.ylabel('time (sec)')
# plt.xlabel('n_vector_dims')
# plt.legend(handles=[p1, p2, p3, p4, p5, p6])
# plt.savefig('pic2.jpg')


non_parallel_time = [0.014167,0.000833,0.000833]


acc_2048_512 = [round(a / b, 6) for a, b in zip(non_parallel_time, _2048_512)]
acc_512_512 = [round(a / b, 6) for a, b in zip(non_parallel_time, _512_512)]
acc_2048_128 = [round(a / b, 6) for a, b in zip(non_parallel_time, _2048_128)]
acc_512_128 = [round(a / b, 6) for a, b in zip(non_parallel_time, _512_128)]
acc_2048_32 = [round(a / b, 6) for a, b in zip(non_parallel_time, _2048_32)]
acc_512_32 = [round(a / b, 6) for a, b in zip(non_parallel_time, _512_32)]

plt.figure(figsize=(8, 5), dpi=80)
p1, = plt.plot(n_vector_dims, acc_2048_512, label='2048_512')
p2, = plt.plot(n_vector_dims, acc_512_512, label='512_512')
p3, = plt.plot(n_vector_dims, acc_2048_128, label='2048_128')
p4, = plt.plot(n_vector_dims, acc_512_128, label='512_128')
p5, = plt.plot(n_vector_dims, acc_2048_32, label='2048_32')
p6, = plt.plot(n_vector_dims, acc_512_32, label='512_32')
plt.ylabel('acc.')
plt.xlabel('n_vector_dims')
plt.legend(handles=[p1, p2, p3, p4, p5, p6])

plt.savefig('pic3.jpg')

print(acc_2048_512)
print(acc_512_512)
print(acc_2048_128)
print(acc_512_128)
print(acc_2048_32)
print(acc_512_32)
