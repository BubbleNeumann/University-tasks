#include <iostream>
#include <string>
#include <random>
using namespace std;

void showError() {
    cout << "Invalid input. Try again" << endl;
}
int getSymbol(const string& request_message, bool ask_to_input, string& single_symbol)
{
    int inp;
    string inp_str;

    cout << request_message;
    while (true) {
        bool inp_valid = true;
        if (ask_to_input) {
            getline(cin, inp_str);
            char ch;
            int smth = inp_str.length();
            while (smth > 0) {
                ch = inp_str[smth - 1];
                if (!isdigit(ch)) inp_valid = false;
                --smth;
            }
        }
        else inp_str = single_symbol;
        try {
            inp = stoi(inp_str);
        }
        catch (const invalid_argument& e) {
            inp_valid = false;
        }
        catch (const out_of_range& e) {
            inp_valid = false;
        }
        if (!ask_to_input && !inp_valid) {
            throw invalid_argument("");
        }
        else if (inp_valid)
            return inp;
        else
            showError();
    }
}
int countSpaces(const string& s) {
    int count = 0;
    for (char i : s)
        if (i == ' ') ++count;
    return count;
}
int* primal_processing(int& len, string& single_symbol)
{
    int* main = (int*) malloc(len * sizeof(int));

    string to_process;
    bool inp_valid = false;
    while (!inp_valid) {

        getline(cin, to_process);
        if (countSpaces(to_process) == (len - 1)) inp_valid = true;
        int i = 0;
        while (to_process.length() > 0) {
            single_symbol = "";
            if (to_process.find(' ') == string::npos) {
                single_symbol = to_process;
                to_process.clear();
            }
            else {
                single_symbol = to_process.substr(0, to_process.find(' ') + 1);
                to_process.erase(0, to_process.find(' ') + 1);
            }
            try {
                main[i] = getSymbol("", false, single_symbol);
            }
            catch (invalid_argument){
                inp_valid = false;
            }
            ++i;
        }
        if (!inp_valid) showError();
    }
    return main;
}
bool binaryChoice(const string& request, char positive, char negative)
{
    char again_inp;
    cout << request;
    while (true) {
        cin >> again_inp;
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        if (again_inp == negative) return false;
        else if (again_inp == positive) return true;
        else showError();
    }
}

int main()
{
    string single_symbol;

    bool again = true;
    while (again) {
        int col = getSymbol("Number of columns :", true, single_symbol);
        int row = getSymbol("Number of rows :", true, single_symbol);
        int** A = (int**) malloc(row * sizeof(int));
        bool hand_input = binaryChoice("Hand input? (Y/N)", 'y', 'n');

        random_device rd; //  to seed the random number generator object called mt
        mt19937 mt(rd()); // requests for random data to the operating system.
        uniform_int_distribution<int> dist(10, 99);

        if (hand_input) {
            for (int i = 0; i < row; ++i) {
                cout << "\nEnter the elements of the " << i + 1 << " row separated by spaces :";
                A[i] = primal_processing(col, single_symbol);
            }
        }
        else {
            for (int i = 0; i < row; ++i) {
                A[i] = (int*) malloc(col * sizeof(int));
                for (int j = 0; j < col; ++j) {
                    A[i][j] = dist(mt);
                }
            }
        }

        cout << "Initial matrix: \n";
        for (int i = 0; i < row; ++i) {
            for (int j = 0; j < col; ++j) cout << A[i][j] << " ";
            cout << endl;
        }

        bool edit = binaryChoice("Do you want to edit the matrix? (Y/N)", 'y', 'n');
        int no;
        if (edit) {
            bool if_add;
            bool if_rows = binaryChoice("Edit Rows or Columns? (R/C)", 'r', 'c');
            if (if_rows) {
                if_add = binaryChoice("Add or delete one? (A/D)", 'a', 'd');
                if (if_add) {

                    do {
                        no = getSymbol("After which row do you want to inset a new one? ", true, single_symbol);
                    } while (no < 1 || no > row);

                    A = (int**) realloc(A, (row + 1) * sizeof(int));
                    ++row;
                    for (int i = row - 1; i > no; --i) {
                        A[i] = A[i - 1];
                    }
                    cout << "\nEnter the elements of the new row separated by spaces : ";
                    A[no] = primal_processing(col, single_symbol);
                }
                else {
                    do {
                        no = getSymbol("What row do you want to delete?", true, single_symbol);
                    } while (no < 1 || no > row);
                    for (int i = no - 1; i < row - 1; ++i) {
                        A[i] = A[i + 1];
                    }
                    --row;
                }
            }
            else {
                bool if_add = binaryChoice("Add or delete one? (A/D) ", 'a', 'd');
                if (if_add) {
                    do {
                        no = getSymbol("After which column do you want to inset a new one? ", true, single_symbol);
                    } while (no < 1 || no > col);

                    cout << "\nEnter the elements of the new column separated by spaces : ";
                    int* input_add = primal_processing(row, single_symbol);

                    for (int i = 0; i < row; ++i) {
                        A[i] = (int*) realloc(A[i], (col + 1) * sizeof(int));
                        for (int j = col; j > no; --j) {
                            A[i][j] = A[i][j - 1];
                        }
                        A[i][no] = input_add[i];
                    }
                    delete[] input_add;
                    ++col;
                }
                else {
                    do {
                        no = getSymbol("What column do you want to delete? ", true, single_symbol);
                    } while (no < 1 || no > col);
                    for (int i = 0; i < row; ++i) {
                        for (int j = no - 1; j < col - 1; ++j) {
                            A[i][j] = A[i][j + 1];
                        }
                    }
                    --col;
                }
            }

            cout << "New matrix: \n";
            for (int i = 0; i < row; ++i) {
                for (int j = 0; j < col; ++j)
                    cout << A[i][j] << " ";
                cout << endl;
            }

            if (!if_add && !if_rows) ++row;
            for (int i = 0; i < row; ++i) {
                free(A[i]);
            }
            free(A);
        }
        again = binaryChoice("\nContinue? (Y/N)", 'y', 'n');
    }
    return 0;
}
