#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>
#include <iostream>
#include <regex>
#include <sstream>
#include <fstream>


inline void showHelp()
{
    std::cout << "cp SOURCE DEST\n" << "mv SOURCE DEST\n" 
        << "stat FILE\n" << "chmod MODE FILE\n" << "q to quit" << std::endl;
}


void copy(std::string source, std::string dest)
{

}

void move(std::string source, std::string dest)
{

}

void getFileInfo(std::string filename = "sem4_OS_lab2.cpp")
{
    // check if file exists
    std::ifstream filestream(filename.c_str());
    if (!filestream.good())
    {
        std::cout << "File does not exist";
        return;
    }

    struct stat st;
    stat(filename.c_str(), &st);

    // size of given file
    std::cout << st.st_size << " bytes" << std::endl;

    // file permissions
    const int MOD_LEN = 9;
    char* mod = new char[MOD_LEN];
    mode_t perm = st.st_mode;
    mod[0] = (perm & S_IRUSR) ? 'r' : '-';
    mod[1] = (perm & S_IWUSR) ? 'w' : '-';
    mod[2] = (perm & S_IXUSR) ? 'x' : '-';
    mod[3] = (perm & S_IRGRP) ? 'r' : '-';
    mod[4] = (perm & S_IWGRP) ? 'w' : '-';
    mod[5] = (perm & S_IXGRP) ? 'x' : '-';
    mod[6] = (perm & S_IROTH) ? 'r' : '-';
    mod[7] = (perm & S_IWOTH) ? 'w' : '-';
    mod[8] = (perm & S_IXOTH) ? 'x' : '-';

    std::cout << std::string(mod, MOD_LEN) << std::endl;

    // last modified time 
    char buff[100];
    time_t time = st.st_ctime;
    strftime(buff, 100, "%Y-%m-%d %H:%M:%S", localtime (&time));
    std::cout << "last edit: " << buff << std::endl;
}

void changeFilePermissions(std::string mode, std::string filename = "sem4_OS_lab2.cpp")
{

}

int readAndHandleUserInput()
{
    const std::regex rxcpmv{R"(^(cp|mv)\s[A-Za-z.0-9\-\_\\]+\s[A-Za-z.0-9\-\_]+$)"};
    const std::regex rxchmod{R"(^chmod\s[ugoarwx+-]{3,6}\s[A-Za-z.0-9\-\_]+$)"};
    const std::regex rxstat{R"(^stat\s[A-Za-z.0-9\-\_\\]+$)"};

    std::string inp;

    getline(std::cin, inp);

    if (regex_match(inp, rxcpmv) || regex_match(inp, rxchmod))
    {
        // parse user input
        const int COMMAND_LEN = 3;
        std::string inpparce[COMMAND_LEN];

        int i = 0;
        std::stringstream ssin(inp);        
        while (ssin.good() && i < COMMAND_LEN)
        {
            ssin >> inpparce[i++];
        }

        // check if file exists and call corresponding function
        std::ifstream secondpos(inpparce[1].c_str());
        std::ifstream thirdpos(inpparce[2].c_str());
        if (secondpos.good() && inpparce[0] == "cp")
        {

            // TODO check if directory exists
            
            std::cout << "cp";
            copy();
        }   
        else if (secondpos.good() && inpparce[0] == "mv")
        {

            // TODO check if directory exists

            std::cout << "mv";
            move();
        }
        else if (thirdpos.good() && inpparce[0] == "chmod")
        {
            std::cout << "chmod";
            changeFilePermissions(inpparce[1], inpparce[2]);
        }
        else
        {
            std::cout << "file '" << inpparce[1] << "' does not exist\n";
        }
    }    
    else if (inp == "--help")
    {
        showHelp();
    }
    else if (inp == "q" || inp == "Q")
    {
        return 1;   
    }
    else
    {
        std::cout << inp << ": command not found\n";
    }

    return 0;
}

int main()
{    
    while(true)
    {
        if (readAndHandleUserInput()) break;
    }

    return 0;
}