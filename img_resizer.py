# import required module
import os
import PIL
import PIL.ImageOps as ImageOps
import cv2
import numpy
import math

import threading

from io import BytesIO


def compress(arr, source_dir, target_dir, target_size, pipe):

    # COULD USE TWO SEPARATE MODES, ONE TO TRIM TO FIXED DIMENSIONS + ONE TO TRIM TO FIXED FILE SIZE

    sub_arr1, sub_arr2, sub_arr3, sub_arr4 = [], [], [], []

    non_remainder = math.floor(len(arr)/2)*2

    for i in range(0, non_remainder, 2):
        sub_arr1.append(arr[i])
        sub_arr2.append(arr[i+1])
        #sub_arr3.append(arr[i+2])
        #sub_arr4.append(arr[i+3])
    for i in range(non_remainder, len(arr)):
        sub_arr1.append(arr[i])

    #print(arr)
    #print("")
    #print(sub_arr1)

    def compress_2(arr, source_dir, target_dir, target_size):

        # iterate over files in source_dir
        for filename in arr:

            print("resizing: " + filename)

            image_in = PIL.Image.open(source_dir + "/" + filename)
            h,w = image_in.size

            res = max(h, w) / 2  

            while True:

                res = int(res)

                image_out = ImageOps.contain(image_in, (res, res))

                f = target_dir + "/" + filename

                fake_file = BytesIO()

                image_out.save(fake_file, 'jpeg')

                size = (fake_file.getbuffer().nbytes)/1000

                if size >= target_size*0.9 and size <= target_size:
                    # resolution is close enough to target
                    print(f)
                    with open(f, "wb") as outfile:
                        # Copy the BytesIO stream to the output file
                        outfile.write(fake_file.getbuffer())
                    break
                elif size < target_size:
                    # increase resolution:
                    res = res + (res/2)
                elif size > target_size:
                    # decrease resolution:
                    res = res/2

    t1 = threading.Thread(target=compress_2, args=(sub_arr1, source_dir, target_dir, target_size))
    t2 = threading.Thread(target=compress_2, args=(sub_arr2, source_dir, target_dir, target_size))
    #t3 = threading.Thread(target=compress_2, args=(sub_arr3, source_dir, target_dir, target_size))
    #t4 = threading.Thread(target=compress_2, args=(sub_arr4, source_dir, target_dir, target_size))

    t1.start()
    t2.start()
    #t3.start()
    #t4.start()

    t1.join()
    t2.join()
    #t3.join()
    #t4.join()
    
    pipe.send("Finished!")


# generates and returns 4 arrays of files from source directory
def split(source_dir):

    sub_arr1 = []
    sub_arr2 = []
    sub_arr3 = []
    sub_arr4 = []

    files = os.listdir(source_dir)
    non_remainder = math.floor(len(files)/4)*4
    
    for i in range(0, non_remainder, 4):
        sub_arr1.append(files[i])
        sub_arr2.append(files[i+1])
        sub_arr3.append(files[i+2])
        sub_arr4.append(files[i+3])
    for i in range(non_remainder, len(files)):
        sub_arr1.append(files[i])

    #print(sub_arr1)
    #print("")
    #print(sub_arr2)
    #print("")
    #print(sub_arr3)
    #print("")
    #print(sub_arr4)

    return(sub_arr1, sub_arr2, sub_arr3, sub_arr4)