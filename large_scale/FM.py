import sys

import gc


# parser = argparse.ArgumentParser() 
# parser.add_argument('-i', default='test.in', type=str)

# print(sys.argv[1])



# load file
print("running", end =" ")
f = open(sys.argv[1], "r")
area_ratio = float(f.readline())
# print(area_ratio)
nets = f.read().split(';')
net_arr = []
for i in range(len(nets)):
    # print(nets[i])
    # print('ans',nets[i].split('c',1))
    try:
        tmp = nets[i].replace(' ','').replace('\n','').split('c',1)[1].split('c')
        
        net_arr.append(tmp)
    except:
        print('. ')
f.close()
del f
del tmp
del nets
gc.collect()

# print(net_arr)
# net_arr = [['9998', '11538','4630'], ['4630', '14231'], ['13254', '11807'], ['12394', '12382', '12376', '12374', '11946', '12348', '11911', '12324', '9808', '12281', '11698', '12252', '8481', '9779', '4801', '11595', '12184']]
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
    # print(i,sys.getsizeof(cell_connect))
del net_arr
gc.collect()

# print(cell_connect['1'])
print(cell_connect)
# print(time.time()-start)

# ==================partition=======================
# print(cells)
# print(len(cell_connect))
# print(len(cells))

A = cells[:int(len(cell_connect)*0.5)]
B = cells[int(len(cell_connect)*0.5):]
# print(len(A)+len(B))

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

# print(A_gain)

A_gain = dict(sorted(A_gain.items(),key=lambda x:x[1],reverse=True))
# print(A_gain)

for cell in B:
    gain = 1
    for pin in cell_connect[cell]:
        if pin in A:
            gain += 1
        else:
            gain -= 1

    B_gain[cell] = gain

B_gain = dict(sorted(B_gain.items(),key=lambda x:x[1],reverse=True))
# print(B_gain)



#========== cut size =============
cut_size = 0
def cutsize():
    print('cutsize')
    print(A)
    global cut_size
    cut_size = 0
    for cell in A:
        print('cell',cell)
        for pin in cell_connect[cell]:
            print('pin ',pin)
            if pin in B:
                cut_size += 1
                print(pin,cut_size)
    # print(cut_size)

cutsize()

min_cut_size = cut_size
min_A = A
min_B = B
# print(cut_size)


# print('==========================')

#===============opz=====================
AorB = 0
change_cell = 'none'


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
       
        # print(A)
        # print(B)

        for cell in cell_connect[change_cell]:
            # print(cell)
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

        # print(A_gain)
        # print(B_gain)

    cutsize()
    # print(cut_size)
    if cut_size < min_cut_size:
        min_cut_size = cut_size
        min_A = A
        min_B = B
    # print(min_cut_size,min_A,min_B)
    gc.collect()

print("Cutsize = ",min_cut_size)
min_A = sorted(list(map(int,min_A)))
min_B = sorted(list(map(int,min_B)))
print("G1 ",len(min_A))
print(min_A)
print("G2 ",len(min_B))
print(min_B)

#=================out file=========================
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




    #=================unit test============================
    # print(A_gain[list(A_gain)[0]])
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

# print(A)
# print(B)

# # print(cell_connect[list(A_gain)[0]])

# # print(A_gain)
# for cell in cell_connect[change_cell]:
#     # print(cell)
#     if cell != change_cell:
#         if cell in A:
#             if AorB == 0:
#                 A_gain[cell] = A_gain[cell]+2
#             else:
#                 A_gain[cell] = A_gain[cell]-2
#         else:
#             if AorB == 0:
#                 B_gain[cell] = B_gain[cell]-2
#             else:
#                 B_gain[cell] = B_gain[cell]+2
#     else:
#         if AorB == 0:
#             del A_gain[cell]
#         else:
#             del B_gain[cell]

# A_gain = dict(sorted(A_gain.items(),key=lambda x:x[1],reverse=True))
# B_gain = dict(sorted(B_gain.items(),key=lambda x:x[1],reverse=True))

# print(A_gain)
# print(B_gain)

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

# print(A)
# print(B)

# for cell in cell_connect[change_cell]:
#     # print(cell)
#     if cell != change_cell:
#         if cell in A_gain:
#             if AorB == 0:
#                 A_gain[cell] = A_gain[cell]+2
#             else:
#                 A_gain[cell] = A_gain[cell]-2
#         elif cell in B_gain:
#             if AorB == 0:
#                 B_gain[cell] = B_gain[cell]-2
#             else:
#                 B_gain[cell] = B_gain[cell]+2
#     else:
#         if AorB == 0:
#             del A_gain[cell]
#         else:
#             del B_gain[cell]

# A_gain = dict(sorted(A_gain.items(),key=lambda x:x[1],reverse=True))
# B_gain = dict(sorted(B_gain.items(),key=lambda x:x[1],reverse=True))

# print(A_gain)
# print(B_gain)

# cutsize()
# if cut_size < min_cut_size:
#     min_cut_size = cut_size
#     min_A = A
#     min_B = B
# print(min_cut_size,min_A,min_B)