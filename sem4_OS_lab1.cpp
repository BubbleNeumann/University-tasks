#include <iostream>
#include <random>

void printArray(int array[], int len)
{
    for (int i = 0; i < len; std::cout << array[i++] << std::endl)
        ;
}

int *generateSortedArray(int len)
{   
    int *arr = new int[len];

    std::random_device rd; // to seed the random number generator object called mt
    std::mt19937 mt(rd()); // requests for random data to the operating system

    for (int i = 0; i < len; i++)
    {
        std::uniform_int_distribution<int> dist(i + i * 10, 1 + i * 11);
        arr[i] = dist(mt);
    }

    return arr;
}

void mergeSortedArrays(int one[], int len_one, int two[], int len_two)
{
    int res[len_one + len_two] = {0}; // zero-initialized array
    int i = 0, j = 0;                 // i is a poiter for first array, j is for the second
    while (i + j < len_one + len_two)
    {
        if (one[i] <= two[j] && i < len_one)
            res[i++ + j] = one[i];

        if (one[i] >= two[j] && j < len_two)
            res[i + j++] = two[j];

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

    const int LEN_ONE = 5;
    const int LEN_TWO = 5;

    int *arrOne = generateSortedArray(LEN_ONE);
    int *arrTwo = generateSortedArray(LEN_TWO);

    mergeSortedArrays(arrOne, LEN_ONE, arrTwo, LEN_TWO);
    delete [] arrOne;
    delete [] arrTwo;

    return 0;
}
