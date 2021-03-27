#include <iostream>
#include <fstream>
#include <string>
using namespace std;

void showError() {
    cout << "Invalid input. Try again" << endl;
}
int getSymbol(const string& request_message)
{
    int inp;
    string inp_str;
    cout << request_message;
    while (true) {
        bool inp_valid = true;
        cin >> inp_str;
        //cin.ignore(numeric_limits<streamsize>::max(), '\n');
        char ch;
        int smth = inp_str.length();
        while (smth > 0) {
            ch = inp_str[smth - 1];
            if (!isdigit(ch)) inp_valid = false;
            --smth;
        }

        try {
            inp = stoi(inp_str);
        }
        catch (const invalid_argument& e) {
            inp_valid = false;
        }
        catch (const out_of_range& e) {
            inp_valid = false;
        }

        if (inp_valid) {
            return inp;
        }
        else {
            showError();
        }
    }
}
bool binaryChoice(const string& request, char positive, char negative)
{
    char again_inp;
    cout << request;
    while (true) {
        cin >> again_inp;
        //cin.ignore(numeric_limits<streamsize>::max(), '\n');
        if (again_inp == negative) return false;
        else if (again_inp == positive) return true;
        else showError();
    }
}
int countLines(const string& file_name)
{
    int numLines = 0;
    ifstream in(file_name);
    string unused;
    while (getline(in, unused))
        ++numLines;
    return numLines;
}

int main()
{
    bool again;
    do {
        string file_name;
        cout << "File name : ";
        cin >> file_name;
        const char* main_file_name = file_name.c_str();
        string option;
        do {
            cout << "What to do with file? (view(V) / edit (E) / exit(EX)) ";
            do {
                cin >> option;
            } while (option != "v" && option != "e" && option != "ex");
            if (option == "v") {
                ifstream file(file_name);
                int no;
                string str_to_show;
                if (file.is_open()) {
                    do {
                        no = getSymbol("Number of the line : ");
                    } while (no <= 0 || no > countLines(file_name));
                    for (int i = 0; i < no; ++i) {
                        getline(file, str_to_show);
                    }
                }
                else cout << "\nproblems. cannot open the file\n";
                cout << str_to_show << endl;
                file.close();
            }
            else if (option == "e") {
                int no;

                string new_line;
                string curr_line;

                cout << "\nInput a line to replace : ";
                while (new_line.length() < 1) {
                    getline(cin, new_line);
                }
                ifstream file(file_name);
                ofstream outfile("tmp.txt");

                if (file.is_open()) {
                    do {
                        no = getSymbol("Number of the line : ");
                    } while (no <= 0 || no > countLines(file_name));

                    int ptr = 1;
                    while (!file.eof())
                    {
                        getline(file, curr_line);
                        if (ptr == no) {
                            outfile << new_line << endl;
                        }
                        else {
                            outfile << curr_line << endl;
                        }
                        ++ptr;
                    }
                    file.close();
                    outfile.close();
                    remove(main_file_name);
                    rename("tmp.txt", main_file_name);
                    cout << "\nDone" << endl;
                }
                else cout << "\nproblems. cannot open the file\n";
            }
        } while (option != "ex");

        again = binaryChoice("Continue? (Y/N) ", 'y', 'n');

    } while (again);
    return 0;
}
