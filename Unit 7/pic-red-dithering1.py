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

def convert_value(old_value, numcolors):
    return np.round(old_value * (numcolors - 1)) / (numcolors - 1)

def steinberg_dither(img, numcolors):
    arr = np.array(img, dtype=float) / 255

    width = img.size[0]
    height = img.size[1]
    for i in range(height):
        for j in range(width):
            # NB need to copy here for RGB arrays otherwise err will be (0,0,0)!
            old_value = arr[i, j].copy()
            new_value = np.round(old_value * (numcolors - 1)) / (numcolors - 1)
            arr[i, j] = new_value
            err = old_value - new_value
            # In this simple example, we will just ignore the border pixels.
            if j < width - 1:
                arr[i, j+1] += err * 7/16
            if i < height - 1:
                if j > 0:
                    arr[i+1, j-1] += err * 3/16
                arr[i+1, j] += err * 5/16
                if j < width - 1:
                    arr[i+1, j+1] += err / 16

    carr = np.array(arr/np.max(arr, axis=(0,1)) * 255, dtype=np.uint8)
    return Image.fromarray(carr)

def vector_quantization_naive(img, pix, method):
    for i in range (img.size[0]):
        for j in range (img.size[1]):
            color = pix[i,j]
            newcolor = [-1,-1,-1]
            if (method == 27):
                for ii in range(3):
                    if (color[ii] < 255/ 3):
                        newcolor[ii] = 0
                    elif (color[ii] > 255*2/3):
                        newcolor[ii] = 255
                    else:
                        newcolor[ii] = 127
            if (method == 8):
                for ii in range(3):
                    if (color[ii] < 128):
                        newcolor[ii] = 0
                    else:
                        newcolor[ii] = 255
            pix[i,j] = (newcolor[0],newcolor[1],newcolor[2])
            
    return img

def color_band(img, method):
    color_list_8 = [(0,0,0),
                  (0,255,0),
                  (255,0,0),
                  (0,0,255),
                  (255,255,0),
                  (0,255,255),
                  (255,0,255),
                  (255,255,255)]
    
    color_list_27 = [(0, 255, 127),
                    (0, 127, 255),
                    (127, 0, 255),
                    (127, 255, 0),
                    (255, 0, 127),
                    (255, 127, 0),
                    (0, 0, 255),
                    (0, 255, 0),
                    (127, 0, 0),
                    (127, 127, 255),
                    (127, 255, 127),
                    (255, 0, 0),
                    (255, 0, 255),
                    (255, 127, 127),
                    (0, 127, 0),
                    (127, 0, 127),
                    (127, 127, 0),
                    (255, 127, 255),
                    (0, 0, 127),
                    (0, 127, 127),
                    (127, 0, 127),
                    (127, 127, 0),
                    (255, 0, 127),
                    (255, 127, 255),
                    (0, 0, 0),
                    (127, 127, 127),
                    (255, 255, 255)]

    if method ==8:
        colorlist = color_list_8.copy()
    else:
        colorlist = color_list_27.copy()
    print(colorlist)
    colorband = int(img.size[0]/method)
    newimg = Image.new("RGB", (img.size[0], img.size[1]+colorband), (255, 255, 255))
    newpix = newimg.load()
    width = img.size[0]
    height = img.size[1]
    print("width and height", width, height)
    for i in range(width):
        for j in range(height):
            newpix[i,j] = pix[i,j]
    
    for count in range(method):
        for i in range(colorband):
            for j in range(colorband):
                x = count*colorband + i
                y = img.size[1]+j
                newpix[x,y] = (colorlist[count][0],colorlist[count][1],colorlist[count][2])
                # print("x, ", x, "y, ", y, "newpix,", newpix[x,y])

    return newimg

#python pic-red.py puppy.jpg 3
filename = sys.argv[1]
k = int(sys.argv[2])

img = Image.open(filename) 
#img.show() 

#print(img.size) # A tuple. Note: width first THEN height. PIL goes [x, y] with y counting from the top of the frame.
pix = img.load() # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so.
# print(pix[2,5]) # Access the color at a specific location; note [x, y] NOT [row, column].
# pix[2,5] = (255, 255, 255) # Set the pixel to white. Note this is called on “pix”, but it modifies “img”.


start = perf_counter()
img_keep = img.copy()
img_naive = vector_quantization_naive(img, pix, k)
img_naive = color_band(img_naive, k)
img_naive.save("kmeansout_naive.png")
# img = img_keep.copy()
# pix = img.load()
# grouplist = k_means(img,pix)
# img = vector_quantization(img, pix, grouplist)
# #img.show() # Now, you should see a single white pixel near the upper left corner
# img.save("kmeansout.png") # Save the resulting image. Alter your filename as necessary.
# newimg = steinberg_dither(img, k)
# newimg.save("kmeansout_dither.png")

end = perf_counter()
print("total time", end-start)