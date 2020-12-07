#include <iostream>
#include <vector>
#include <fstream>
#include <string>
using namespace std;

int main()
{
	/*
	Option 16.
	Filter string from numbers.
	Input data: string.
	Output data: a string without numbers and an array of numbers.
	*/

	bool again;
	do {

		// ------------------ MAIN ALGORITHM---------------------------

		ifstream infile("C:\\Users\\bubbl\\source\\repos\\ConsoleApplication1\\Release\\input.txt");
		string inp;
		if (infile.is_open()) {
			getline(infile, inp);
		}
		infile.close();
		cout << "Initial string :\n" << inp;

		vector<int> out;
		string out_letters = "";
		string out_digits = "";

		for (int i = 0; i < inp.length(); ++i) {
			if (inp[i] >= '0' and inp[i] <= '9') {
				out.push_back(inp[i] - '0');
				out_digits += inp[i];
			}
			else out_letters += inp[i];
		}

		/*int curr_num = 0;
		for (int i = 0; i < inp.length(); ++i) {
			if (inp[i] >= '0' && inp[i] <= '9') {
				if ((i != (inp.length() - 1)) && (inp[i + 1] >= '0') && (inp[i + 1] <= '9')) {
					curr_num *= 10;
					curr_num += inp[i] - '0';
				}
				else {
					curr_num *= 10;
					curr_num += inp[i] - '0';
					out.push_back(curr_num);
				}
			}
			else {
				out_letters += inp[i];
				curr_num = 0;
			}
		}*/

		cout << "\n\n" << out_letters << endl;
		for (int i = 0; i < out.size(); ++i) {
			cout << out[i] << " ";
		}

		ofstream fout("C:\\Users\\bubbl\\source\\repos\\ConsoleApplication1\\Release\\output.txt");
		if (fout.is_open()) {
			fout << out_letters << "\n";
			fout << out_digits;
		}
		fout.close();

		// ---------------- END OF MAIN ALGORITHM ----------------------

		char again_inp;
		bool again_correct = false;
		cout << "\nContinue? (Y/N) ";
		while (again_correct == false) {
			cin >> again_inp;
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			if ((again_inp == 'y') or (again_inp == 'Y') or (again_inp == 'n') or (again_inp == 'N')) {
				if ((again_inp == 'n') or (again_inp == 'N')) again = false;
				else again = true;
				again_correct = true;
			}
			else cout << "Invalid input. Try again" << endl;
		}
	} while (again == true);
	return 0;
}