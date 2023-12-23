#working version but slow
#python pic-part2-slow.py puppy.jpg 8

import sys
from time import perf_counter
from PIL import Image
from random import randrange

meanlist = []

k = 8

def  vector_quantization(img, pix, grouplist):
    global meanlist

    newimg = Image.new("RGB", (img.size[0], img.size[1]), 0)
    newpix = newimg.load()
    i = 0
    for group in grouplist:
        for p in group:
            newpix[p[0],p[1]] = (int(meanlist[i][0]),int(meanlist[i][1]),int(meanlist[i][2]))
        i += 1
            
    return newimg

def find_initial_means(pix):
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
    
    #print(meanlist)
    return meanlist

def k_means(img, pix):
    global meanlist, k

    meanlist = find_initial_means(pix)
    oldgrouplist = [[[]] * k]

    counter = 0
    while True:
        grouplist = []
        for i in range(k):
            g = []
            grouplist.append(g)
        counter += 1
        print("\n\nstarting round ", counter, "current mean list", meanlist)
        
        for x in range (img.size[0]):
            for y in range (img.size[1]):
                color = pix[x,y]
                min = 1000000
                idx = -1
                for i in range(k):
                    squared_error = (color[0]-meanlist[i][0])**2 + (color[1]-meanlist[i][1])**2 +  (color[2]-meanlist[i][2])**2 
                    if squared_error < min:
                        min = squared_error
                        idx = i
                grouplist[idx].append((x,y))
                #print("x", x, "y", y, "idx", idx, grouplist[idx])
                
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
        #     print(meanlist[i])
        #     print(newmeanlist[i])
        #     print()
            #print("group", i, "old len",len(oldgrouplist[i]), "new len", len(grouplist[i]) )
            # print("old group", oldgrouplist[i])
            # print("------------------------------------------")
            # print("new group", grouplist[i])
            #print("**************************************")
            if len(oldgrouplist[i]) != len(grouplist[i]):
                nextround = True
                break
        if nextround == False:
            break
            
        oldgrouplist = grouplist.copy()
        meanlist = newmeanlist
        

    for i in range(k):
        print("\nMean ", i, meanlist[i], "group size", len(grouplist[i]) )

    return grouplist

filename = sys.argv[1]
k = int(sys.argv[2])

img = Image.open(filename) 
#img.show() 

#print(img.size) # A tuple. Note: width first THEN height. PIL goes [x, y] with y counting from the top of the frame.
pix = img.load() # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so.
# print(pix[2,5]) # Access the color at a specific location; note [x, y] NOT [row, column].
# pix[2,5] = (255, 255, 255) # Set the pixel to white. Note this is called on “pix”, but it modifies “img”.

start = perf_counter()
grouplist = k_means(img,pix)
img = vector_quantization(img, pix, grouplist)
img.show() # Now, you should see a single white pixel near the upper left corner
img.save("kmeansout.png") # Save the resulting image. Alter your filename as necessary.
end = perf_counter()
print("total time", end-start)