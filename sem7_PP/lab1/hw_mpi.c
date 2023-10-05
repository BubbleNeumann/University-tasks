#include "mpi.h"
#include "stdio.h"
#include <time.h>
#include <math.h>
#include <omp.h>

int main(int argc, char* argv[])
{
    double t1 = MPI_Wtime(); // start 
	int rank, ranksize, i; 
	MPI_Init(&argc, &argv);// 
	//Определяем свой номер в группе:
	MPI_Comm_rank(MPI_COMM_WORLD, &rank); //
	//Определяем размер группы:
	MPI_Comm_size(MPI_COMM_WORLD, &ranksize);//
	printf("Hello world from process %d from total number of %d\n", rank, ranksize);
	MPI_Finalize();//
    double t2 = MPI_Wtime(); // finish
    printf( "Elapsed time is %f\n", t2 - t1 );
	return 0;
}

