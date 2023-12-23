from math import log
from collections import defaultdict
import random
from random import randrange

k = 6
starlist = []
dict = defaultdict(list)

with open("star_data.csv") as f:
    line_list = [line.strip() for line in f]

def build_data(line_list):
    global starlist

    for idx, line in enumerate(line_list):
        if (idx == 0):
            continue
        currentline = line_list[idx].split(",")
        star = (log(int(currentline[0])),log(float(currentline[1])),log(float(currentline[2])),float(currentline[3]))
        starlist.append(star)
        dict[star] = int(currentline[4])

    return starlist

def k_means():
    meanlist = random.sample(starlist, k)
    oldgrouplist = [[],[],[],[],[],[]]

    counter = 0
    while True:
        grouplist = [[],[],[],[],[],[]]
        counter += 1
        # print("\n\nstarting round ", counter)
        # print("current mean list", meanlist)
        for star in starlist:
            min = 1000000
            idx = -1
            for i in range(k):
                squared_error = (star[0]-meanlist[i][0])**2 + (star[1]-meanlist[i][1])**2 +  (star[2]-meanlist[i][2])**2 + (star[3]-meanlist[i][3])**2
                if squared_error < min:
                    min = squared_error
                    idx = i
            grouplist[idx].append(star)

        newmeanlist = []
        count = 0
        for g in grouplist: #each group
            glen = len(g)
            #print(glen)

            suml = [0.0,0.0,0.0,0.0]
            for s in g:     #each star in this group
                #print("group", count, s)
                for i in range(4):
                    suml[i] += s[i]
                #print(suml)
                
            newmeanlist.append((suml[0]/glen, suml[1]/glen, suml[2]/glen, suml[3]/glen))
            count = count+1
        # print("new gen mean list", newmeanlist)

        nextround = False
        for i in range(k):
        #     print(meanlist[i])
        #     print(newmeanlist[i])
        #     print()
            # print("group", i, "old len",len(oldgrouplist[i]), "new len", len(grouplist[i]) )
            # print("old group", oldgrouplist[i])
            # print("------------------------------------------")
            # print("new group", grouplist[i])
            # print("**************************************")
            if len(oldgrouplist[i]) != len(grouplist[i]):
                nextround = True
                break
        if nextround == False:
            break
        
        oldgrouplist = grouplist.copy()
        meanlist = newmeanlist

    for i in range(k):
        print("\nMean ", i, meanlist[i] )
        for g in grouplist[i]:
            print(g, " -----> ", dict[g])
        print("\n................................................")

    return 

build_data(line_list)
#print(starlist)
k_means()
