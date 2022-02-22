#include <fcntl.h>
#include <sys/stat.h>

// for Unix-like systems only
//#include <unistd.h>



int umask(int newmask)
{
	
}

/**
 * @brief 
 * @param pathname 
 * @param flags 
 * @param mode_t Permission bits
 * @return 
*/
//int open(char* pathname, int flags, mode_t mode)
//{
//
//}


int close(int fd)
{

}


size_t read(int fd, void* buf, size_t length)
{

}


size_t read(int fd, const void* buf, size_t length)
{

}

size_t write(int fd, void* buf, size_t length)
{

}

/**
 * @brief 
 * @param fd 
 * @param buf 
 * @param length 
 * @return 
*/
size_t write(int fd, const void* buf, size_t length)
{




}


/**
 * @brief Put read/write pointer
 * @param fd 
 * @param offset 
 * @param whence A place to put the pointer : SEEKSET, SEEK_CUR, SEEKEND
 * @return 
*/
int lseek(int fd, off_t offset, int whence)
{

}


int truncate(const char* pathname, size_t length)
{

}


int truncate(int fd, size_t length)
{

}

int fsync(int fd)
{

}

int fdatasync(int fd)
{

}

/**
 * @brief 
 * @param pathname 
 * @param statbuf 
 * @return 
*/
int stat(const char* pathname, struct stat* statbuf)
{

}

int lstat(const char* pathname, struct stat* statbuf)
{

}

int fstat(int fd, struct stat* statbuf)
{

}

//int chmod(const char* pathname, mode_t mode)
//{
//
//}

//int fchmod(int fd, mode_t mode)
//{
//
//}


int link(const char* origpath, const char* newpath)
{

}

int symlink(const char* origpath, const char* newpath)
{

}

int unlink(char* pathname)
{

}


int unlink(char* pathname)
{

}

int rename(const char* oldpath, const char* newpath)
{

}



int main()
{
	return 0;
}