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
create a dictionary key is cell and value is this key connect cells include key

```python=
cell_connect = {}
cells = []
for i,net in enumerate(net_arr):
    for cell in net:
        if cell not in cell_connect:
            cell_connect[cell] = []
            cells.append(cell)
            for net2 in net_arr[i:]:
                if cell in net2:
                    for item in net2:
                        cell_connect[cell].append(item)
            cell_connect[cell] = set(cell_connect[cell])
```

like
`{'1': {'5', '1', '3'}, '3': {'6', '1', '5', '4', '3', '2'}, '5': {'6', '1', '7', '5', '3'}, '2': {'4', '3', '2'}, '4': {'4', '3', '2', '6'}, '6': {'6', '7', '5', '4', '3', '8'}, '7': {'8', '6', '5', '7'}, '8': {'8', '6', '7'}}`
so
`cell_connect[cell]`
`cell_connect['1'] = {'5', '1', '3'}`
#### separate A B side by area ratio
```python=
A = cells[:int(len(cell_connect)*area_ratio)]
B = cells[int(len(cell_connect)*area_ratio):]
```
#### calculate gain
calculate A B gain
```python=
A_gain = {}
B_gain = {}
for cell in A:
    gain = 1
    for pin in cell_connect[cell]:
        if pin in B:
            gain += 1
        else:
            gain -= 1

    A_gain[cell] = gain


A_gain = dict(sorted(A_gain.items(),key=lambda x:x[1],reverse=True))

for cell in B:
    gain = 1
    for pin in cell_connect[cell]:
        if pin in A:
            gain += 1
        else:
            gain -= 1

    B_gain[cell] = gain

B_gain = dict(sorted(B_gain.items(),key=lambda x:x[1],reverse=True))
```

#### calculate cut size
```python=
cut_size = 0
def cutsize():
    global cut_size
    cut_size = 0
    for cell in A:
        for pin in cell_connect[cell]:
            if pin in B:
                cut_size += 1
```

#### iteration
each while iteration 
frist time select gain bigger side cell
and next time select the other side gain bigger cell
still any side all cells are change

```python=
while(len(A_gain) and len(B_gain)):

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

        for cell in cell_connect[change_cell]:
            if cell != change_cell:
                if cell in A_gain:
                    if AorB == 0:
                        A_gain[cell] = A_gain[cell]+2
                    else:
                        A_gain[cell] = A_gain[cell]-2
                elif cell in B_gain:
                    if AorB == 0:
                        B_gain[cell] = B_gain[cell]-2
                    else:
                        B_gain[cell] = B_gain[cell]+2
            else:
                if AorB == 0:
                    del A_gain[cell]
                else:
                    del B_gain[cell]

        A_gain = dict(sorted(A_gain.items(),key=lambda x:x[1],reverse=True))
        B_gain = dict(sorted(B_gain.items(),key=lambda x:x[1],reverse=True))

    cutsize()
    if cut_size < min_cut_size:
        min_cut_size = cut_size
        min_A = A
        min_B = B

    gc.collect()
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