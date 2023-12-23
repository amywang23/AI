#k means ++ select initial values
import sys
import random
from time import perf_counter
from PIL import Image
from random import randrange
from collections import defaultdict
import numpy as np

dict = defaultdict(list)
meanlist = []

k = 8

def  vector_quantization(img, pix, grouplist):
    global meanlist

    colorband = int(img.size[0]/k)
    newimg = Image.new("RGB", (img.size[0], img.size[1]+colorband), (255, 255, 255))
    newpix = newimg.load()
    i = 0
    for group in grouplist:
        for p in group:
            newpix[p[0],p[1]] = (int(meanlist[i][0]),int(meanlist[i][1]),int(meanlist[i][2]))
        i += 1

    
    for ii in range(k):
        for i in range(colorband):
            for j in range(colorband):
                x = ii*colorband + i
                y = img.size[1]+j
                newpix[x,y] = (int(meanlist[ii][0]),int(meanlist[ii][1]),int(meanlist[ii][2]))

    return newimg

def find_initial_means_random(pix):
    global k
    meanlist = []

    while True:
        x = randrange(0, 256)
        y = randrange(0, 256)
        color = pix[x,y]
        if not color in meanlist:
            meanlist.append(color)
        if len(meanlist) == k:
            break
    
    print("random means:", meanlist)
    return meanlist

def find_initial_means_plus(pix):
    global k
    meanlist = []

    x = randrange(0, 256)
    y = randrange(0, 256)
    color = pix[x,y]
    meanlist.append(color)
    #print("first pick", color)

    count = 1
    while True:
        if (count > 2*k):
            break
        #print("round", count, "meanlist size", len(meanlist))
        count += 1
        grouplist = []
        for i in range(len(meanlist)):
            g = []
            grouplist.append(g)
     
        nextcolor = meanlist[0]
        max = 0
        for color in dict:
            min = 100000000
            idx = -1
            for i in range(len(meanlist)):
                squared_error = (color[0]-meanlist[i][0])**2 + (color[1]-meanlist[i][1])**2 +  (color[2]-meanlist[i][2])**2 
                if squared_error < min:     #find min to each mean
                    min = squared_error
                    idx = i
            #print("color", color, "min", min, "idx", idx, "max", max)
            if min > max:           #find the max distance among all
                max = min
                nextcolor = color
            grouplist[idx].extend(dict[color])
      
        if not nextcolor in meanlist:
            meanlist.append(nextcolor)
            #print(len(meanlist), "nextcolor", nextcolor)
        if len(meanlist) == k:
            break

    print("++meanlist:", meanlist)
    return meanlist

def build_rgb_dcit(img, pix):
    global dict
    dict = defaultdict(list)
    for x in range (img.size[0]):
            for y in range (img.size[1]):
                color = pix[x,y]
                if color in dict:
                    dict[color].append((x,y))
                else:
                    dict[color] = [(x,y)]
    print("dict size", len(dict))
    
    return dict

def k_means(img, pix):
    global meanlist, k, dict
    
    dict = build_rgb_dcit(img, pix)
    meanlist = find_initial_means_plus(pix)
    #meanlist = random.sample(list(dict.keys()), k)
    
    oldgrouplist = [[[]] * k]

    counter = 0
    while True:
        grouplist = []
        for i in range(k):
            g = []
            grouplist.append(g)
        counter += 1
        #print("\n\nstarting round ", counter, "current mean list", meanlist)
        
        for color in dict:
            #print(color, dict[color])
            min = 1000000
            idx = -1
            for i in range(k):
                squared_error = (color[0]-meanlist[i][0])**2 + (color[1]-meanlist[i][1])**2 +  (color[2]-meanlist[i][2])**2 
                if squared_error < min:
                    min = squared_error
                    idx = i
            grouplist[idx].extend(dict[color])
                   
        newmeanlist = []
        count = 0
        for g in grouplist: #each group
            glen = len(g)
            #print("group", count, "size", glen)

            suml = [0.0,0.0,0.0]
            for p in g:     #each pixel in this group
                #print("group", count, p)
                s = pix[p[0], p[1]]
                for i in range(3):
                    suml[i] += s[i]
            #print("sum", suml)
                    
            newmeanlist.append((suml[0]/glen, suml[1]/glen, suml[2]/glen))
            count = count+1
        
        #print("new mean list", newmeanlist)

        nextround = False
        for i in range(k):
            if len(oldgrouplist[i]) != len(grouplist[i]):
                nextround = True
                break
        if nextround == False:
            break
            
        oldgrouplist = grouplist.copy()
        meanlist = newmeanlist
        
    print("total round", counter)
    # for i in range(k):
    #     print("\nMean ", i, meanlist[i], "group size", len(grouplist[i]) )

    return grouplist

def dither(img, nc):

    return

def find_initial_means(img, pix):
    #build_rgb_dcit(img, pix)
    find_initial_means_plus(pix)

def get_new_val(old_val, nc):
    return np.round(old_val * (nc - 1)) / (nc - 1)

def fs_dither(img, nc):
    arr = np.array(img, dtype=float) / 255

    w = img.size[0]
    h = img.size[1]
    for ir in range(h):
        for ic in range(w):
            # NB need to copy here for RGB arrays otherwise err will be (0,0,0)!
            old_val = arr[ir, ic].copy()
            new_val = get_new_val(old_val, nc)
            arr[ir, ic] = new_val
            err = old_val - new_val
            # In this simple example, we will just ignore the border pixels.
            if ic < w - 1:
                arr[ir, ic+1] += err * 7/16
            if ir < h - 1:
                if ic > 0:
                    arr[ir+1, ic-1] += err * 3/16
                arr[ir+1, ic] += err * 5/16
                if ic < w - 1:
                    arr[ir+1, ic+1] += err / 16

    carr = np.array(arr/np.max(arr, axis=(0,1)) * 255, dtype=np.uint8)
    return Image.fromarray(carr)

#python pic-red.py puppy.jpg 3
filename = sys.argv[1]
k = int(sys.argv[2])

img = Image.open(filename) 
#img.show() 

#print(img.size) # A tuple. Note: width first THEN height. PIL goes [x, y] with y counting from the top of the frame.
pix = img.load() # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so.
# print(pix[2,5]) # Access the color at a specific location; note [x, y] NOT [row, column].
# pix[2,5] = (255, 255, 255) # Set the pixel to white. Note this is called on “pix”, but it modifies “img”.


# start = perf_counter()
# grouplist = k_means(img,pix)
# img = vector_quantization(img, pix, grouplist)
# #img.show() # Now, you should see a single white pixel near the upper left corner
# img.save("kmeansout.png") # Save the resulting image. Alter your filename as necessary.
# end = perf_counter()
# print("total time", end-start)

newimg = fs_dither(img, 3)
newimg.show()