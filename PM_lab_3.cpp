#include <iostream>
#include <string> // stoi(), getline()
#include <vector>
#include <algorithm> //sort()
#include <chrono>
using namespace std;

void merge(vector<int>& A, int& iBegin, int& iMiddle, int& iEnd, vector<int>& B)
{
	int i = iBegin;
	int j = iMiddle;

	for (int k = iBegin; k < iEnd; ++k) {
		if (i < iMiddle && (j >= iEnd || A[i] <= A[j])) {
			B[k] = A[i];
			++i;
		}
		else {
			B[k] = A[j];
			++j;
		}
	}
}
void split(vector<int>& B, int iBegin, int iEnd, vector<int>& A)
{
	if (iEnd - iBegin <= 1) return;
	int iMiddle = (iEnd + iBegin) / 2;
	split(A, iBegin, iMiddle, B);
	split(A, iMiddle, iEnd, B);
	merge(B, iBegin, iMiddle, iEnd, A);
}

void showError() {
	cout << "Invalid input. Try again" << endl;
}
int getSymbol(string request_message, bool ask_to_input, string& single_symbol)
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
		else if (ask_to_input == false and check == false) throw invalid_argument("");
		else showError();
	}
	return inp;
}
int countSpaces(string s) {
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
		if (countSpaces(to_process) == (len - 1)) inp_valid = true;

		while (to_process.length() > 0) {
			string single_symbol = "";
			if (to_process.find(" ") == string::npos) {
				single_symbol = to_process;
				to_process.clear();
			}
			else {
				single_symbol = to_process.substr(0, to_process.find(" ") + 1);
				to_process.erase(0, to_process.find(" ") + 1);
			}
			bool ex_caught = false;
			if (ex_caught == false) main.push_back(getSymbol("", false, single_symbol));
		}
		if (inp_valid == false) showError();
	}
	return main;
}
bool binaryChoice(string request)
{
	char again_inp;
	bool again_correct = false;
	cout << request;
	while (again_correct == false) {
		cin >> again_inp;
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		if ((again_inp == 'y') or (again_inp == 'Y') or (again_inp == 'n') or (again_inp == 'N')) {
			if ((again_inp == 'n') or (again_inp == 'N')) return false;
			if ((again_inp == 'y') or (again_inp == 'Y')) return true;
			again_correct = true;
		}
		else showError();
	}
}

int main()
{
	string single_symbol;
	vector<int> A;
	
	bool again = true;
	while (again == true) {

		/*
		Вариант 13.
		Сортировка слиянием.
		Строго случайные данные и «почти отсортированные» случайные данные.
		Входные данные: количество элементов, тип входного вектора, вектор.
		Выходные данные:. отсортированный массив, время работы библиотечной и реализованной функций сортировок, ускорение библиотечной сортировки.
		Должна присутствовать возможность выбора исходного вектора: вводимый с клавиатуры или генерируемый согласно варианту (два возможных для выбора
		типа генерируемых данных);
		*/

		// ------------------ MAIN ALGORITHM---------------------------

		int len = getSymbol("Enter the number of the elements : ", true, single_symbol);
		bool hand_input = binaryChoice("Hand input? (Y/N) ");
		if (hand_input) {
			cout << "\nEnter the elements of the vector separated by spaces : ";
			A = primal_processing(len, single_symbol);
		}
		else {
			for (int i = 0; i < len; ++i) A.push_back(rand() % 1000);
			bool partly_sorted = binaryChoice("Shall it be partly sorted? (Y/N) ");
			if (partly_sorted) {
				sort(A.begin(), A.end());
				int k;
				for (int i = 0; i < (int)len / 4; ++i) {
					k = rand() & len;
					swap(A[k], A[len - 1 - k]);
				}
			}			
		}
		vector<int> copy = A;
		vector<int> B = A;	
		cout << endl << "\nInitial vector: ";
		for (int i = 0; i < len; ++i) cout << A[i] << " ";		
		
		auto t1 = chrono::high_resolution_clock::now();
		split(B, 0, len , A);
		auto t2 = chrono::high_resolution_clock::now();
		auto duration_custom = chrono::duration_cast<chrono::microseconds>(t2 - t1).count();

		t1 = chrono::high_resolution_clock::now();
		sort(copy.begin(), copy.end());
		t2 = chrono::high_resolution_clock::now();
		auto duration_defolt = chrono::duration_cast<chrono::microseconds>(t2 - t1).count();

		if (len > 50) {
			cout << "\nSorted vector is too long, so there are its elements from i = 20 to i = 50 : \n";
			for (int i = 20; i <= 50; ++i) cout << A[i] << " ";
		}
		else {
			cout << endl << "\nSorted: ";
			for (int i = 0; i < len; ++i) cout << A[i] << " ";
		}

		cout << "\nLibrary sorting worktime (microseconds) : " << duration_defolt;
		cout << "\nCustom sorting worktime (microseconds) : " << duration_custom;

		// ---------------- END OF MAIN ALGORITHM ----------------------

		again = binaryChoice("\nContinue? (Y/N) ");
	}
	return 0;
}
