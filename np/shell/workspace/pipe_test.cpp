

#include <unistd.h>
#include <iostream>
#include <string>
#include <cstring>
#include <sstream>
#include <signal.h>
#include <vector>
#include <algorithm>
#include <sys/wait.h>
#include <sys/stat.h> 
#include <fcntl.h>

#define MAX_WORDS_IN_LINE 1000
#define BUFF_SIZE 100000

void sing_handler(int signal)
{
    std::cout << "over " << getpid() << "\n";
    _exit;
}

int main()
{
    int status;
    int pipeline1[2];
    int pipeline2[2];
    int fd;
    pipe(pipeline1);
    pipe(pipeline2);

    signal(SIGCHLD,SIG_IGN);
    pid_t pid_A, pid_B, pid_C;

    if( !(pid_A = fork()) )
    {
        dup2(pipeline1[1], STDOUT_FILENO);
        close(pipeline1[0]);
        close(pipeline1[1]);
        char* arg[] = {(char*)"ls",NULL};
        execvp(arg[0],arg);
    }

    if( !(pid_B = fork()) )
    {
        
        dup2(pipeline1[0], STDIN_FILENO);
        close(pipeline1[0]);
        close(pipeline1[1]);
        char* arg[] = {(char*)"grep",(char*)"o",NULL};
        execvp(arg[0],arg);
        int newstdout = creat("out.txt",0644);
        close(pipeline1[1]);
        dup(newstdout);
        close(newstdout);
    }

    // if( !(pid_C = fork()) )
    // {
    //     dup2(pipeline1[0], 0);
    //     close(pipeline1[0]);
    //     close(pipeline1[1]);
    //     char* arg[] = {(char*)"grep",(char*)"l",NULL};
    //     execvp(arg[0],arg);
    // }


}