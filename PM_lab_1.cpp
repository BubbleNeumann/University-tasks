#include <iostream>
using namespace std;
#include <cstdlib>

int main()
{
	int start_h;
	int start_m;
	int start_s;
	
	int fin_h;
	int fin_m;
	int fin_s;
		
	cout << "Enter time the process started (HH:MM:SS) > ";
	cin >> start_h >> start_m >> start_s;
	cout << "\nEnter time the process was over (HH:MM:SS) > ";
	cin >> fin_h >> fin_m >> fin_s;

	if (start_h > fin_h) {
		fin_h += 24;
	}
	if (start_m > fin_m) {
		fin_m += 60;
	}
	if (start_s > fin_s) {
		fin_s += 60;
	}
	
	cout << "\nThe process' duration: ";
	cout << fin_h - start_h << ":" << fin_m - start_m << ":" << fin_s - start_s << endl;

	system("pause");
	return 0;
}