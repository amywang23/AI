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
    selected = random.sample(starlist, k)
    grouplist = [[],[],[],[],[],[]]

    for star in starlist:
        min = 1000000
        idx = -1
        for i in range(k):
            squared_error = (star[0]-selected[i][0])**2 + (star[1]-selected[i][1])**2 +  (star[2]-selected[i][2])**2 + (star[3]-selected[i][3])**2
            if squared_error < min:
                min = squared_error
                idx = i
        grouplist[idx].append(star)

    meanlist = []
    count = 0
    for g in grouplist:
        glen = len(g)
        print(glen)

        suml = [0.0,0.0,0.0,0.0]
        for s in g:
            #print("group", count, s)
            for i in range(4):
                suml[i] += s[i]
            #print(suml)
            
        meanlist.append((suml[0]/glen, suml[1]/glen, suml[2]/glen, suml[3]/glen))
        count = count+1
    
    for i in range(k):
        print(selected[i])
        print(meanlist[i])
        print()

    return 

build_data(line_list)
#print(starlist)
k_means()
