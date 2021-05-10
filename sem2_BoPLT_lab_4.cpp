#include <cstring>
#include <fstream>
#include <vector>
#include <ctype.h>

/*
 Automata states
 S - start (first symbol)
 A - correct letter found (possible kw or id)
 B - digit found (vl lexeme type)
 E - error (wl)
 H - correct exit (got the string of special chracters)
 F - correct exit (possible kw or id)
 HsA - previous correct "word" lexeme, now delimiter character found
 HsB - previous correct "const" lexeme, now delimiter character found
 */
enum AState { S, A, B, C, E, M, F, G, H, Ef, Hs, HsA, HsB, HsC };

const char lex_name[14][3]{ "if", "th", "ei", "en", "no", "vl",
        "lo", "co", "ao", "id", "eq", "sc", "wl" };

// idC - for condition statement
// idO - for arithmetical exptession
enum LexType { IF, TH, EI, EN, NO, vl, lo, co, ao, id, eq, sc, wl, Er, L, idC, idO, idE};


const AState st[6][6]
{
    // S, A, B, C, E, M
      {A, A, E,HsC, E, HsC},    // alpha
      {B, E, B,HsC, E, HsC},    // digit    
      {C,E,E, C, E, HsC},       // special character
      {S, F, G, H, Ef, H},      // space, tab, EOL
      {Hs,HsA,HsB,HsC,Ef, HsC}, // special character, which is a separator
      {M, HsA, HsB, HsC, Ef, M} // special separator which could be paired
};

const LexType type[12][16]
{
  // the previous lexeme type:
  // L, IF, TH, EI, EN, NO, vl, lo, co, ao, id, eq, sc, idC, idO, idE
    {IF,Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er}, // IF
    {Er,Er, Er, Er, Er, Er, Er, Er, Er, Er, TH, Er, Er, TH, Er, Er}, // TH
    {Er,Er, Er, Er, Er, Er, Er, Er, Er, Er, EI, Er, Er, Er, EI, Er}, // EI
    {Er,Er, Er, Er, Er, Er, EN, Er, Er, Er, EN, Er, Er, Er, EN, Er}, // EN
    {Er,NO, Er, NO, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er}, // NO
    {Er,Er, Er, Er, Er, Er, Er, Er, vl, vl, Er, vl, Er, Er, Er, Er}, // vl
    {Er,Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, lo, Er, Er}, // lo
    {Er,Er, Er, Er, Er, Er, Er, Er, Er, Er, co, Er, Er, co, Er, Er}, // co
    {Er,Er, Er, Er, Er, Er, ao, Er, Er, Er, Er, Er, Er, Er, ao, Er}, // ao
    {Er,idC,idE,idC,Er, idC,Er, idC,id, id, Er, idO,Er, Er, Er, idO}, // id
    {Er,Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, eq}, // eq
    {Er,Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er, Er}  // sc
};

int getPath(char curr, char first)
{
    if (isspace(curr) || curr == '\t' || curr == '\0' || curr == '\n') return 3;
    if ((curr >= 'a' && curr <= 'z') || (curr >= 'A' && curr <= 'Z')) return 0;
    if (isdigit(curr)) return 1;
    if (curr == '+' || curr == '-' || curr == '*' || curr == '/' || curr == '=' || curr == ';') return 4;
    if (curr == '>' || curr == '<') return 5;

    return 2;
}

struct Lex
{
    LexType type;
    char* body;
};

// called for the lexemes which only consist of Latin letters
int wordType(const Lex& a)
{
    if (!strcmp(a.body, "if")) return IF;
    if (!strcmp(a.body, "then")) return TH;
    if (!strcmp(a.body, "elseif")) return EI;
    if (!strcmp(a.body, "end")) return EN;
    if (!strcmp(a.body, "not")) return NO;
    if (!strcmp(a.body, "and") || !strcmp(a.body, "or")) return lo;

    return id;
}

// called for the lexemes which consist of special characters
int coType(const Lex& a)
{
    if (!strcmp(a.body, "<") || !strcmp(a.body, "<=")) return co;
    if (!strcmp(a.body, ">") || !strcmp(a.body, ">=")) return co;
    if (!strcmp(a.body, "<>")) return co;

    if (!strcmp(a.body, "+") || !strcmp(a.body, "-")) return ao;
    if (!strcmp(a.body, "*") || !strcmp(a.body, "/")) return ao;

    if (!strcmp(a.body, "=")) return eq;
    if (!strcmp(a.body, ";")) return sc;

    return wl;
}

// add new lexeme to the vector
void addLex(std::vector<Lex>& result, AState& state, char* lexeme)
{
    Lex lex;
    lex.body = lexeme;

    if (state == F || state == HsA)
    {
        lex.type = (LexType)wordType(lex);
    }

    if (state == G || state == HsB)
    {
        lex.type = vl;
    }

    if (state == H || state == HsC || state == Hs)
    {
        lex.type = (LexType)coType(lex);
    }

    if (state == Ef)
    {
        lex.type = wl;
    }
    result.push_back(lex);
    state = S;
}

void lexAnalysis(std::vector<Lex>& result, char*& str)
{
    int pos = 0; // current position
    int firstPos; // lexeme beginning
    AState state = S;
    do {

        // lexeme initialization
        if (state == S && str[pos] != ' ' && str[pos] != '\t' && str[pos] != '\n')
        {
            firstPos = pos;
        }

        // walk through matrix states
        state = st[getPath(str[pos], str[firstPos])][state];

        // remember the lexeme if end state is reached
        if (state == F || state == G || state == H || state == HsA || state == HsB || state == HsC || state == Ef)
        {
            char* lexeme = new char[pos - firstPos + 1];
            int t1 = firstPos;
            for (int i = 0; i < pos - firstPos; i++, t1++)
            {
                lexeme[i] = str[t1];
            }
            lexeme[pos - firstPos] = '\0';

            // if needed to start a new lexeme with a current symbol
            if (state == HsA || state == HsB || state == HsC) --pos;
            addLex(result, state, lexeme);
        }

        // automata state which is needed to write down just the current symbol
        if (state == Hs)
        {
            char* lexeme = new char[2];
            lexeme[0] = str[pos];
            lexeme[1] = '\0';
            addLex(result, state, lexeme);
        }

    } while (str[pos++] != '\0');
}

// th efunction
void syntaxAnalysis(std::vector<Lex>& vect, std::ofstream& inf)
{

    // the beginning of the construction
    LexType state = L;

    // size_t: alias of unsigned integer type
    for (size_t i = 0; i < vect.size(); ++i)
    {
        if (vect[i].type != wl) state = type[vect[i].type][state];
        
        if (state == Er || vect[i].type == wl)
        {
            
        }
        else if (state == EN)
        {
            if (i == vect.size() - 1) inf << "\nOK";
            else state = L;
        }

    }

}

// read the content of the .txt file 
char* getSymbols()
{
    std::ifstream fromf("input.txt", std::ios::binary);
    char* line = NULL;
    if (fromf.is_open())
    {
        int size = 0;

        // set the pointer at 0 position from the end of a stream
        fromf.seekg(0, std::ios::end);

        // get the file's size (returns the current position of the get pointer)
        size = fromf.tellg();
        line = new char[size + 1];

        // set the pointer at 0 position from the beginning of a stream
        fromf.seekg(0, std::ios::beg);

        // extracts characters from stream and stores them into locations of the array
        fromf.read(&line[0], size);
        line[size] = '\0';
        fromf.close();
    }
    return line;
}

void printLexemeList(std::vector<Lex>& v, std::ofstream& inf)
{
    for (size_t i = 0; i < v.size(); ++i) 
    {
        inf << v[i].body << '[' << lex_name[v[i].type] << ']' << ' ';
    }
}

int main()
{
    char* str = getSymbols();
    std::vector<Lex> list;
    lexAnalysis(list, str);
    
    std::ofstream inf("output.txt");

    printLexemeList(list, inf);

    // function also puts the second row to the output file
    syntaxAnalysis(list, inf);

    inf.close();

    delete[] str;
    for (unsigned int i = 0; i < list.size(); i++)
    {
        delete[] list[i].body;
    }
    return 0;
}