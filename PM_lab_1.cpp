#include <iostream>
#include <string>
#include <typeinfo>
using namespace std;

void message() {
	cout << "Invalid input. Try again" << endl;
}

int main()
{
	int start_h;
	int start_m;
	int start_s;

	int fin_h;
	int fin_m;
	int fin_s;

	string start;
	string end;

	cout << "Enter time the process started (HH:MM:SS) > ";

	bool inp_valid = false;
	while (inp_valid == false) {

		cin >> start;
		if (start.size() == 8) {

			bool local = true;

			if ((start.at(2) != ':') or (start.at(5) != ':')) local &= false;

			string now = start.substr(6);
			bool exception_caught = false;
			try {
				start_s = stoi(now);
			}
			catch (const invalid_argument& e) {
				exception_caught = true;
				local &= false;
			}
			if (exception_caught == false) {
				if ((start_s < 0) or (start_s > 60)) local &= false;
				if (typeid(start_s).name() != typeid(5).name()) local &= false;
			}

			now = start.substr(3, 4);
			exception_caught = false;
			try {
				start_m = stoi(now);
			}
			catch (const invalid_argument& e) {
				exception_caught = true;
				local &= false;
			}
			if (exception_caught == false) {
				if ((start_m < 0) or (start_m > 60)) local &= false;
				if (typeid(start_m).name() != typeid(5).name()) local &= false;
			}

			now = start.substr(0, 2);
			exception_caught = false;
			try {
				start_h = stoi(now);
			}
			catch (const invalid_argument& e) {
				exception_caught = true;
				local &= false;
			}
			if (exception_caught == false) {
				if ((start_h < 0) or (start_h > 24)) local &= false;
				if (typeid(start_h).name() != typeid(5).name()) local &= false;
			}

			if (local == true) inp_valid = true;
			else message();
		}
		else message();
	}

	cout << "\nEnter time the process was over (HH:MM:SS) > ";

	inp_valid = false;
	while (inp_valid == false) {

		cin >> end;
		if (end.size() == 8) {

			bool local = true;

			if ((end.at(2) != ':') or (end.at(5) != ':')) local &= false;

			string now = end.substr(6);
			bool exception_caught = false;
			try {
				fin_s = stoi(now);
			}
			catch (const invalid_argument& e) {
				exception_caught = true;
				local &= false;
			}
			if (exception_caught == false) {
				if ((fin_s < 0) or (fin_s > 60)) local &= false;
				if (typeid(fin_s).name() != typeid(5).name()) local &= false;
			}

			now = end.substr(3, 4);
			exception_caught = false;
			try {
				fin_m = stoi(now);
			}
			catch (const invalid_argument& e) {
				exception_caught = true;
				local &= false;
			}
			if (exception_caught == false) {
				if ((fin_m < 0) or (fin_m > 60)) local &= false;
				if (typeid(fin_m).name() != typeid(5).name()) local &= false;
			}

			now = end.substr(0, 2);
			exception_caught = false;
			try {
				fin_h = stoi(now);
			}
			catch (const invalid_argument& e) {
				exception_caught = true;
				local &= false;
			}
			if (exception_caught == false) {
				if ((fin_h < 0) or (fin_h > 24)) local &= false;
				if (typeid(fin_h).name() != typeid(5).name()) local &= false;
			}

			if (local == true) inp_valid = true;
			else message();
		}
		else message();
	}

	if (start_h > fin_h) fin_h += 24;
	if (start_m > fin_m) fin_m += 60;
	if (start_s > fin_s) fin_s += 60;

	cout << "\nThe process' duration: ";
	cout << fin_h - start_h << ":" << fin_m - start_m << ":" << fin_s - start_s << endl;

	system("pause");
	return 0;
}