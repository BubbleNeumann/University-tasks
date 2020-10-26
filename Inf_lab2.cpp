#include <iostream>
#include <cstdlib>
#include <string>
using namespace std;

void error_message() {
	cout << "Invalid input. Try again" << endl;
}
string input(string &request_message)
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
		else error_message();
	}
	return inp_str;
}
long double convert_Ldouble(string to_process, bool &convert_suc)
{
	long double out;
	bool check = true;
	bool exception_caught = false;
	try {
		out = stold(to_process);
	}
	catch (const invalid_argument) {
		exception_caught = true;
		check &= false;
	}
	catch (const out_of_range) {
		exception_caught = true;
		check &= false;
	}
	if (exception_caught == false) if (out < 0) check = false;

	if (check == true) return out;
	else {
		error_message();
		convert_suc = false;
		return 0;
	}
}
long double general_processing(string request_message)
{
	long double out;
	string inp;

	bool inp_valid = false;
	bool convert_suc = true;
	while (inp_valid == false) {
		inp = input(request_message);
		out = convert_Ldouble(inp, convert_suc);
		if (convert_suc) inp_valid = true;
		else error_message();
	}	
	return out;
}

int main()
{
	/*
	Вариант 5. Приближённый корень.
	Программа должна для заданного неотрицательного числа x вычислять элементы последовательности, первый элемент которой
	равен x, а каждый последующий – среднему арифметическому из предыдущего элемента и отношения x к предыдущему элементу, до
	тех пор, пока очередной элемент не станет отличаться от квадратного корня из x не более чем на заданное число.
	
	Входные данные : Неотрицательное дробное число x, из которого нужно извлечь корень, и положительное дробное значение точности вычислений.
	Выходные данные : Номер первого подходящего элемента последовательности, сам этот элемент и значение модуля разности между этим
	элементом и реальным значением корня из x.
	*/

	/*
	TO FIX:
	 - user can enter only 1 point (add point counter to input() ), (if there are several points the programm doesn't throw an error);
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
		x = general_processing("Enter x : ");
		while (eps > 1) eps = general_processing("Enter the absolute error : ");

		// ------------------ MAIN ALGORITHM---------------------------

		int counter = 0;
		long double defx = x;
		while (abs((sqrt(defx) - x)) > eps){
			++counter;
			x = (x + (defx/ x)) * 0.5;
		}
		//cout << "\n" << sqrt(x) << endl;
		cout << "\n#" << counter<< "\nx = " << x << "\nan absolute error = " << abs((sqrt(defx) - x));

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
