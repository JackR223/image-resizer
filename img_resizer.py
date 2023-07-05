# import required module
import os
import PIL
import PIL.ImageOps as ImageOps
import cv2
import numpy

def compress(source_dir, target_dir, target_size):

    # COULD USE TWO SEPARATE MODES, ONE TO TRIM TO FIXED DIMENSIONS + ONE TO TRIM TO FIXED FILE SIZE

    # iterate over files in source_dir
    for filename in os.listdir(source_dir):

        print("resizing: " + filename)

        image_in = PIL.Image.open(source_dir + "/" + filename)
        h,w = image_in.size

        res = max(h, w) / 2  

        while True:

            res = int(res)

            image_out = ImageOps.contain(image_in, (res, res))

            image_out = cv2.cvtColor(numpy.array(image_out), cv2.COLOR_RGB2BGR)
            #f = os.path.join('resized', filename)
            f = target_dir + "/" + filename
            print(f)

            x = open(f, 'a')
            x.close()
        
            cv2.imwrite(f, image_out)

            size = (os.stat(f).st_size)/1000
            size = size

            if size >= target_size*0.9 and size <= target_size:
                # resolution is close enough to target
                break
            elif size < target_size:
                # increase resolution:
                res = res + (res/2)
            elif size > target_size:
                # decrease resolution:
                res = res/2