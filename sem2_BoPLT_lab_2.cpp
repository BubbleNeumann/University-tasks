#include <cctype>
#include <fstream>
#include <vector>

/*
 Automata states
 S - start (first symbol)
 A - required symbol isn't found yet
 B - required symbol is found (lexem is suitable)
 E - lexem isn't suitable (wrong symbol found)
 H - incorrect exit (word couldn't be written in vector)
 F - correct exit (word could be written in vector)
 */
enum AState { S, A, B, E, H, F };

AState matrix[4][6]
{
  // S, A, B, E, H, F
	{B, B, B, E, H, F}, // required alpha
	{A, A, B, E, H, F}, // other alfa
	{E, E, E, E, H, H}, // special character or digit
	{H, H, F, H, H, F}  // space, tab, EOL
};

int getPath(char curr, char first)
{
	if (std::isspace(curr) || curr == '\t' || curr == '\0' || curr == '\n') return 3;
	if (!((curr >= 'a' && curr <= 'z') || (curr >= 'A' && curr <= 'Z'))) return 2;
	if (curr == first) return 0;
	return 1;
}

std::vector<char*> lexAnalysis(char* str)
{
	std::vector<char*> result;
	int pos = 0; // current position
	int firstPos; // lexeme beginning
	AState state = S;

	do {
		// lexeme initialization
		if (state == S && str[pos] != ' ' && str[pos] != '\t' && str[pos] != '\n')
		{
			firstPos = pos;
			state = A;
		}

		// walk through matrix states
		if (pos != firstPos)
		{
			state = matrix[getPath(str[pos], str[firstPos])][state];
		}

		// remember the lexeme if it's suitable (in 'F' state), initialize the new one
		if (state == F)
		{
			char* lexeme = new char[pos - firstPos + 1];			
			int t1 = firstPos;
			for (int i = 0; i < pos - firstPos; i++, t1++)
			{
				lexeme[i] = str[t1];
			}

			lexeme[pos - firstPos] = '\0';
			result.push_back(lexeme);
			state = S;
		}
		if (state == H) state = S;
		
	} while (str[pos++] != '\0');
	return result;
}

char* getSymbols()
{
	std::ifstream fromf("input.txt", std::ios::binary);
	char* line;
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

void print(std::vector<char*> words)
{
	std::ofstream inf("output.txt");
	if (inf.is_open())
	{
		for (unsigned int i = 0; i < words.size(); ++i)
		{
			inf << words[i] << " ";
		}
		inf.close();
	}
}

int main()
{
	char* str = getSymbols();
	std::vector<char*> list = lexAnalysis(str);
	print(list);
	
	delete [] str;
	for (unsigned int i = 0; i < list.size(); i++) 
	{
		delete [] list[i];
	}
	return 0;
}
