#include "stdio.h"
#include <time.h>

int main()
{
    clock_t start = clock();
    printf("hello world\n");
    clock_t end = clock();
    printf("time %f\n", ((double) (end - start)) / CLOCKS_PER_SEC);
    return 0;
}
