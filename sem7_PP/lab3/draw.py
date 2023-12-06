import matplotlib.pyplot as plt

n_proc = [5, 10, 15]


# table 3
omp_static = [1.660293,1.508270,1.436218]
omp_dynamic = [1.251977,1.149849,0.953414]
omp_guided = [1.222666,1.174816,0.945487]
mpi_mul = [0.008780,0.008854,0.009743]
mpi_non_mul = [0.008319,0.008534,0.00741]

plt.figure(figsize=(6, 4), dpi=80)
p1, = plt.plot(n_proc, omp_static, color='b', label='omp static')
p2, = plt.plot(n_proc, omp_dynamic, color='g', label='omp dynamic')
p3, = plt.plot(n_proc, omp_guided, color='r', label='omp quided')
p4, = plt.plot(n_proc, mpi_mul, color='orange', label='mpi mul')
p5, = plt.plot(n_proc, mpi_non_mul, color='black', label='mpi non mul')
plt.ylabel('time (sec)')
plt.xlabel('n_proc')
plt.legend(handles=[p1, p2, p3, p4, p5])
plt.savefig('pic6.jpg')


# acceleration (table 4)
non_parallel_time = 0.03
plt.figure(figsize=(6, 4), dpi=80)
p1, = plt.plot(n_proc, [non_parallel_time / x for x in omp_static], color='b', label='omp crit')
p2, = plt.plot(n_proc, [non_parallel_time / x for x in omp_dynamic], color='g', label='omp atomic')
p3, = plt.plot(n_proc, [non_parallel_time / x for x in omp_guided], color='r', label='omp reduction')
p4, = plt.plot(n_proc, [non_parallel_time / x for x in mpi_mul], color='orange', label='mpi point-to-point')
p5, = plt.plot(n_proc, [non_parallel_time / x for x in mpi_non_mul], color='black', label='mpi collective')
plt.ylabel('acc.')
plt.xlabel('n_proc')
plt.legend(handles=[p1, p2, p3, p4, p5])
plt.savefig('pic7.jpg')

print('acceleration without q:')
print([non_parallel_time / x for x in omp_static])
print([non_parallel_time / x for x in omp_dynamic])
print([non_parallel_time / x for x in omp_guided])
print([non_parallel_time / x for x in mpi_mul])
print([non_parallel_time / x for x in mpi_non_mul])

# table 5 (time with Q parameter)
omp_static_q = [0.927363,0.783763,1.017671]
omp_dynamic_q = [0.927363,0.783763,1.017671]
omp_guided_q = [0.897342,0.992380,1.184587]
mpi_mul_q = [0.097640,0.097755,0.110743]
mpi_non_mul_q = [0.117640,0.137755,0.170743]
# mpi_mul_q = [0.118640,0.019755,0.113743]
# mpi_non_mul_q = [0.009528,0.011645,0.016442]

plt.figure(figsize=(6, 4), dpi=80)
p1, = plt.plot(n_proc, omp_static_q, color='b', label='omp crit')
p2, = plt.plot(n_proc, omp_dynamic_q, color='g', label='omp atomic')
p3, = plt.plot(n_proc, omp_guided_q, color='r', label='omp reduction')
p4, = plt.plot(n_proc, mpi_mul_q, color='orange', label='mpi point-to-point')
p5, = plt.plot(n_proc, mpi_non_mul_q, color='black', label='mpi collective')
plt.ylabel('time (sec)')
plt.xlabel('n_proc')
plt.legend(handles=[p1, p2, p3, p4, p5])
plt.savefig('pic12.jpg')

# acceleration (table 6)
non_parallel_time = 8.89
plt.figure(figsize=(6, 4), dpi=80)
p1, = plt.plot(n_proc, [non_parallel_time / x for x in omp_static_q], color='b', label='omp crit')
p2, = plt.plot(n_proc, [non_parallel_time / x for x in omp_dynamic_q], color='g', label='omp atomic')
p3, = plt.plot(n_proc, [non_parallel_time / x for x in omp_guided_q], color='r', label='omp reduction')
p4, = plt.plot(n_proc, [non_parallel_time / x for x in mpi_mul_q], color='orange', label='mpi point-to-point')
p5, = plt.plot(n_proc, [non_parallel_time / x for x in mpi_non_mul_q], color='black', label='mpi collective')
plt.ylabel('acc.')
plt.xlabel('n_proc')
plt.legend(handles=[p1, p2, p3, p4, p5])
plt.savefig('pic13.jpg')

print('acceleration with q parameter:')
print([non_parallel_time / x for x in omp_static_q])
print([non_parallel_time / x for x in omp_dynamic_q])
print([non_parallel_time / x for x in omp_guided_q])
print([non_parallel_time / x for x in mpi_mul_q])
print([non_parallel_time / x for x in mpi_non_mul_q])
