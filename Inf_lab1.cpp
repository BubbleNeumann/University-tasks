#include <iostream>
#include <cstdlib>
#include <string>
using namespace std;

void error_message(){
	cout << "Invalid input. Try again" << endl;
}

int input (string request_message)
{
	int inp = 0;
	string inp_str;
	
	cout << request_message;
	bool inp_valid = false;
	bool check;
	while (inp_valid == false) {

		check = true;
		string inp_str;
		getline(cin, inp_str);
		
		char ch;
		int smth = inp_str.length();
		while (smth > 0) {
			ch = inp_str[smth-1];
			if (!isdigit(ch)) check &= false;
			--smth;
		}

		bool exception_caught = false;
		try {
			inp = stoi(inp_str);
		}
		catch (const invalid_argument& e) {
			exception_caught = true;
			check &= false;
		}
		catch (const out_of_range& e) {
			exception_caught = true;
			check &= false;
		}
		if (exception_caught == false) {
			if (inp <= 0) check &= false;
			if (typeid(inp).name() != typeid(5).name()) check &= false;
		}		
		if (check == true) inp_valid = true;
		else error_message();
	}
	return inp;
}

int gcd(int a, int b, int& x, int& y)
{
	if (a == 0) {
		x = 0;
		y = 1;
		return b;
	}
	int x1, y1;
	int d = gcd(b % a, a, x1, y1);
	x = y1 - (b / a) * x1;
	y = x1;
	return d;
}

int main()
{
	int inp;
	int modul;
	int x;
	int y;
	bool again = true;
	while (again == true) {

		inp = input("Input a positive integer > ");
		modul = input("\nInput a module > ");

		// Euclidean algorithm (if gcd == 1, it is possible to find the invesed element)

		if (gcd(inp, modul, x, y) == 1) {
			x = (x % modul + modul) % modul;
			cout << "Result : " << x << endl;
		}
		else cout << "It's impossible to calculate\n";
		
		char again_inp;
		bool again_correct = false;
		cout << "Continue? (Y/N) ";
		
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