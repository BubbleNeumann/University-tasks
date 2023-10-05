#include <math.h>
#include <omp.h>
#include <time.h>
#include <stdlib.h>
#include <locale.h>
#include <stdio.h>


int main(int argc, char* argv[])
{
	omp_set_num_threads(12);
    double start = omp_get_wtime();
	int nTheads, theadNum;
	#pragma omp parallel  private(nTheads, theadNum)
	{
		nTheads = omp_get_num_threads(); 
		theadNum = omp_get_thread_num(); 
		printf("OpenMP thread ?%d from %d threads \n", theadNum, nTheads);
	}
    double finish = omp_get_wtime();
    printf("time %f", finish - start);
	return 0;
}

