#include <iostream>
#include <cstdlib>
#include <string>
using namespace std;

void error_message() {
	cout << "Invalid input. Try again" << endl;
}
string input(string request_message, bool & if_double)
{
	string inp_str;
	cout << request_message;
	bool inp_valid = false;
	bool check;
	while (inp_valid == false) {

		check = true;
		if_double = false;	
		getline(cin, inp_str);
		if (inp_str == "") check = false;

		char ch;
		int smth = inp_str.length();
		while (smth > 0) {
			ch = inp_str[smth - 1];
			if (!isdigit(ch) and ch != '.') check &= false;
			if (ch == '.') if_double = true;
			--smth;
		}
		if (check) inp_valid = true;
		else error_message();
	}
	return inp_str;
}
double convert_double(string to_process)
{
	double out;
	bool check = true;
	bool exception_caught = false;
	try {
		out = stod(to_process);
	}
	catch (const invalid_argument) {
		exception_caught = true;
		check &= false;
	}
	catch (const out_of_range) {
		exception_caught = true;
		check &= false;
	}
	//if (exception_caught == false) if (out <= 0) check &= false;

	if (check == true) return out;
	else {
		error_message();
		return -2;
	}
}
int convert_int(string to_process)
{
	int out;
	bool check = true;
	bool exception_caught = false;
	try {
		out = stoi(to_process);
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

	if (check) return out;
	else {
		error_message();
		return -2;
	}
}
long double calculate_a(double x, int i) 
{
	const long double pi = 3.14159265358979323846264338;
	long double a;
	a = sin((pi * i / 4.0)) * pow(2, (i / 2.0));

	for (int n = 0; n <= i; ++n) {
		if (n == 0) a *= x / 1.0;
		else a *= x / (double)n;
	}
	
	return a;
}

int main()
{
	int alfa_int = -1;
	double alfa_fl = -1.0;
	double x = -1.0;
	bool if_double;
	string inp;

	bool again = true;
	while (again == true) {

		bool inp_valid = false;
		while (inp_valid == false) {
			inp = input("Enter x: ", if_double);
			x = convert_double(inp);
			if ((x != -2) and (abs(x) <= 1)) inp_valid = true;
			else error_message();
		}
		inp_valid = false;
		while (inp_valid == false) {
			inp = input("Enter alfa: ", if_double);
			if (if_double) alfa_fl = convert_double(inp);
			else alfa_int = convert_int(inp);
			if ((alfa_fl != -2) and (alfa_int != -2)) {
				if (alfa_fl != -2 and alfa_fl < 1 and alfa_fl > 0) inp_valid = true;
				else if (alfa_int != -2) inp_valid = true;
			}
			else error_message();
		}

		// ------------------ MAIN ALGORITHM---------------------------

		long double sum = 0;
		long double a;
		long double a1;

		if (if_double == false) {
			for (int i = 0; i <= alfa_int; ++i) {
				a = calculate_a(x, i);
				a1 = calculate_a(x, i + 1);	
				sum += a;
				cout << "\na #" << i << " = " << a << " Current summ : " << sum ;
				cout << " Current error : 0 ";
				cout << " Current error : " << abs(a1 / sum) << endl;
				//if ((int)sum == 0) cout << " Current error : 0 " ;
				//else cout << " Current error : " << abs(a1 / sum) << endl;
			}
		}
		else {
			int i = 0;
			a1 = calculate_a(x, i + 1);
			while (abs(a1 / sum) > alfa_fl) {
				a = calculate_a(x, i);
				a1 = calculate_a(x, i + 1);
				sum += a;
				cout << "\na #" << i << " = " << a << " \nCurrent summ : " << sum ;
				cout << " Current error : 0 ";
				cout << " Current error : " << abs(a1 / sum) << endl;
				//if ((int)sum == 0) cout << " Current error : 0 " ;
				//else cout << " Current error : " << abs(a1 / sum) << endl;
				++i;	
			}
		}
		cout << "\nFinal sum : " << sum << endl;

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
			else error_message();
		}
	}
	return 0;
}
