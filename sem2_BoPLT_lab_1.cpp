#include <fstream>
#include <vector>

std::vector<char*> getWords(char* text, int len) {
    std::vector<char*> list;
    char* word = NULL;
    char* check;
    char* a;
    int word_len = 0;
    bool suitable = false;
    for (int i = 0; i < len; ++i) {

        if (text[i] == ' ' || text[i] == '\t' || text[i] == '\n' || text[i] == EOF) {
            if (suitable) {
                a = new char[word_len + 1];
                for (int j = 0; j < word_len; ++j) a[j] = word[j];
                a[word_len] = '\0';
                list.push_back(a);
                suitable = false;
            }
            word_len = 0;
        }
        else {
            check = (char*)realloc(word, ++word_len * sizeof(char));
            if (check != nullptr) {
                word = check;
                word[word_len - 1] = text[i];
                if (word_len > 1 && word[word_len - 1] == word[0]) suitable = true;
            }
        }
    }
    return list;
}

int main() {
    std::ifstream fromf("input.txt");
    std::ofstream inf("output.txt");
    if (fromf.is_open() && inf.is_open()) {
        char* letters = nullptr;
        char* check;
        int length = 0;
        for (; true; ++length) { 
            check = (char*)realloc(letters, (length+1) * sizeof(char));
            if (check != nullptr) {
                letters = check;
                letters[length] = fromf.get();
                if (letters[length] == EOF) {
                    ++length;
                    break;
                }
            }
        }

        std::vector<char*> list = getWords(letters, length);
        for (unsigned int i = 0; i < list.size(); ++i) inf << list[i] << ' ';
        free(letters);
    }
    return 0;
}