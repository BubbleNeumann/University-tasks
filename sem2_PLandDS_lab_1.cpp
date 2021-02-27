#include <fstream>
#include <cmath>

double processing(double* arr, int n) {
   
    double ans = 1.0;
    for (int j = n-2; j >= 0; --j) {
        if (arr[j] < 0) ans *= pow(arr[j], 3);
    }    
    if (ans > 1 || ans < 1) return ans;
    else return 0;
}

int main() {
    std::ifstream fromf("input.txt");
    std::ofstream inf("output.txt");
    if (fromf.is_open() && inf.is_open()) {
        double* A = NULL;
        double* b = NULL;
        int i;
        for (i = 0; fromf.peek() != EOF; ++i) {
            b = (double*)realloc(A, (i+1) * sizeof(double));
            if (b != NULL) {
                A = b;
                fromf >> A[i];
            }
        }
        fromf.close();
        inf.precision(10);
        inf << processing(A, i);
        inf.close();
        free(A);
    }
    return 0;
}