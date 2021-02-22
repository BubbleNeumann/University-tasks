#include <iostream>
#include <fstream>
#include <string>
#include <regex>

using namespace std;

bool binaryChoice(const string &request, char positive, char negative) {
    char again_inp;
    cout << request;
    while (true) {
        cin >> again_inp;
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        if (again_inp == negative) { return false; }
        else if (again_inp == positive) { return true; }
        else {
            cout << "Invalid input. Try again" << endl;
        }
    }
}

int countLines(const string &file_name) {
    int numLines = 0;
    ifstream in(file_name);
    string unused;
    while (getline(in, unused))
        ++numLines;
    return numLines;
}

class Date {

    int y, m, d;
public:

    void setDate(const string &file_inp) {
        const regex rx_date{R"(^(\d\d)[\.](\d\d)[\.](\d{4})$)"};
        string date_str;
        bool date_inp_correct;
        do {
            date_inp_correct = true;
            if (!file_inp.empty()) {
                date_str = file_inp;
                if (!regex_match(date_str, rx_date)) {
                    cout << "\nIncorrect date format in file\n";
                    date_inp_correct = false;
                }
            } else {
                cout << "Enter the date in format \\DD.MM.YYYY\\: ";
                do {
                    getline(cin, date_str);
                } while (!regex_match(date_str, rx_date));
            }

            if (date_inp_correct) {
                this->y = stoi(date_str.substr(6));
                this->m = stoi(date_str.substr(3, 5));
                this->d = stoi(date_str.substr(0, 2));
                date_inp_correct = !(this->m > 12 || this->m < 1 || this->d > 31 || (this->m == 2 and this->d > 29));
            }

        } while (!date_inp_correct && file_inp.empty());
        if (!date_inp_correct) {
            this->y = 0;
            this->m = 0;
            this->d = 0;
        }
    }

    int year() { return y; }

    int month() { return m; }

    int day() { return d; }

    friend ostream &operator<<(ostream &os, Date date);
};

ostream &operator<<(ostream &os, Date date) {
    return os << date.day() << '.' << date.month() << '.' << date.year();
}

struct Time {
    int h, m;
    bool inp_correct;

    void setTime(const string &user_request, const string &file_inp) {

        string time_str;
        const regex rx_time{R"(^(\d\d)[\.](\d\d)$)"};

        do {
            this->inp_correct = true;
            if (!file_inp.empty()) {
                if (!regex_match(file_inp, rx_time)) {
                    cout << "Incorrect time format in file\n";
                    this->inp_correct = false;
                }
                time_str = file_inp;
            } else {
                cout << user_request;
                do {
                    getline(cin, time_str);
                } while (!regex_match(time_str, rx_time));
            }

            if (this->inp_correct) {
                this->h = stoi(time_str.substr(0, 2));
                this->m = stoi(time_str.substr(3));
                this->inp_correct = !(this->h > 23 || this->m > 59);
            }

        } while (!(this->inp_correct) && file_inp.empty());
    }

    friend ostream &operator<<(ostream &os, const Time &time);
};

ostream &operator<<(ostream &os, const Time &time) {
    return os << time.h << '.' << time.m;
}

class WorkDay {

    Date curr_date;
    Time time_start, time_end, duration;

public:

    void consoleInit() {
        curr_date.setDate("");
        time_start.setTime("Time the work day started in format \\HH.MM\\: ", "");
        time_end.setTime("Time the work day ended in format \\HH.MM\\: ", "");
    }

    void fileInit() {

        cout << "Enter the input file name: ";
        string file_name;
        getline(cin, file_name);
        ifstream file(file_name);
        if (file.is_open()) {
            if (countLines(file_name) == 3) {
                string date_str, time_start_str, time_end_str;

                getline(file, date_str);
                curr_date.setDate(date_str);

                getline(file, time_start_str);
                time_start.setTime("", time_start_str);

                getline(file, time_end_str);
                time_end.setTime("", time_end_str);
            } else {
                cout << "\nIncorrect data format in file;\n";
            }
            file.close();
        } else {
            cout << "Unable to open the file\n";
        }
    }

    void calculateDuration() {
        if (time_start.inp_correct && time_end.inp_correct) {
            if (time_end.h < time_start.h) {
                time_end.h += 24;
            }
            duration.h = time_end.h - time_start.h;
            if (time_end.m < time_start.m) {
                time_end.m += 60;
                --duration.h;
            }
            duration.m = time_end.m - time_start.m;
        } else {
            duration.h = 0;
            duration.m = 0;
        }
    }

    Date date() { return curr_date; }

    Time timeStart() { return time_start; }

    Time timeEnd() { return time_end; }

    Time workDayDuration() {
        calculateDuration();
        return duration;
    }
};

int main() {
    bool again;

    do {
        WorkDay today;
        bool read_from_file = binaryChoice("Get data from file? (Y/N) ", 'y', 'n');
        if (read_from_file) {
            today.fileInit();
        } else {
            today.consoleInit();
        }

        bool write_to_file = binaryChoice("Write the answer to the file? (Y/N)", 'y', 'n');
        if (write_to_file) {
            string file_name;
            cout << "Enter the output file name: ";
            getline(cin, file_name);
            ofstream file(file_name);
            if (file.is_open()) {
                file << today.date() << endl;
                file << today.workDayDuration();
                file.close();
            } else {
                cout << "Unable to open the file\n";
            }
        } else {
            cout << today.date() << " the work day last " << today.workDayDuration() << " hours.";
        }

        again = binaryChoice("\nContinue? (Y/N) ", 'y', 'n');

    } while (again);

    return 0;
}
