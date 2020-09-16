#include <iostream>
using namespace std;
#include <cstdlib>

int main()
{
	int first;
	int second;
	int add;
	bool again = true;
	string inp;

	while (again == true) {

		cout << "Input an integer > ";
		cin >> first;
		cout << "\n Input an integer > ";
		cin >> second;

		while (first != second) {

			if (second > first) {

				add = first;
				first = second;
				second = add;
			}

			while (second < first) {

				first -= second;
			}
		}

		cout << "\n Result : " << first << endl;
		cout << "\n Continue? (Y/N) ";
		cin >> inp;
		if (inp == "Y" or inp == "y") {
			again = true;
		}
		else if (inp == "N" or inp == "n") {
			again = false;
		}
		else {
			cout << "\n Answer unclear ";
			again = false;
		}
	}
	system("pause");
	return 0;
}