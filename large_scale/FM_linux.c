#include <stdio.h>
#include <stdlib.h>
#include <string.h>


typedef struct node{
    int cell;
    struct node *next;
}node;

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

int cut_size(node **net,int *G,int net_len,int G_len){
    int cutsize = 0;

    for(int i=0;i<net_len;i++){
        node *now = net[i];
        int G1_num = 0, net_cell_num = 0;
        
        do{
            net_cell_num++;
            for(int j=0;j<G_len;j++){
                // printf("G1 %d in net cell %d\n",G[j],now->cell);
                if(G[j] == now->cell){
                    G1_num++;
                    break;
                }
            }
            now = now->next;

        }while(now->cell != 0);
        // printf("G1 num %d net_cell_num %d\n",G1_num,net_cell_num);
        if(G1_num != 0 && net_cell_num-G1_num !=0){
            cutsize++;
        }
        
    }
    return cutsize;

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
            

            // if(current_cell>max_cell_num){
            //     int pre_cell_num = max_cell_num;
            //     max_cell_num = current_cell;
            //     cell = (node **)realloc(cell,sizeof(node*)*(max_cell_num));
            //     for(int cell_num=pre_cell_num;cell_num<max_cell_num;cell_num++){
            //         // printf("cell num %d\n",cell_num);
            //         push_node(&cell[cell_num],0);
            //     }
            // }
            // if(is_net == 1 || first_cell == 1){
            //     pre_cell = current_cell;
            //     first_cell = 0;
            // }else{
            //     push_node(&cell[current_cell-1],pre_cell);
            //     push_node(&cell[pre_cell-1],current_cell);
            //     pre_cell = current_cell;
            // }

            // for(int i=0;i<max_cell_num;i++){
            //     node *curr = cell[i];
            //     printf("cell %d: ",i+1);
            //     printf(" %d",curr->cell);
            //     // curr = curr->next;
            //     // printf(" %d",curr->cell);
            //     // do{
            //     //     printf(" %d",curr->cell);
            //     //     curr = curr->next;
            //     // }while(curr->cell != 0);
            //     printf("\n");
            // }
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

            // --------- cell ----------
            if(current_cell>max_cell_num){
                int pre_cell_num = max_cell_num;
                max_cell_num = current_cell;
                cell = (node **)realloc(cell,sizeof(node*)*(max_cell_num));
                for(int cell_num=pre_cell_num;cell_num<max_cell_num;cell_num++){
                    // printf("cell num %d\n",cell_num);
                    push_node(&cell[cell_num],0);
                }
            }
            
            push_node(&cell[current_cell-1],net_len);
            // --------- cell ----------
        }
    }


    // // partition
    int mid = max_cell_num / 2;
    int G1_len = mid,G2_len = mid;
    int *G1 = 0;
    
    // if cell num can't divide 2
    if(max_cell_num % 2 != 0){
        G1 = (int *)malloc(sizeof(int)*(mid+1));
        G1[mid] = mid + 1; 
        G1_len++;
    }else{
        G1 = (int *)malloc(sizeof(int)*mid);
    }
    int *G2 = 0;
    G2 = (int *)malloc(sizeof(int)*mid);
    // G1: 1 2 3 4 ...
    // G2: 8 7 6 5 ...
    for(int i=0;i<mid;i++){
        G1[i] = i+1;
        G2[i] = max_cell_num-i;
    }



    // // --------- cut size ----------
    printf("cut size %d\n",cut_size(&net[0],&G1[0],net_len,G1_len));
    int cutsize = cut_size(&net[0],&G1[0],net_len,G1_len);
    // // --------- cut size ----------

    // ----------- gain -------------
    // gain **Gain = 0;
    // Gain = (gain **)malloc(sizeof(gain*)*max_cell_num);
    int Gain[max_cell_num][2];

    
    for(int i=0;i<max_cell_num;i++){
        int gain_num = 0;
        node *cell_ptr = cell[i];
        
        do{
            int G1_num = 0, net_cell_num = 0;
            // printf("test net %d\n",cell_ptr->cell);
            node *net_ptr = net[(cell_ptr->cell)-1];
            do{
                // printf(" %d",net_ptr->cell);
                net_cell_num++;
                for(int j=0;j<G1_len;j++){
                    if(G1[j] == net_ptr->cell){
                        G1_num++;
                        break;
                    }
                }
                net_ptr = net_ptr->next;
            }while(net_ptr->cell != 0);
            // printf("\n g1 num %d net_cell_num %d\n",G1_num,net_cell_num);
            if(G1_num != 0 && net_cell_num-G1_num !=0){
                gain_num++;
            }else{
                gain_num--;
            }
            // printf("gain %d\n",gain_num);
            cell_ptr = cell_ptr->next;
        }while(cell_ptr->cell != 0);
        
        Gain[i][0] = i+1;
        Gain[i][1] = gain_num;
    }
    for(int i=0;i<max_cell_num;i++){
        
        printf("cell %d gain %d\n",Gain[i][0],Gain[i][1]);
    }
    // ----------- sort -------------
    
    quicksort(Gain,0,max_cell_num-1);

    // ----------- gain -------------

    // ----------- swap -------------
    int G1_change = 0;
    int G2_change = 0;
    if(Gain[max_cell_num-1][0] <= mid+1){
        G1_change = Gain[max_cell_num-1][0];
        int fi = 1;
        while(Gain[max_cell_num-(++fi)][0] <= mid+1);
        G2_change = Gain[max_cell_num-fi][0];
    }else{
        G2_change = Gain[max_cell_num-1][0];
        int fi = 1;
        while(Gain[max_cell_num-(++fi)][0] > mid+1);
        G1_change = Gain[max_cell_num-fi][0];
    }
    


    // // --------- write file ----------
    write_file(argv[2],cutsize,&G1[0],G1_len,&G2[0],G2_len);
    // // print all net
    for(int i=0;i<net_len;i++){
        node *now = net[i];
        printf("net %d: ",i+1);
        
        do{
            printf(" %d",now->cell);
            now = now->next;
        }while(now->cell != 0);
        printf("\n");
        // printf("test\n");
    }
    // // print all cell

    for(int i=0;i<max_cell_num;i++){
        node *curr = cell[i];
        printf("cell %d: ",i+1);
        // printf(" %d",curr->cell);
        // curr = curr->next;
        // printf(" %d",curr->cell);
        do{
            printf(" %d",curr->cell);
            curr = curr->next;
        }while(curr->cell != 0);
        printf("\n");
    }

    // print all gain
    for(int i=0;i<max_cell_num;i++){
        
        printf("cell %d gain %d\n",Gain[i][0],Gain[i][1]);
    }
    // print max gain
    printf("G1 max gain %d G2 max gain %d\n",G1_change,G2_change);
}