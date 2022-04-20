import sys
import gc

from numpy import append

# load file
print("running", end =" ")
f = open(sys.argv[1], "r")
area_ratio = float(f.readline())
# print(area_ratio)
nets = f.read().split(';')
net_arr = []
cells = []
for i in range(len(nets)):

    try:
        tmp = nets[i].replace(' ','').replace('\n','').split('c',1)[1].split('c')
        cells = [*cells,*tmp]
        net_arr.append(tmp)
    except:
        print('. ')
f.close()
cells = list(sorted(map(int,set(cells))))
print(cells)
del f
del tmp
del nets
gc.collect()
print(net_arr)

cell_connect = []
connect_net = []

for cell in cells:
    cell_connect.append([])
    connect_net.append([])
    for net_i,net in enumerate(net_arr):
        if str(cell) in net:
            # print('cell ',cell,' cell_connect len ',len(cell_connect))
            idx = net.index(str(cell))
            # print('index',idx)
            if idx == 0 and len(net)>1:
                cell_connect[cell-1].append(net[idx+1])
                connect_net[cell-1].append(net_i+1)
            elif idx == len(net)-1:
                cell_connect[cell-1].append(net[idx-1])
                connect_net[cell-1].append(net_i+1)
            else:
                cell_connect[cell-1].append(net[idx+1])
                connect_net[cell-1].append(net_i+1)
                cell_connect[cell-1].append(net[idx-1])
                connect_net[cell-1].append(net_i+1)
    # cell_connect[cell-1] = list(set(cell_connect[cell-1]))
    print('cell ',cell,' connecting')
print(net_arr)
print(cell_connect)
print(connect_net)
# =============gain================


A = cells[:int(len(cells)*0.5)]
B = cells[int(len(cells)*0.5):]
# A = [1,3,4,7]
# B = [2,5,6,8]
# print(len(A)+len(B))
print('=================')
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


# #========== cut size =============
cut_size = 0
def cutsize():
    # print('cutsize')
    # print(A)
    global cut_size
    cut_size = 0
    cut_net = []
    for cell in A:
        # print('cell',cell)
        for pin_i,pin in enumerate(cell_connect[cell-1]):
            
            # print('pin ',pin)
            if int(pin) in B:
                # print('inB',connect_net[cell-1][pin_i])
                cut_net.append(connect_net[cell-1][pin_i])
                # cut_size += 1
                # print(pin,cut_size)
            # print(cut_net)
    cut_size = len(set(cut_net))
    # print(cut_size)

cutsize()

min_cut_size = cut_size
min_A = A
min_B = B
print(cut_size)


# #===============alg=====================
AorB = 0
change_cell = 'none'
swap_time = 0

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

        
        # print('A: ',A)
        # print(A_gain)
        # print('B: ',B)
        # print(B_gain)

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

print("Cutsize = ",min_cut_size)
min_A = sorted(list(map(int,min_A)))
min_B = sorted(list(map(int,min_B)))
print("G1 ",len(min_A))
print(min_A)
print("G2 ",len(min_B))
print(min_B)

# #=================out file=========================
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

print("done")




#     #=================unit test============================
#     # print(A_gain[list(A_gain)[0]])
# if A_gain[list(A_gain)[0]] > B_gain[list(B_gain)[0]]:
#     AorB = 0
#     change_cell = list(A_gain)[0]
#     B.append(change_cell)
#     A.remove(change_cell)
    
# else:
#     AorB = 1
#     change_cell = list(B_gain)[0]
#     A.append(change_cell)
#     B.remove(change_cell)

# # # print(A)
# # # print(B)

# # # # print(cell_connect[list(A_gain)[0]])

# # # # print(A_gain)
# for pin in cell_connect[change_cell-1]:
#     # print(cell)
#     if AorB == 0:
#         if int(pin) in A:
#             A_gain[int(pin)] = A_gain[int(pin)]+2
#         else:
#             B_gain[int(pin)] = B_gain[int(pin)]-2
#     else:
#         if int(pin) in A:
#             A_gain[int(pin)] = A_gain[int(pin)]-2
#         else:
#             B_gain[int(pin)] = B_gain[int(pin)]+2
    
# if AorB == 0:
#     del A_gain[change_cell]
# else:
#     del B_gain[change_cell]

# A_gain = dict(sorted(A_gain.items(),key=lambda x:x[1],reverse=True))
# B_gain = dict(sorted(B_gain.items(),key=lambda x:x[1],reverse=True))

# print(A_gain)
# print(B_gain)
# cutsize()
# print(cut_size)
# if AorB == 0:
#     AorB = 1
#     change_cell = list(B_gain)[0]
#     A.append(change_cell)
#     B.remove(change_cell)
    
# else:
#     AorB = 0
#     change_cell = list(A_gain)[0]
#     B.append(change_cell)
#     A.remove(change_cell)

# # # print(A)
# # # print(B)

# for pin in cell_connect[change_cell-1]:
#     # print(cell)
#     if AorB == 0:
#         if int(pin) in A:
#             A_gain[int(pin)] = A_gain[int(pin)]+2
#         else:
#             B_gain[int(pin)] = B_gain[int(pin)]-2
#     else:
#         if int(pin) in A:
#             A_gain[int(pin)] = A_gain[int(pin)]-2
#         else:
#             B_gain[int(pin)] = B_gain[int(pin)]+2
    
# if AorB == 0:
#     del A_gain[change_cell]
# else:
#     del B_gain[change_cell]

# A_gain = dict(sorted(A_gain.items(),key=lambda x:x[1],reverse=True))
# B_gain = dict(sorted(B_gain.items(),key=lambda x:x[1],reverse=True))

# print(A_gain)
# print(B_gain)
# cutsize()
# print('A: ',A)
# print('B: ',B)
# print(cut_size)

# # cutsize()
# # if cut_size < min_cut_size:
# #     min_cut_size = cut_size
# #     min_A = A
# #     min_B = B
# # print(min_cut_size,min_A,min_B)