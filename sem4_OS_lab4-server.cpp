#pragma comment(lib, "ws2_32.lib")
#include <winsock2.h>
#include <iostream>
#include <string>

#pragma warning(disable: 4996) // disabling inet_addr() exc

std::string decrypte(const std::string& encrypted_msg, int key)
{
	const int MOD = 26;	
	if (key >= MOD) key %= MOD;

	std::string decrypted_msg;
	for (char c : encrypted_msg)
	{
		if (c >= 'a' && c <= 'z')
		{
			(c - key >= 'a') ? decrypted_msg += c - key : decrypted_msg += 'z' + (c - 'a' + 1) - key;
		}
		else if (c >= 'A' && c <= 'Z')
		{
			(c - key >= 'A') ? decrypted_msg += c - key : decrypted_msg += 'Z' + (c - 'A' + 1) - key;
		}
		else
			decrypted_msg += c;
	}

	return decrypted_msg;
}

int main()
{
	WSAData wsaData;
	
	// start up the library, where MAKEWORD(2, 1) is WinSock library version
	if (WSAStartup(MAKEWORD(2, 1), &wsaData))
	{
		std::cout << "library startup error\n";
		exit(1);
	}

	// save the socket address
	SOCKADDR_IN addr; 
	int sizeofaddr = sizeof(addr);
	addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // save an ip (local host)
	addr.sin_port = htons(1111); // id port for incoming data
	addr.sin_family = AF_INET; // internet protocols family 	
							   
	// connection protocol
	// create a new socket 
	SOCKET sListen = socket(AF_INET, SOCK_STREAM, NULL);

	// bind the local address and the socket
	// (SOCKADDR*)&addr - pointer to the sockaddr structure to which the connection should be established
	bind(sListen, (SOCKADDR*)&addr, sizeof(addr));
	
	// places a socket in a state in which it is listening for an incoming connection
	listen(sListen, SOMAXCONN);

	// accept returns a new socket pointer, will be used for data exchange with client,
	// permits an incoming connection attempt on a socket
	SOCKET newConnection = accept(sListen, (SOCKADDR*)&addr, &sizeofaddr);

	if (!newConnection)
	{
		std::cout << "server can't connect to the client\n";
		exit(1);
	}
	else
	{
		std::cout << "server connection is sucessful\n";
		
		int shift;
		char shiftchar[10];
		recv(newConnection, shiftchar, sizeof(shift), NULL);

		shift = atoi(shiftchar);

		char msg[256];

		while (true)
		{
			recv(newConnection, msg, sizeof(msg), NULL);
			std::string decmsg = decrypte(msg, shift);
			if (decmsg == "Exit" || decmsg == "exit" || decmsg == "ex")
			{				
				std::cout << "> exiting\n";
				break;
			}

			std::cout << "enc message: " << msg << std::endl;
			std::cout << "dec messege: " << decmsg << "\n";
		}
	}
	
	closesocket(sListen);
	closesocket(newConnection);
	WSACleanup();

	return 0;
}
