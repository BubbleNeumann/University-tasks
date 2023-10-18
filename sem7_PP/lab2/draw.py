import matplotlib.pyplot as plt

n_proc = [5, 10, 15]

# TODO : add time for MPI

# table 3
omp_crit = [0.624505, 0.628952, 0.840364]
omp_atomic = [0.626001, 0.788721, 0.729887]
omp_reduction = [0.004366, 0.004694, 0.004573]

plt.figure(figsize=(6, 4), dpi=80)
p1, = plt.plot(n_proc, omp_crit, color='b', label='omp crit')
p2, = plt.plot(n_proc, omp_atomic, color='g', label='omp atomic')
p3, = plt.plot(n_proc, omp_reduction, color='r', label='omp reduction')
plt.ylabel('time (sec)')
plt.xlabel('n_proc')
plt.legend(handles=[p1, p2, p3])
plt.savefig('pic6.jpg')


non_parallel_time = 0.02

# acceleration (table 4)
plt.figure(figsize=(6, 4), dpi=80)
p1, = plt.plot(n_proc, [non_parallel_time / x for x in omp_crit], color='b', label='omp crit')
p2, = plt.plot(n_proc, [non_parallel_time / x for x in omp_atomic], color='g', label='omp atomic')
p3, = plt.plot(n_proc, [non_parallel_time / x for x in omp_reduction], color='r', label='omp reduction')
plt.ylabel('acc.')
plt.xlabel('n_proc')
plt.legend(handles=[p1, p2, p3])
plt.savefig('pic7.jpg')

omp_crit_q = []
omp_atomic_q = []
omp_reduction_q = []

mpi_pp = []
mpi_collective = []
mpi_pp_q = []
mpi_collective_q = []


