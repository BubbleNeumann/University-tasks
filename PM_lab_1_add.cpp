#include <iostream>
#include <cstdlib>
#include <string>
#include <vector>
using namespace std;

void error_message() {
	cout << "Invalid input. Try again" << endl;
}

int input(string request_message, bool ask_to_input, string & single_symbol)
{
	int inp = 0;
	string inp_str;

	cout << request_message;
	bool inp_valid = false;
	bool check;
	while (inp_valid == false) {

		check = true;
		if (ask_to_input == true) {

			getline(cin, inp_str);

			char ch;
			int smth = inp_str.length();
			while (smth > 0) {
				ch = inp_str[smth - 1];
				if (!isdigit(ch)) check = false;
				--smth;
			}
		}
		else inp_str = single_symbol;

		bool exception_caught = false;
		try {
			inp = stoi(inp_str);
		}
		catch (const invalid_argument& e) {
			exception_caught = true;
			check = false;
		}
		catch (const out_of_range& e) {
			exception_caught = true;
			check = false;
		}
		if (check == true) inp_valid = true;
		else if (ask_to_input == false and check == false) return -666;
		else error_message();
	}
	return inp;
}
int count_spaces(string s) {
	int count = 0;
	for (int i = 0; i < s.size(); ++i)
		if (s[i] == ' ') ++count;
	return count;
}


vector<int> primal_processing(int& len, string& single_symbol)
{
	vector<int> main;
	string to_process;

	bool inp_valid = false;
	while (inp_valid == false) {

		getline(cin, to_process);
		if (to_process.find(" ") != std::string::npos and count_spaces(to_process) == (len - 1)) inp_valid = true;

		while (to_process.length() > 0) {
			string single_symbol = "";

			if (to_process.find(" ") == std::string::npos) {
				single_symbol = to_process;
				to_process.clear();
			}
			else {
				single_symbol = to_process.substr(0, to_process.find(" ") + 1);
				to_process.erase(0, to_process.find(" ") + 1);
			}
			
			if (input("", false, single_symbol) != -666) {
				inp_valid &= true;
				main.push_back(input("", false, single_symbol));
			}
			else {
				inp_valid = false;
				main = {};
				break;
			}
		}
		if (inp_valid == false) error_message();
	}
	return main;
}

int main()
{
	int len;
	bool again = true;
	string single_symbol;
	while (again == true) {

		len = input("Enter the length of the sqare array's string : ", true, single_symbol);
		vector<vector<int>> final;

		for (int i = 1; i <= len; ++i) {
			cout << "\nEnter the elements of the " << i << " string separated by spaces : ";
			final.push_back(primal_processing(len, single_symbol));
		}
		cout << "Your matrix: \n";
		for (int i = 0; i < len; ++i) {
			for (int j = 0; j < len; ++j) {
				cout << final[i][j] << " ";
			}
			cout << endl;
		}
		cout << endl<< "The transposed matrix: \n";
		for (int i = 0; i < len; ++i) {
			for (int j = 0; j < len; ++j) {
				if (i < j) swap(final[i][j], final[j][i]);
				cout << final[i][j] << " ";
			}
			cout << endl;
		}

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
			else error_message();
		}
	}
	return 0;
}
