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

		int sp = inp_str.find(" ");
		if (sp > 0) check &= false;
		
		bool exception_caught = false;
		try {
			inp = stoi(inp_str);
		}
		catch (const invalid_argument& e) {
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

bool gcd(int a, int b)
{
	while (a != b) {
		if (b > a) swap(a, b);
		while (a > b) a -= b;
	}
	if (a == 1) return true;
	else return false;
}

int main()
{
	int inp;
	int modul;

	bool again = true;
	while (again == true) {

		inp = input("Input a positive integer > ");
		modul = input("\nInput a module > ");

		// Euclidean algorithm (if gcd == 1, it is possible to find the invesed element)

		if (gcd(inp, modul) == true) {
			
			int ans = 1;
			while ((inp * ans) % modul != 1) ++ans;
			cout << "Result : " << ans << endl;
		}
		else cout << "It's impossible to calculate\n";
		
		string again_inp;
		bool again_inp_check = false;
		
		while (again_inp_check == false) {
			cout << "Continue? (Y/N) ";
			cin >> again_inp;
			if ((again_inp == "y") or (again_inp == "Y") or (again_inp == "n") or (again_inp == "N")) {
				if ((again_inp == "n") or (again_inp == "N")) again = false;
				again_inp_check = true;
			}
			else error_message();
		}
	}
	system("pause");
	return 0;
}