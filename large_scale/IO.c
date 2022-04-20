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

    int *cell = 0;
    int *net = 0;
    int net_len = 0; 
    int len = 0;

    int c_st = 0;
    int c_end = 0;
    int dif = 0;
    int is_cell = 0;
    for(int i=0;i<(int)fsize;i++){
        if(string[i] == 'c'){
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
            len++;
        }
    }
    for(int i=0;i<len;i++){
        
        printf("cell %d is %d add is %p\n",i,cell[i],&cell[i]);
    }
  
}