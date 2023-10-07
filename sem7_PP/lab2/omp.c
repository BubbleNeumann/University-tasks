#include <omp.h>
#define CHUNK 100
#define NMAX 1000000
#include "stdio.h"

int main(int argc, char* argv[]){
	omp_set_num_threads(2);
	int i;
	double a[NMAX], sum;
	//заполнение массива 
	double st_time, end_time;
	st_time = omp_get_wtime();
	sum = 0;
#pragma omp parallel for shared(a) private(i)
	for (i=0; i<NMAX; i++){
		sum = sum + a[i];
	}
	end_time = omp_get_wtime ();
	end_time = end_time - st_time;
	printf("\nTotal Sum = %10.2f",sum);
	printf("\nTIME OF WORK IS %f ", end_time);
	return 0;
}

