#include <iostream>
#include <random>

void printArray(int *array, int len)
{
    for (int i = 0; i < len; std::cout << array[i++] << std::endl)
        ;
}

void mergeSortedArrays(int one[], int len_one, int two[], int len_two)
{
    int res[len_one + len_two] = {0}; // zero-initialized array

    int i = 0; // i is a poiter for first array, j is for the second
    int j = 0;
    while (i + j < len_one + len_two)
    {
        std::cout << i << j << std::endl;
        if (one[i] <= two[j] && i < len_one)
        {
            res[i + j] = one[i];
            ++i;
        }
        if (one[i] >= two[j] && j < len_two)
        {
            res[i + j] = two[j];
            ++j;
        }
        if (i == len_one || j == len_two)
        {
            res[i + j] = !(i == len_one) * one[i] + !(j == len_two) * two[j];
            i += !(i == len_one);
            j += !(j == len_two);
        }
    }

    printArray(res, len_one + len_two);
}

int main()
{

    // Write a function to merge two sorted arrays into one sorted array.

    // TODO generate new arrays using lambda

    std::random_device rd; // to seed the random number generator object called mt
    std::mt19937 mt(rd()); // requests for random data to the operating system
    std::uniform_int_distribution<int> dist(1, 99);

    // std::cout << dist(mt) << std::endl;

    int len_one, len_two;
    std::cin >> len_one >> len_two;

    int one[] = {1, 2, 3, 4};
    int two[] = {2, 9, 12};

    mergeSortedArrays(one, len_one, two, len_two);

    return 0;
}
