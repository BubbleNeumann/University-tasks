﻿#include <iostream>
#include <fstream>
int main() {
    
    std::ifstream fromf("input.txt");
    std::ofstream inf("output.txt");
    if (fromf.is_open()) {
        int n;
        int ans = 0;
        fromf >> n;
        int* arr = new int[n];
        for (int i = 0; i < n; ++i) {
            fromf >> arr[i];
            if (arr[i] < 0) ans += arr[i] * arr[i] * arr[i];
        }
        fromf.close();

        inf << ans;
        std::cout << arr[3];
        inf.close();
        delete[] arr;
    }
    else inf << "Input file is not open";
    return 0;
}