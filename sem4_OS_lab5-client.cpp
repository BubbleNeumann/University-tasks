#include <Windows.h>
#include <iostream>
#include <random>

int main()
{
	DWORD dwBytes;
	HANDLE pipe;

	do {
		pipe = CreateFile(TEXT("\\\\.\\pipe\\mypipe1"), GENERIC_READ | GENERIC_WRITE, NULL,	NULL, OPEN_EXISTING, NULL, NULL);
		Sleep(1000);
	} while (pipe == INVALID_HANDLE_VALUE);

	std::random_device rd; // seed the random number generator object
	std::mt19937 mt(rd()); // requests for random data to OS
	std::uniform_int_distribution<int> dist(5, 10);
	
	int timeToHeal = dist(mt);
	
	if (!WriteFile(pipe, &timeToHeal, sizeof(int), &dwBytes, NULL))
	{
		std::cout << "can't write to file\n";
		CloseHandle(pipe);
		return 1;
	}

	CloseHandle(pipe);
	return 0;
}
