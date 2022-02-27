#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>
#include <iostream>
#include <regex>
#include <sstream>
#include <fstream>

/**
 * @brief show list of available commands
*/
inline void showHelp()
{
    std::cout << "cp SOURCE DEST\n" << "mv SOURCE DEST\n" 
        << "stat FILE\n" << "chmod MODE FILE\n" << "q to quit" << std::endl;
}

/**
 * @brief copy one file content into another
 * @param source source file
 * @param dest new file
 * @return 1 if error occured, 0 if success
*/
int copy(std::string source, std::string dest)
{
	const int BUFSZ = 4096;
    char buf[BUFSZ];
    
    // open file for reading
    int readfile;
    if ((readfile = open(source.c_str(), O_RDONLY)) == -1)
    {
        return 1;
    }

    // open file or create one if does not exists for writing
    int writefile;
    if ((writefile = open(dest.c_str(), O_WRONLY | O_CREAT)) == -1)
    {
        return 1;
    }

    size_t rbytes, wbytes;

    // read() returns 0 when reaches EOF and -1 if error occurs
    while ((rbytes = read(readfile, buffer, BUFSZ)) > 0)
    {
        wbytes = write(w_fd, buf, rbytes);
    }
    
    close(readfile);
    close(writefile);

    return 0;
}

/**
 * @brief copy file to dest directory, then remove original
 * @param source 
 * @param dest 
 * @return 1 if error occured, 0 if success
*/
int move(std::string source, std::string dest)
{
    return (copy(source, dest) == -1 || unlink(source.c_str()) == -1);    
}

/**
 * @brief 
 * @param filename 
*/
void getFileInfo(std::string filename)
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

    delete [] mod;
}

/**
 * @brief 
 * @param mode new permissions to assign
 * @param filename 
*/
void changeFilePermissions(std::string mode, std::string filename)
{
    const std::string MODES = { "---", "--x", "-w-", "-wx", "r--", "r-x", "rw-", "rwx" };

    // if mode format consists of digits, change format to rwxrwxrwx
    if (mode.length() == 3)
    {
        int mask = std::stoi(mode);
        mode = "";
        while (mask)
        {
            mode += conversion[mask % 10];
            mask /= 10;
        }
    }

    // generate permission code
    int perm = 0;
    for (int i = 0, int bin = 256; i < mask.length(); i++, bin /=2)
    {
        if (mask[i] != "-")
        {
            perm += bin;
        }
    }

    chmod(filename.c_str(), perm);
}

/**
 * @brief parse user input and call corresponding function
 * @return 1 if quit and 0 if continue asking user for input
*/
int readAndHandleUserInput()
{
    const std::regex rxcpmv{R"(^(cp|mv)\s[A-Za-z.0-9\-\_\\]+\s[A-Za-z.0-9\-\_]+$)"};
    const std::regex rxchmod{R"(^chmod\s(([ugoarwx+-]{3,6})|(([0-7])([0-7])([0-7])))\s[A-Za-z.0-9\-\_]+$)"};
    const std::regex rxstat{R"(^stat\s[A-Za-z.0-9\-\_\\]+$)"};

    std::string inp;
    getline(std::cin, inp);

    if (regex_match(inp, rxcpmv) || regex_match(inp, rxchmod) || regex_match(inp, rxstat))
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
		struct stat st;
        std::ifstream secondpos(inpparce[1].c_str());
        std::ifstream thirdpos(inpparce[2].c_str());
        if (inpparce[0] == "cp" && secondpos.good())
        {
		    if (copy(inpparce[1], inpparce[2]))
            {
                std::cout << "error writing data\n";
            }
        }   
        else if (inpparce[0] == "mv" && secondpos.good())
        {
            if (move())
            {
                std::cout << "error moving file\n";
            }
        }
        else if (inpparce[0] == "chmod" && thirdpos.good())
        {
            std::cout << "chmod";
            changeFilePermissions(inpparce[1], inpparce[2]);
        }
        else if (thirdpos.good() && inpparce[0] == "chmod")
        {
            std::cout << "chmod";
            changeFilePermissions(inpparce[1], inpparce[2]);
        }
        else
        {
            std::cout << "file '" << inpparce[1] << "' does not exist or command isn't correct\n";
        }

        secondpos.close();
        thirdpos.close();
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