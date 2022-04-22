## run
`python3 FM.py [input_file] [out_file]`

### sample
`python3 FM.py test.in test.out`

## explain code

#### read file

```python=
f = open(sys.argv[1], "r")
area_ratio = float(f.readline())
# print(area_ratio)
nets = f.read().split(';')
net_arr = []
for i in range(len(nets)):
   
    try:
        tmp = nets[i].replace(' ','').replace('\n','').split('c',1)[1].split('c')
        
        net_arr.append(tmp)
    except:
        print('. ')
f.close()
```
spilt with net
like
`[
['9998', '11538','4630'],
['4630', '14231'], 
['13254', '11807'], 
['12394', '12382', '12376', '12374', '11946'], 
['12348', '11911'], 
['12324', '9808', '12281', '11698', '12252', '8481', '9779', '4801', '11595', '12184']
]`
so
`net_arr[0]` is NET1 all cells


#### connect cells
create a list the cell-1 "index" value is this cell connect other cells(pin)

```python=
cell_connect = []

for cell in cells:
    cell_connect.append([])
    for net in net_arr:
        if str(cell) in net:
            # print('cell ',cell,' cell_connect len ',len(cell_connect))
            idx = net.index(str(cell))
            # print('index',idx)
            if idx == 0 and len(net)>1:
                cell_connect[cell-1].append(net[idx+1])
            elif idx == len(net)-1:
                cell_connect[cell-1].append(net[idx-1])
            else:
                cell_connect[cell-1].append(net[idx+1])
                cell_connect[cell-1].append(net[idx-1])
    cell_connect[cell-1] = list(set(cell_connect[cell-1]))
    print('cell ',cell,' connecting')
print(cell_connect)
```


#### calculate gain
calculate A B gain
```python=
A_gain = {}
B_gain = {}

for cell in A:
    gain = 0
    
    for pin in cell_connect[cell-1]:
        
        if int(pin) in B:
            gain += 1
        else:
            gain -= 1
    
    A_gain[cell] = gain
    print('A_gain len',len(A_gain))

A_gain = dict(sorted(A_gain.items(),key=lambda x:x[1],reverse=True))
print(A_gain)

for cell in B:
    gain = 0
    
    for pin in cell_connect[cell-1]:
        
        if int(pin) in A:
            gain += 1
        else:
            gain -= 1
    
    B_gain[cell] = gain
    print('B_gain len',len(B_gain))

B_gain = dict(sorted(B_gain.items(),key=lambda x:x[1],reverse=True))
print(B_gain)
```

#### calculate cut size
```python=
cut_size = 0
def cutsize():
    # print('cutsize')
    # print(A)
    global cut_size
    cut_size = 0
    for cell in A:
        # print('cell',cell)
        for pin in cell_connect[cell-1]:
            # print('pin ',pin)
            if int(pin) in B:
                cut_size += 1
                # print(pin,cut_size)
    # print(cut_size)

cutsize()
```

#### iteration
each while loop iteration 
first time select gain bigger side (AorB) cell
and next time select the other side gain bigger cell
still any side all cells are change(or achieve swap time)

```python=
while((len(A_gain) and len(B_gain)) and swap_time<100):

    # for next reverse so set reverse AorB
    if A_gain[list(A_gain)[0]] > B_gain[list(B_gain)[0]]:
        AorB = 1  
    else:
        AorB = 0

    for i in range(2):
        # reverse last time chage side
        if AorB == 0:
            AorB = 1 
            change_cell = list(B_gain)[0]
            A.append(change_cell)
            B.remove(change_cell)

        else:
            AorB = 0
            change_cell = list(A_gain)[0]
            B.append(change_cell)
            A.remove(change_cell)
       
        # print(A)
        # print(B)

        for pin in cell_connect[change_cell-1]:
            
            if AorB == 0:
                if int(pin) in A and int(pin) in A_gain:
                    A_gain[int(pin)] = A_gain[int(pin)]+2
                elif int(pin) in B_gain:
                    B_gain[int(pin)] = B_gain[int(pin)]-2
            else:
                if int(pin) in A and int(pin) in A_gain:
                    A_gain[int(pin)] = A_gain[int(pin)]-2
                elif int(pin) in B_gain:
                    B_gain[int(pin)] = B_gain[int(pin)]+2
            
        if AorB == 0:
            del A_gain[change_cell]
        else:
            del B_gain[change_cell]


        A_gain = dict(sorted(A_gain.items(),key=lambda x:x[1],reverse=True))
        B_gain = dict(sorted(B_gain.items(),key=lambda x:x[1],reverse=True))


    cutsize()
    # print(cut_size)
    if cut_size < min_cut_size:
        min_cut_size = cut_size
        min_A = A
        min_B = B
    # print(min_cut_size,min_A,min_B)
    gc.collect()
    swap_time += 1
    print('swap_time: ',swap_time,'max A_gain: ',A_gain[list(A_gain)[0]],',max B_gain: ',B_gain[list(B_gain)[0]])
    if A_gain[list(A_gain)[0]] + B_gain[list(B_gain)[0]] < 1:
            break
```
#### write file
```python=
min_A = sorted(list(map(int,min_A)))
min_B = sorted(list(map(int,min_B)))

of = open(sys.argv[2], "w")

of.write("Cutsize = "+str(min_cut_size)+"\n")

of.write("G1 "+str(len(min_A))+"\n")

for item in min_A:
    of.write("c"+str(item)+" ")
of.write(";\n")

of.write("G2 "+str(len(min_B))+"\n")

for item in min_B:
    of.write("c"+str(item)+" ")
of.write(";\n")

of.write("\n")

of.close()
```
