#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>
#include <iostream>
#include <regex>
#include <sstream>
#include <fstream>
#include <filesystem>

/**
 * @brief show list of available commands
*/
inline void showHelp()
{
    std::cout << "cp SOURCE DEST\n" << "mv SOURCE DEST\n" 
        << "stat FILE\n" << "chmod MODE FILE\n" << "q to quit" << std::endl;
}

/**
 * @brief copy one file content into another or to another directory
 * @param source source file
 * @param dest where to put a new file
 * @return 1 if error occured, 0 if success
*/
int copy(std::string source, std::string dest)
{
	const int BUFSZ = 65536;
    // char *buf = malloc(BUFSZ);
    char buf[BUFSZ];
    // like mkdir, rmdir, return 0 for success, -1 for failure
    // if (!buf) return -1; 
    // FILE *hin = fopen(source.c_str(), "rb");

    // open file in ifstream consructor
    std::ifstream fileread(source.c_str());
    if (!fileread.good())
	{
		return 1;
	}

    // FILE *hout = fopen(dest.c_str(), "wb");
    
    std::ofstream filewrite(dest.c_str());    
    if (!filewrite.good())
	{
        fileread.close();
		return 1;
	}

    unsigned int buflen;
    while ((buflen = fread(buf, 1, BUFSZ)) > 0)
	{
        if (buflen != fwrite(buf, 1, buflen))
		{


            // fclose(hout);
            // fclose(hin);
            // free(buf);
            // IO error writing data
            return 1; 
        }
    }

    fwrite.close();

    // free(buf);
	// check if fread had indicated IO error on input
    // int r = ferror(hin) ? -1 : 0; 
    // fclose(hin);
	// final case: check if IO error flushing buffer -- don't omit this really can happen; calling `fflush()` won't help.
    // return fclose(hout) ? -1 : 0; 
    return 0;
}

/**
 * @brief 
 * @param source 
 * @param dest 
*/
void move(std::string source, std::string dest)
{

  

}

/**
 * @brief 
 * @param filename 
*/
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
    // const int MOD_LEN = 9;
    // char* mod = new char[MOD_LEN];
    // mode_t perm = st.st_mode;
    // mod[0] = (perm & S_IRUSR) ? 'r' : '-';
    // mod[1] = (perm & S_IWUSR) ? 'w' : '-';
    // mod[2] = (perm & S_IXUSR) ? 'x' : '-';
    // mod[3] = (perm & S_IRGRP) ? 'r' : '-';
    // mod[4] = (perm & S_IWGRP) ? 'w' : '-';
    // mod[5] = (perm & S_IXGRP) ? 'x' : '-';
    // mod[6] = (perm & S_IROTH) ? 'r' : '-';
    // mod[7] = (perm & S_IWOTH) ? 'w' : '-';
    // mod[8] = (perm & S_IXOTH) ? 'x' : '-';

    // std::cout << std::string(mod, MOD_LEN) << std::endl;

    std::cout << std::filesystem::status(filename.c_str().permissions())

    // last modified time 
    char buff[100];
    time_t time = st.st_ctime;
    strftime(buff, 100, "%Y-%m-%d %H:%M:%S", localtime (&time));
    std::cout << "last edit: " << buff << std::endl;

    delete [] mod;
}

/**
 * @brief 
 * @param mode new permissions
 * @param filename 
*/
void changeFilePermissions(std::string mode, std::string filename = "sem4_OS_lab2.cpp")
{

    chmod(filename.c_str());

}

/**
 * @brief 
 * @return 
*/
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
		struct stat st;
        std::ifstream secondpos(inpparce[1].c_str());
        std::ifstream thirdpos(inpparce[2].c_str());
        if (inpparce[0] == "cp" && secondpos.good())
        {
			// check if directory exists
			if ((stat(thirdpos, &myStat) == 0) && (((myStat.st_mode) & S_IFMT) == S_IFDIR)) {
				std::cout << "cp";
            	if (copy(inpparce[1], inpparce[2]))
                {
                    std::cout << "error writing data\n";
                }
			}
			else{
				std::cout << "directory " << inpparce[2] << " does not exist\n";
			}
        }   
        else if (inpparce[0] == "mv" && secondpos.good())
        {
            // check if directory exists
			if ((stat(thirdpos, &myStat) == 0) && (((myStat.st_mode) & S_IFMT) == S_IFDIR)) {
				std::cout << "mv";
            	move();
			}
			else{
				std::cout << "directory " << inpparce[2] << " does not exist\n";
			}
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