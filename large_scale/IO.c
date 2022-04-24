#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc,char *argv[]){
    // read file
    printf("%s\n",argv[1]);
    FILE *f = fopen(argv[1], "r");
    fseek(f, 0, SEEK_END);
    long fsize = ftell(f);
    fseek(f, 0, SEEK_SET);  /* same as rewind(f); */
    printf("%ld\n",fsize);

    char *string = malloc(fsize + 1);
    fread(string, fsize, 1, f);
    fclose(f);

    string[fsize] = 0;
    // net arr -> cell arr
    int *cell = 0;
    int *net = 0;
    int net_len = 0; 
    int len = 0;
    int is_new_net = 1;

    // cell arr -> net arr
    int max_cell_num = 0;

    // string spilt cell and net
    int c_st = 0;
    int c_end = 0;
    int dif = 0;
    int is_cell = 0;

    for(int i=0;i<(int)fsize;i++){
        if(string[i] == ';'){
            is_new_net = 1;
        }else if(string[i] == 'c'){
            c_st = i;
            is_cell = 1;
        }else if(string[i] == ' ' && is_cell == 1){
            is_cell = 0;
            c_end = i;
            dif = c_end-c_st;
            char tmp[dif];
            memcpy(tmp,&string[c_st+1],dif);
            tmp[dif] = '\0';
            // printf("%d\n",atoi(tmp));

            cell = realloc(cell,sizeof(int)*(len+1));
            cell[len] = atoi(tmp);
            // if (atoi(tmp)>max_cell_num){

            // }
            if(is_new_net == 1){
                net = realloc(net,sizeof(int)*(net_len+1));
                net[net_len] = len;
                is_new_net = 0;
                net_len++;
            }
            len++;
            
        }
    }
    for(int i=0;i<len;i++){
        
        printf("cell %d is %d add is %p\n",i,cell[i],&cell[i]);
    }
    for(int i=0;i<net_len;i++){
        // printf("net %d is start cell %d\n",i,net[i]);
        for(int j=0;j<(net[i+1]-net[i]);j++){
            printf("net %d has cell %d\n",i,cell[net[i]+j]);
        }
    }
  
}