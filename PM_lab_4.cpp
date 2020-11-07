#include <iostream>
#include <vector>
using namespace std;

int main()
{
	/*
	Option 16.
	Filter string from numbers.
	Input data: string.
	Output data: a string without numbers and an array of numbers.
	*/

	string inp;
	bool again = true;
	while (again == true) {

		// ------------------ MAIN ALGORITHM---------------------------
		
		cin >> inp;
		vector<int>  out;
		string out_str = "";

		for (int i = 0; i < inp.length(); ++i) {
			if (inp[i] >= '0' and inp[i] <= '9') out.push_back(inp[i] - '0');
			else out_str += inp[i];
		}
		cout << "\n" << out_str << endl;
		for (int i = 0; i < out.size(); ++i) cout << out[i] << " ";

		// ---------------- END OF MAIN ALGORITHM ----------------------

		char again_inp;
		bool again_correct = false;
		cout << "\nContinue? (Y/N) ";
		while (again_correct == false) {
			cin >> again_inp;
			cin.ignore(numeric_limits<streamsize>::max(), '\n'); // somehow cleans buffer
			if ((again_inp == 'y') or (again_inp == 'Y') or (again_inp == 'n') or (again_inp == 'N')) {
				if ((again_inp == 'n') or (again_inp == 'N')) again = false;
				again_correct = true;
			}
			else cout << "Invalid input. Try again" << endl;
		}
	}
	return 0;
}
