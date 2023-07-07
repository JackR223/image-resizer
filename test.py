import threading
import multiprocessing

import time
import math

def m1():
    for i in range(0, 10):
        print("m1")
        time.sleep(3)

def m2():
    for i in range(0, 10):
        print("m2")
        time.sleep(2)


t1 = threading.Thread(target=m1)
t2 = threading.Thread(target=m2)


def main_loop(arr):
    for i in range(0, len(arr)):
        print(arr[i])
        time.sleep(3)



#t1.start()
#t2.start()



arr = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

sub_arr1 = []
sub_arr2 = []
sub_arr3 = []
sub_arr4 = []

non_remainder = math.floor(len(arr)/4)*4

for i in range(0, non_remainder, 4):
    #print(i)
    sub_arr1.append(arr[i])
    sub_arr2.append(arr[i+1])
    sub_arr3.append(arr[i+2])
    sub_arr4.append(arr[i+3])

for i in range(non_remainder, len(arr)):
    sub_arr1.append(arr[i])

#print(sub_arr1)
#print(sub_arr2)
#print(sub_arr3)
#print(sub_arr4)

if __name__ == '__main__':

    p1 = multiprocessing.Process(target=main_loop, args=(sub_arr1,))
    p2 = multiprocessing.Process(target=main_loop, args=(sub_arr2,))
    p3 = multiprocessing.Process(target=main_loop, args=(sub_arr3,))
    p4 = multiprocessing.Process(target=main_loop, args=(sub_arr4,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()