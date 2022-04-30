#include <stdio.h>
#include <stdlib.h>
#include <string.h>


typedef struct node{
    int cell;
    struct node *next;
}node;



void push_node(node **head,int cell){
    node *new_node = malloc(sizeof(node));
    if(cell == 0){
        new_node->cell = 0;
        new_node->next = NULL;
        *head = new_node;
    }else if (new_node != NULL){
        new_node->cell = cell;
        new_node->next = *head;
        *head = new_node;
    }
}

int cut_size(node **net,int *cell_G,int net_len){
    int cutsize = 0;

    for(int i=0;i<net_len;i++){
        node *now = net[i];
        int G1_num = 0, net_cell_num = 0,G2_num = 0;
        
        do{
            net_cell_num++;

            if(cell_G[(now->cell)-1] == 0){
                G1_num++;
            }else{
                G2_num++;
            }
      
            now = now->next;

        }while(now->cell != 0);
   
        if(G1_num != 0 && G2_num != 0 ) cutsize++;
        
    }
    return cutsize;

}

// row is not mandatory 
void quicksort(int arr[][2],int left,int right){
    if(left < right){
        int s = arr[(left+right)/2][1];
        int i = left - 1;
        int j = right + 1;

        while(1){
            while(arr[++i][1] < s);
            while(arr[--j][1] > s);
            if(i >= j) break;
            // swap
            int temp0 = arr[i][0];
            int temp1 = arr[i][1];
            arr[i][0] = arr[j][0];
            arr[i][1] = arr[j][1];
            arr[j][0] = temp0;
            arr[j][1] = temp1;
        }
        quicksort(arr,left,i-1);
        quicksort(arr,j+1,right);
    }
}

void write_file(char *file,int cutsize,int *G1,int G1_len,int *G2,int G2_len){
    printf("%s\n",file);
    FILE *of = fopen(file,"w");

    fprintf(of,"Cutsize = %d\n",cutsize);
    fprintf(of,"G1 %d\n",G1_len);

    for(int i=0;i<G1_len;i++){
        fprintf(of,"c%d ",G1[i]);
    }
    fprintf(of,";\n");

    fprintf(of,"G2 %d\n",G2_len);

    for(int i=0;i<G2_len;i++){
        fprintf(of,"c%d ",G2[i]);
    }
    fprintf(of,";\n");

    fclose(of);
}


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

    // net with cell
    node **net = 0;
    net = (node **)malloc(sizeof(node*)*1);
    push_node(&net[0],0);
    int net_len = 1; // current net len
    int current_net = 0; // current net idx

    // // cell with net
    node **cell = 0;
    cell = (node **)malloc(sizeof(node*)*1);
    push_node(&cell[0],0);
    int pre_cell = 0;
    node **cell_pins = 0;
    cell_pins = (node **)malloc(sizeof(node*)*1);
    push_node(&cell_pins[0],0);
    

    // // spilt char and net
    int c_st = 0; // one cell start idx
    int c_end = 0; // one cell end idx
    int dif = 0; // one cell's len 
    int is_cell = 0; // is new cell
    int is_net = 0; // is new net

    int max_cell_num = 0;
    int first_cell = 1;

    for(int i=0;i<fsize;i++){
        if(string[i] == ';'){
            is_net = 1;
        }else if(string[i] == 'c'){
            c_st = i;
            is_cell = 1;
        }else if(string[i] == ' ' && is_cell == 1){
            // one cell end is ' '
            // -------- new cell ---------
            is_cell = 0;
            c_end = i;
            dif = c_end - c_st;

            char tmp[dif]; // create a string space
            memcpy(tmp,&string[c_st+1],dif);
            tmp[dif] = '\0'; // end notation
            int current_cell = atoi(tmp);
            // -------- new cell --------- 

            // --------- cell connect ----------
            

            if(current_cell>max_cell_num){
                int pre_cell_num = max_cell_num;
                max_cell_num = current_cell;
                cell = (node **)realloc(cell,sizeof(node*)*(max_cell_num));
                cell_pins = (node **)realloc(cell_pins,sizeof(node*)*(max_cell_num));
                for(int cell_num=pre_cell_num;cell_num<max_cell_num;cell_num++){
                    // printf("cell num %d\n",cell_num);
                    push_node(&cell[cell_num],0);
                    push_node(&cell_pins[cell_num],0);
                }
            }
            if(is_net == 1 || first_cell == 1){
                pre_cell = current_cell;
                first_cell = 0;
            }else{
                push_node(&cell[current_cell-1],pre_cell);
                cell_pins[current_cell-1]->cell += 1;
                push_node(&cell[pre_cell-1],current_cell);
                cell_pins[pre_cell-1]->cell += 1;
                pre_cell = current_cell;
            }

            // --------- cell connect ----------

            // ---------- nets ----------
            if(is_net == 1){
                is_net = 0;
                // creat new net
                net = (node **)realloc(net,sizeof(node*)*(net_len+1));
                net_len++;
                current_net++;
                push_node(&net[current_net],0);
            }

            // // set new node (cell)
            push_node(&net[current_net],current_cell);
            
            
        }
    }


    // // partition
    int cell_G[max_cell_num];

    int mid = max_cell_num / 2;
    int G1_len = mid,G2_len = mid;
    int *G1 = 0;
    int unlock[max_cell_num];
    memset(unlock, 0, max_cell_num*sizeof(int));
    
    
    // if cell num can't divide 2
    if(max_cell_num % 2 != 0){
        G1 = (int *)malloc(sizeof(int)*(mid+1));
        
        G1[mid] = mid + 1; 
        
        G1_len++;

    }else{
        G1 = (int *)malloc(sizeof(int)*mid);

    }
    for(int i=0;i<G1_len;i++) cell_G[i] = 0;// G1 0
    int *G2 = 0;
    

    G2 = (int *)malloc(sizeof(int)*mid);
    

    for(int i=0;i<G2_len;i++) cell_G[G1_len + i] = 1; // G2 1
    // G1: 1 2 3 4 ...
    // G2: 8 7 6 5 ...
    for(int i=0;i<mid;i++){
        G1[i] = i + 1;
        
        G2[i] = max_cell_num - i;
    }

    //---------- gain --------
    int gain[max_cell_num];
    memset(gain, 0, max_cell_num*sizeof(int));
    for(int i=0;i<max_cell_num;i++){
        node *pin_node = cell[i];
        while(pin_node->cell != 0){
            if(cell_G[pin_node->cell-1] == cell_G[i] ) gain[i]--;
            if(cell_G[pin_node->cell-1] != cell_G[i] ) gain[i]++;
            pin_node = pin_node->next;
        }

    }

    // for(int i=0;i<max_cell_num;i++) printf("%d ",gain[i]);

    int G1_max_gain_cell = 0,G1_max_gain = -1,G2_max_gain_cell = 0,G2_max_gain = -1; 
    //  // ------------ find max gain -----------
    for(int i=0;i<max_cell_num;i++){
        if(gain[i] >= G1_max_gain && cell_G[i] == 0){
            G1_max_gain_cell = i+1;
            G1_max_gain = gain[i];
            unlock[i] = 1;
        }
        if(gain[i] >= G2_max_gain && cell_G[i] == 1){
            G2_max_gain_cell = i+1;
            G2_max_gain = gain[i];
            unlock[i] = 1;
        }

    } 
    
    
    // printf("ttt %d\n",cell_G[G2_max_gain_cell-1]);

    // for(int i=0;i<G1_len;i++) printf("G1 %d ",G1[i]);
    // for(int i=0;i<G2_len;i++) printf("G2 %d ",G2[i]);

    // for(int i=0;i<max_cell_num;i++){
    //     node *pin = cell[i];
    //     printf("cell %d : ",i+1);
    //     while (pin->cell != 0){
    //         printf(" %d ",pin->cell);
    //         pin = pin->next;
    //     }
    //     printf("\n");
    // }
    
    // for(int i=0;i<100;i++){
        G1[G1_max_gain_cell-1] = G2_max_gain_cell;
        G2[max_cell_num-G2_max_gain_cell] = G1_max_gain_cell;
        
        cell_G[G1_max_gain_cell-1] ^= 1;
    //     // printf("ttt %d\n",cell_G[G2_max_gain_cell-1]);
        cell_G[G2_max_gain_cell-1] ^= 1;

        // for(int i=0;i<max_cell_num;i++) printf("G %d \n",gain[i]);
    //     // ---------- update gain ------------
        node *pin_node = cell[G1_max_gain_cell-1];
        while(pin_node->cell != 0){
            if(cell_G[pin_node->cell-1] == 0) gain[pin_node->cell-1] += 2;
            if(cell_G[pin_node->cell-1] == 1) gain[pin_node->cell-1] -= 2;
            pin_node = pin_node->next;
        }

        node *pin_node2 = cell[G2_max_gain_cell-1];
        while(pin_node2->cell != 0){
            if(cell_G[pin_node2->cell-1] == 1) gain[pin_node2->cell-1] += 2;
            if(cell_G[pin_node2->cell-1] == 0) gain[pin_node2->cell-1] -= 2;
            pin_node2 = pin_node2->next;
        }

        G1_max_gain_cell = 0,G1_max_gain = -1,G2_max_gain_cell = 0,G2_max_gain = -1; 
        //  // ------------ find max gain -----------
        for(int i=0;i<max_cell_num;i++){
            if(gain[i] >= G1_max_gain && cell_G[i] == 0 && unlock[i] == 0){
                G1_max_gain_cell = i+1;
                G1_max_gain = gain[i];
                unlock[i] = 1;
            }
            if(gain[i] >= G2_max_gain && cell_G[i] == 1 && unlock[i] == 0){
                G2_max_gain_cell = i+1;
                G2_max_gain = gain[i];
                unlock[i] = 1;
            }

        } 
        // for(int i=0;i<max_cell_num;i++) printf("Gt %d \n",gain[i]);

        for(int i=0;i<max_cell_num;i++){
            if(gain[i] >= G1_max_gain && cell_G[i] == 0){
                G1_max_gain_cell = i+1;
                G1_max_gain = gain[i];
            }
            if(gain[i] >= G2_max_gain && cell_G[i] == 1){
                G2_max_gain_cell = i+1;
                G2_max_gain = gain[i];
            }

        } 
        
    // }
    
    
   
    // // --------- cut size ----------
    int cutsize = cut_size(&net[0],&cell_G[0],net_len);
    // // --------- cut size ----------


    
    // // --------- write file ----------
    write_file(argv[2],cutsize,&G1[0],G1_len,&G2[0],G2_len);

}