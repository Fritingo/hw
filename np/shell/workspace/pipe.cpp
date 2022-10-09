#include <errno.h>
#include <fcntl.h>
#include <iostream>
#include <signal.h>
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>
#include <vector>

// int process_pipe(std::vector<std::string> cmds)
// {
//     int pipes[]
// }

int main(int argc, char **argv) {

    signal(SIGCHLD,SIG_IGN);
  
    int cmd_num = 3;
    char **cmds[cmd_num];

    char *p1_args[] = {(char*)"ls", NULL};
    cmds[0] = p1_args;

    char *p2_args[] = {(char*)"grep",(char*)"o", NULL}; // 只是 DEMO，所以重複利用
    // for (int i = 1; i < cmd_num; i++)
    //     cmds[i] = p2_args;
    cmds[1] = p2_args;
    char *p3_args[] = {(char*)"grep",(char*)"l", NULL};
    cmds[2] = p3_args; 

    int pipes[(cmd_num-1)*2]; 
    for (int i = 0; i < (cmd_num -1); i++)
        pipe(pipes + i * 2); // 建立 i-th pipe

    pid_t pid;

    for (int i = 0; i < cmd_num; i++) {

        pid = fork();
        if (pid == 0) { // Child
            std::cout << i << "i \n";
            // 讀取端
            if (i != 0) {
                // 用 dup2 將 pipe 讀取端取代成 stdin
                dup2(pipes[(i - 1) * 2], STDIN_FILENO);
            }

            // 用 dup2 將 pipe 寫入端取代成 stdout
            if (i != cmd_num -1) {
                dup2(pipes[i * 2 + 1], STDOUT_FILENO);
            }

            // 全關掉之前一次打開的
            for (int j = 0; j < (cmd_num-1)*2; j++) {
                close(pipes[j]);
            }

            execvp(*cmds[i], cmds[i]);

            // execvp 正確執行的話，程式不會繼續到這裡
            fprintf(stderr, "Cannot run %s\n", *cmds[i]);

        } else { // Parent
            printf("- fork %d\n", pid);

            if (i != 0) { // close
                close(pipes[(i - 1) * 2]);     
                close(pipes[(i - 1) * 2 + 1]); 
            }
        }
    }

    waitpid(pid, NULL, 0); // 等最後一個指令結束

    std::cout << "===" << std::endl;
    std::cout << "All done." << std::endl;
}

