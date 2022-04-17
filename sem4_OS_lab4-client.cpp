#pragma comment(lib, "ws2_32.lib")
#include <winsock2.h>
#include <iostream>
#include <string>

#pragma warning(disable: 4996) // disabling inet_addr() exc

std::string encrypte(const std::string& msg, int key)
{
	const int MOD = 26;
	if (key >= MOD) key %= MOD;

	std::string encrypted_msg;
	for (char c : msg)
	{
		if (c >= 'a' && c <= 'z')
		{
			(c + key <= 'z') ? encrypted_msg += c + key : encrypted_msg += 'a' - ('z' - c + 1) + key;
		}
		else if (c >= 'A' && c <= 'Z')
		{
			(c + key <= 'Z') ? encrypted_msg += c + key : encrypted_msg += 'A' - ('Z' - c + 1) + key;
		}
		else
			encrypted_msg += c;
	}

	return encrypted_msg;
}

int main()
{
	WSAData wsaData;
	if (WSAStartup(MAKEWORD(2, 1), &wsaData))
	{
		std::cout << "library startup error\n";
		exit(1);
	}

	SOCKADDR_IN addr;
	int sizeofaddr = sizeof(addr);
	addr.sin_addr.s_addr = inet_addr("127.0.0.1");	
	addr.sin_port = htons(1111);
	addr.sin_family = AF_INET;

	SOCKET connection = socket(AF_INET, SOCK_STREAM, NULL); // descriptor identifying an unconnected socket
	if (connect(connection, (SOCKADDR*)&addr, sizeof(addr)))
	{
		std::cout << "client can't connect to the server\n";
		exit(1);
	}
	
	std::cout << "client connection is sucessful\n";
	
	const int SHIFT = 4;

	send(connection, std::to_string(SHIFT).c_str(), sizeof(SHIFT), NULL);

	while (true)
	{
		std::cout << "Your message:\n";
		std::string userInput;
		std::getline(std::cin, userInput);
		std::string encrypted_msg = encrypte(userInput, SHIFT);
		
		send(connection, encrypted_msg.c_str(), sizeof(encrypted_msg), NULL);
		
		if (userInput == "Exit" || userInput == "exit" || userInput == "ex")
		{
			std::cout << "> exiting\n";
			break;
		}

		std::cout << "Encrypted message: " << encrypted_msg << std::endl;		
	}

	closesocket(connection);
	WSACleanup();

	return 0;
}
