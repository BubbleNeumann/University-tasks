#include <iostream>
#include <string>
#include <sys/types.h>
#include <unistd.h>
#include <cstring>
#include <regex>

int pipe_in[2];
int pipe_out[2];

struct userData
{
	double leftBorder;
	double rightBorder;
	int numberOfSplits;
};

void showHelp(const std::string request)
{
	std::cout << "Given programm calculates an integral of x^2 in borders set by user.\n
                  Now you're expected to provide " << request << std::endl;
}

double integrate(double a, double b, int n)
{
	double result = 0;
	double h = (b - a) / n;

	for (int x = a, int i = 0; i < n; ++i, x += h)
	{
		result += h * (x * x + (x + h) * (x + h)) / 2;
	}

	return result;
}

int readNum(const std::string mod)
{
	std::string userInp;
    const std::regex rxint{R"(^[0-9]+$)"};
    const std::regex rxdouble{R"(^[0-9]*(?:\.[0-9]+)?$)"};

    while (true)
    {
        getline(std::cin, userInp);
        if (userInp == "--help" || userInp == "help" || userInp == "h")
            showHelp(mod);
        else if (mod == "int" && regex_match(userInp, rxint))
            return std::stoi(userInp);
        else if (mod == "double" && regex_match(userInp, rxdouble))
            return std::stod(userInp);
        else
            std::cout << "input is not valid\n";
    }
}

void client()
{
    userData data;
	data.leftBorder = readNum("double");
	data.rightBorder = readNum("double");
	data.numberOfSplits = readNum("int");

    if (data.leftBorder > data.rightBorder)
        std::swap(data.leftBorder, data. rightBorder);

	write(pipe_in[1], &data, sizeof(userData));

	double result;
	read(pipe_out[0], &result, sizeof(double));

	std::cout << result << std::endl;
	exit(0);
}

void server()
{
	userData data;
	read(pipe_in[0], &data, sizeof(userData));
    double res = integrate(data.leftBorder, data.rightBorder, data.numberOfSplits);
	write(pipe_out[1], &res, sizeof(double));
    exit(0);
}

int main()
{    
    pipe(pipe_in);
	pipe(pipe_out);

    switch(fork())
    {
        case -1:
            std::cout << "can't fork the process";
            exit(1);
        case 0:            
            server(); // call to server side in child-process
        default:            
            client();   // call to client side in parent process
    }  

    for (int i = 0; i < 2; ++i)
	{
		close(pipe_in[i]);
		close(pipe_out[i]);
	}      

	return 0;
}