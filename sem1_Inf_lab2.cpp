#include <iostream>
#include <cstdlib>
#include <string>
using namespace std;

void showError() {
	cout << "Invalid input. Try again" << endl;
}
string getStringInput(string &request_message)
{
	string inp_str;
	cout << request_message;
	bool inp_valid = false;
	bool check;
	while (inp_valid == false) {

		check = true;
		getline(cin, inp_str);
		if (inp_str == "" or inp_str == ".") check = false;

		char ch;
		int ch_count = 0;
		int smth = inp_str.length();
		while (smth > 0) {
			ch = inp_str[smth - 1];
			if (!isdigit(ch) and ch != '.') check = false;
			if (ch == '.') ++ch_count;
			--smth;
		}
		if (check and (ch_count == 0 or ch_count == 1)) inp_valid = true;
		else showError();
	}
	return inp_str;
}
long double stringToLongDouble(string to_process)
{
	long double out;
	bool check = true;
	bool exception_caught = false;
	try {
		out = stold(to_process);
	}
	catch (const invalid_argument) {
		exception_caught = true;
		check = false;
	}
	catch (const out_of_range) {
		exception_caught = true;
		check = false;
	}
	if (exception_caught == false) if (out < 0) check = false;

	if (check == true) return out;
	else {
		showError();
		throw invalid_argument("");
	}
}
long double getLongDoubleInput(string request_message)
{
	long double out;
	string inp;

	bool inp_valid = false;
	bool convert_suc = true;
	while (inp_valid == false) {
		inp = getStringInput(request_message);
		try {
			out = stringToLongDouble(inp);
		}
		catch (const invalid_argument) {
			convert_suc = false;
		}
		if (convert_suc) inp_valid = true;
		else showError();
	}	
	return out;
}

int main()
{
	/*
	Option 5. Approximate root.
	The program must, for a given non-negative number x, calculate the elements of the sequence, the first element of which
	equals x, and each subsequent one is the arithmetic mean of the previous element and the ratio of x to the previous element, up to
	until the next element differs from the square root of x by no more than a given number.

	Specifications Input: A non-negative fractional number x, from which you want to extract the root, and a positive fractional value of the calculation precision.
	Output data: The number of the first matching element of the sequence, this element itself and the value of the modulus of the difference between this
	element and real value of the root of x.
	*/

	/*
	TO FIX:
	DONE - user can enter only 1 point (add point counter to input() ), (if there are several points the programm doesn't throw an error);
	DONE - (?) eps can't be greater than 1 (if it is not requered : remove the while cycle and defolt eps value);
	---------------------------------------------------------------------
	TO ADD:
	 DONE - main algorithm;
	*/

	string inp;
	bool again = true;
	while (again == true) {

		long double x;
		long double eps = 2.0;
		x = getLongDoubleInput("Enter x : ");
		while (eps > 1) eps = getLongDoubleInput("Enter the absolute error : ");

		// ------------------ MAIN ALGORITHM---------------------------

		int counter = 0;
		long double defx = x;
		long double prev_x = x;
		while ((prev_x - x) > eps or counter == 0){
			++counter;
			prev_x = x;
			x = (x + (defx/ x)) * 0.5;
		}
		//cout << "\n" << sqrt(x) << endl;
		cout << "\n#" << counter<< "\nx = " << x << "\nan absolute error = " << prev_x - x;

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
			else showError();
		}
	}
	return 0;
} 
