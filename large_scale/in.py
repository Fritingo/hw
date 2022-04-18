import sys
import time
import gc

# parser = argparse.ArgumentParser() 
# parser.add_argument('-i', default='test.in', type=str)

# print(sys.argv[1])

start = time.time()

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

print(sys.getsizeof(net_arr))
del f
del tmp
del nets
net_arr.append(net_arr)
print(sys.getsizeof(net_arr))
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
    
    print(i,sys.getsizeof(cells),sys.getsizeof(cell_connect))

print('done')