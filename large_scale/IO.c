#include <stdio.h>
#include <stdlib.h>


int main(void){
    FILE *f = fopen("case1.in", "r");
    fseek(f, 0, SEEK_END);
    long fsize = ftell(f);
    fseek(f, 0, SEEK_SET);  /* same as rewind(f); */
    printf("%ld\n",fsize);

    char *string = malloc(fsize + 1);
    fread(string, fsize, 1, f);
    fclose(f);

    string[fsize] = 0;
  
}