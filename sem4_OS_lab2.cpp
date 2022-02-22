#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>
#include <iostream>
#include <time.h>


void showHelp()
{
    std::cout << "cp SOURCE DEST\n" << "mv SOURCE DEST\n" 
        << "stat FILE\n"<< "chmod MODE FILE" << std::endl;
}


void copy(std::string source, std::string dest)
{

}

void move(std::string source, std::string dest)
{

}

void getFileInfo(std::string filename = "sem4_OS_lab2.cpp")
{
    // convert std::string to const char*
    const char* chfilename = filename.c_str();

    struct stat st;
    stat(chfilename, &st);

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

void changeFilePermissions(std::string mode, std::string filename)
{

}


int main()
{
    
    getFileInfo();

    // showHelp();

    return 0;
}