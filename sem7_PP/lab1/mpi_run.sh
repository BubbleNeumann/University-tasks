#!/bin/bash
#SBATCH --job-name=myjob
#SBATCH --time=00:03:00
#SBATCH --nodes=1 --ntasks-per-node=4
#SBATCH --mem=1gb

export I_MPI_LIBRARY=/usr/lib64/slurm/mpi_pmi2.so
srun --mpi=pmi2 ./mpi_out

