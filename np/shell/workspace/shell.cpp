#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cstring>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <errno.h>
#include <dirent.h>



// #define MAX_CMD_LINE 80

void InitPath()
{
	setenv("PATH", "bin:.", 1);	
}

typedef struct CMD_Pipe_Follow
{
    std::vector<std::string> cmds;
    int number_pipe;
}cpf;

typedef struct CMD_info
{
    std::vector<std::string> cmd;
    std::vector<int> pipe_index;
    int out = 0;
}cmd_info;

int check_PATH_exec(std::string cmd)
{
    DIR *dir; struct dirent *diread;
    std::vector<char *> files;

    if ((dir = opendir(std::getenv("PATH"))) != nullptr) {
        while ((diread = readdir(dir)) != nullptr) {
            files.push_back(diread->d_name);
        }
        closedir (dir);
    } else {
        perror ("opendir");
        return -1;
    }

    for (std::string file : files)
    {
        if (cmd == file) return 1;
    }

    return -1;
}


int cmd_process(cmd_info cmdss)
{
    signal(SIGCHLD,SIG_IGN);
  
    int cmd_num = 3;
    char **cmds[cmd_num];

    char *p1_args[] = {(char*)"ls", NULL};
    cmds[0] = p1_args;

    char *p2_args[] = {(char*)"cat", NULL}; // 只是 DEMO，所以重複利用
    for (int i = 1; i < cmd_num; i++)
        cmds[i] = p2_args;

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

    waitpid(pid, NULL, 0);



    // -------- handle pipe --------
    // std::cout << "here\n";
    // signal(SIGCHLD,SIG_IGN);

    // int pipes[(cmds.pipe_index.size() - 2) * 2];
    
    // for (int i = 0; i < (cmds.pipe_index.size() - 2); i++)
    //     pipe(pipes + i * 2);

    // pid_t pid;
    // int current_pipe_index = 0;

    // for (int i = 0; i < (cmds.pipe_index.size() - 1); i++) 
    // {
    //     pid = fork();
    //     if(pid < 0) std::cout << "fork error\n";
        
    //     if (pid == 0)  // Child
    //     {
    //         std::cout << "child " << pid  << "i" << i << "\n";
    //         //stdin
    //         if (i != 0)
    //         {
    //             dup2(pipes[(i - 1) * 2], STDIN_FILENO);
    //         }
    //         //stdout
    //         if (i != (cmds.pipe_index.size() - 2))
    //         {
    //             dup2(pipes[i * 2 + 1], STDOUT_FILENO);
    //         }

    //         // close all
    //         for (int j = 0; j < ((cmds.pipe_index.size() - 2) * 2); j++)
    //         {
    //             close(pipes[j]);
    //         }
    //         std::cout << "i " << i << " index " << current_pipe_index<< "\n";
    //         if (current_pipe_index == 0)
    //         {
    //             std::cout << "first\n";
    //             char* arg[cmds.pipe_index[current_pipe_index + 1] - cmds.pipe_index[current_pipe_index] + 1];
    //             for (int k = 0; k < (cmds.pipe_index[current_pipe_index + 1] - cmds.pipe_index[current_pipe_index]); k++)
    //             {
    //                 arg[k] = strdup(cmds.cmd[current_pipe_index + k].c_str());
    //             }
    //             arg[cmds.pipe_index[current_pipe_index + 1] - cmds.pipe_index[current_pipe_index]] = NULL;
    //             current_pipe_index++;
                
    //             execvp(arg[0], arg);
    //         }else
    //         {
    //             std::cout << "others\n";
    //             std::cout << "here" << "\n";
    //             char* arg[cmds.pipe_index[current_pipe_index + 1] - cmds.pipe_index[current_pipe_index]];
    //             for (int k = 0; k < (cmds.pipe_index[current_pipe_index + 1] - cmds.pipe_index[current_pipe_index] - 1); k++)
    //             {
    //                 arg[k] = strdup(cmds.cmd[current_pipe_index + 1 + k].c_str());
    //             }
    //             arg[cmds.pipe_index[current_pipe_index + 1] - cmds.pipe_index[current_pipe_index] - 1] = NULL;
    //             current_pipe_index++;
    //             execvp(arg[0], arg);
    //         }
            
    //     }else // parent
    //     {
    //         std::cout << getpid() <<  " i " << i << "parent \n";
    //         if (i != 0) { // close
    //             close(pipes[(i - 1) * 2]);     
    //             close(pipes[(i - 1) * 2 + 1]); 
    //         }
    //     }

    // }
    // waitpid(pid, NULL, 0);
    // ------
    // char* arg[cmds.cmd.size() + 1];

    // for (int i=0; i<cmds.cmd.size(); i++)
    // {
    //     arg[i] = strdup(cmds.cmd[i].c_str());
    // }
    // arg[cmds.cmd.size()] = NULL;

    // pid_t c_pid = fork();

    // if (c_pid == -1) {
    //     perror("fork");
        
    // } else if (c_pid > 0) {
    //     std::cout << "printed from parent process " << getpid() << "\n";
    //     wait(nullptr);
    // } else {
    //     std::cout << "printed from child process " << getpid() << "\n";
    //     int status_code = execvp(arg[0], arg);
    // }

    //=====
    // if (fork() == 0) {
    //     // Newly spawned child Process. This will be taken over by "ls -l"
    //     int status_code = execvp(arg[0], arg);

    //     printf("ls -l has taken control of this child process. This won't execute unless it terminates abnormally!\n");

    //     if (status_code == -1) {
    //         printf("Terminated Incorrectly\n");
    //         return 1;
    //     }
    // }
    // else {
    //     // Old Parent process. The C program will come here
    //     printf("This line will be printed\n");
    // }    
    return -1;
}


cmd_info sparate_cmd(std::string input)
{
    std::istringstream iss(input);
    cmd_info cmds;
    std::string cmd;
    int pipe_i = 0;
    cmds.pipe_index.push_back(pipe_i);

    while (iss >> cmd)
    {
        cmds.cmd.push_back(cmd);

        if (cmd == "|")
            cmds.pipe_index.push_back(pipe_i);
        pipe_i++;

        if (cmd == ">")
            cmds.out = 1;
    }
    cmds.pipe_index.push_back(pipe_i);

    return cmds;
}

int exec_cmd(cmd_info cmds)
{
    if (cmds.cmd.size() < 1) return 1;
    if (cmds.cmd[0] == "exit")  return 0;
            

    if (cmds.cmd[0] == "printenv" and cmds.cmd.size() == 2){
        std::cout << std::getenv(cmds.cmd[1].c_str()) << "\n";
        return 1;
    }

    if (cmds.cmd[0] == "setenv" and cmds.cmd.size() == 3){
        setenv(cmds.cmd[1].c_str(), cmds.cmd[2].c_str(), 1);
        return 1;
    }

    
    
    if (check_PATH_exec(cmds.cmd[0]) == -1)
    {
        std::cout << "Unknown command: [" << cmds.cmd[0] << "].\n"; 
    }    
    else
    {
        cmd_process(cmds);
    }

    return 1;
}

int read_loop()
{
    while (true)
    {
        std::string input;
        std::cout << "%";
        std::getline(std::cin, input);

        cmd_info cmds = sparate_cmd(input);

        if (exec_cmd(cmds) <= 0)    return(0);

    }
    
}

int main(int argc, char **argv, char **envp){
    InitPath();

    read_loop();
    


    

    return 0;
}

    // char *args[MAX_CMD_LINE/2 +1];
    // int should_run =1;
    // int argc = 0;               //argument count
    
    
    // std::vector<std::string> entered_input;
    // std::vector<std::string> command_history;
    
    // std::string test = "a b  cf : | 5";
    // std::cout << test << "\n";
    // test = test + " EOF";
    // std::cout << test << "\n";
    // std::istringstream iss(test);
    // std::string val;
    // iss >> val;
   
    // while(val != "EOF"){
    //     iss >> val;
    //     std::cout << val << "\n";
    // }
    
    
    // while(should_run == 1){
    //     int status = 1;             //int variable to control to run a process.
        
    //     std::string input;              //user input variable initialize
    //     std::string cmd;
    //     std::cout << "%";
    //     std::getline(std::cin, input);  //capture entire user input line
    //     std::cout << input << input.length() << "\n";
    //     std::istringstream iss(input);  //start tokenizing
    //     std::string InputAfterSpace;                  //capture second input after space

    //     std::vector<std::string *> cmd_list;


    //     iss >> cmd;

    //     if (cmd == "printenv"){
    //         iss >> cmd;
    //         char *envcmd = &cmd[0];
    //         std::cout << std::getenv(envcmd) << "\n";
    //     }

    //     if (cmd == "exit"){
    //         return (0);
    //     }

    //     if (cmd == "setenv"){
    //         iss >> cmd;
    //         char *envcmd = &cmd[0];
    //         iss >> cmd;
    //         char *path = &cmd[0];
    //         std::cout << envcmd << "," << path << "\n";
    //         setenv(envcmd, path, 1);	
    //         std::cout << std::getenv(envcmd) << "\n";
    //     }

        // while ( getline( iss, InputAfterSpace, ' ' ) ) {    //getline with space delimiter
            
            
        //     if(InputAfterSpace == "exit"){              //if user input exit, program stops
        //         std::cout << "Exiting the program..." << std::endl;
                
        //         should_run = 0; //set should run to 0 so gets out of while loop and stop
                
        //     }
            
        //     if(!InputAfterSpace.empty() && (InputAfterSpace != "history")){ //history isnt captured as a shell command.
        //         if(input[0] == '!'){
        //             continue;
        //         }
        //         else{
        //             /*
        //              The token is not history or does not start with exclamation mark
        //              Therefore, it is a shell command and should be stored for the history
        //              feature purposes.
                     
        //              Argc = Argument Count is also increased in order to find index of commands.
                     
        //              */
        //             entered_input.push_back(InputAfterSpace);
        //             command_history.push_back(InputAfterSpace);
        //             argc++;
        //         }
        //     }
            
            
        // }
        // std::string com_arr[argc];                      //allocate array memory for as many as arguments present
        // std::copy(command_history.begin(), command_history.end(), com_arr); //copy vector into array of strings
        
        // if(input == "history"){
        //     /*
             
        //      User types history and wants to see what commands are executed.
        //      They are going to displayed here.
             
        //      If no commands in the history error that to user.
        //      As assignment 1 stated, only last 10 commands to be displayed.
        //      */
            
        //     if(command_history.empty()){
                
        //         std::cout << "No commands in history.." << std::endl;
        //     }
        //     if(command_history.size() > 10)
        //     {
        //         for(int i=argc; i> (command_history.size() -10); i--){
        //             std::cout << i << ": " << com_arr[i-1] << std::endl;
        //         }
        //     }
        //     else
        //     {
        //         for(int i = argc; i>0; i--)
        //         {
        //             std::cout <<  i << ": " << com_arr[i-1] << std::endl;
        //         }
        //     }
        // }
        
        
        // std::string arr[argc];          //allocate array size of argument count
        // std::copy(entered_input.begin(),  entered_input.end(), arr); // copy vector into array of strings
        
        // if(input != "history") {
        //     /*
        //      This is where user inputs actual command such as ps, cal, who, top etc.
        //      and they get executed by the child proccess.
        //      */
            
            
            
        //     if(input[0] == '!' && input[1] != '!'){
                
        //         int num = 0;                    //int variable num, number , to get the number after exclamation mark
        //         std::string hold = &input[1];   //get the number after ! and store as a string
        //         num = std::stoi(hold.c_str());  //conversion from string to int and
        //         //this is also the command index we want to access and run
                
        //         if (num > command_history.size()) //if number is not in range of command history, show that error
        //         {
        //             std::cout << "No such command in history..." << std::endl;
        //             status =0;                      //this variable is not to trigger the most recent process.
        //         }
        //         else{
        //             num--;                              //because the vector list start from 0, correction is made by decreasing
        //             //num variable by 1
                    
        //             args[0] = const_cast<char*>(entered_input.begin()[num].c_str());  //accesed to Nth element in the history
        //         }
        //     }
        //     else  if(input == "!!"){
        //         /*
        //          The case where user enter double exclamation marks
        //          The most recent command is to be run
        //          */
        //         if(command_history.empty())
        //         {
        //             /*
        //              Check if there are no commands
        //              */
        //             std::cout << "No commands in history.." << std::endl;
                    
        //         }
        //         else{
        //             /*
        //              There are commands therefore access the last element of vector list
        //              */
        //             args[0] = const_cast<char*>(entered_input.end()[-1].c_str());
        //         }
        //     }
            
        //     else{
        //         /*
        //          User input to run
        //          */
                
        //         args[0]= const_cast<char*>(entered_input.back().c_str());
        //     }
            
            
        //     if(status == 1 && (should_run == 1)){
                
        //         /*
        //          Status = 1 therefore execute this part of the code.
                 
        //          Start child and parent processes here.
        //          */
                
        //         args[argc] = NULL; //The last element of args is always set to be NULL
                
        //         pid_t pid = fork();  //create child process
                
                
        //         if (pid < 0) {
        //             /*
        //              Pid is negative number flag the error
        //              */
        //             std::cout << "Error" << std::endl;
        //             return 1;
        //         }
                
        //         // Child process
        //         else if (pid == 0) {
        //             // Execute command
        //             execvp(args[0], args);
                    
        //             return 0;
        //         }
                
        //         // Parent process
        //         else {
        //             // Wait for child process to finish
        //             int childStatus;
        //             waitpid(pid, &childStatus, 0);
        //             should_run = 1;
        //         }
        //     }
            
        // }
    // }
    
//     return 0;
// }
