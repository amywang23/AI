import sys;
from heapq import heappush, heappop, heapify, nsmallest, nlargest

from time import perf_counter
start = perf_counter()
#All your code goes here, including reading in the files and printing your output
f1, f2, f3 = sys.argv[1], sys.argv[2], sys.argv[3]

with open(f1) as f:
    l1 = [int(line.strip()) for line in f]
with open(f2) as f: 
    l2 = [int(line.strip()) for line in f]
with open(f3) as f:
    l3 = [int(line.strip()) for line in f]

#1
set1 = set(l1)
set2 = set(l2)
set3 = set(l3)
final = set1.intersection(set2)
print("#1:", len(final))

#2
def removeDupFromSeq(seq):
    #go thru the list and add to set every time
    #when set length is %100 == 0, sum+= the number you j added
    alist = set()
    alist2 = alist.add
    return [x for x in seq if not (x in alist or alist2(x))]

uniq = removeDupFromSeq(l1)
result = [int(x) for x in uniq[99::100]]
print("#2:", sum(result))

#3
count1 = 0
united = set1.union(set2)
intersectedset = set3.intersection(united)

uniquelist = [i for i in l1 if i in intersectedset]
uniquelist2 = [i for i in l2 if i in intersectedset]
print("#3:", len(uniquelist) + len(uniquelist2))

#4 use heaps and heappop
# list = list(set1)
# newlist = nsmallest(10, list)
heapify(heap1 := list(set1))
newlist = []
count = 0
while count < 10:
    temp = heappop(heap1)
    if temp not in newlist:
        newlist.append(temp)
        count+= 1
print("#4:", newlist)


#5
maximumlist = []
negativelist = [i * -1 for i in l2]
heapify(negativelist)
gogo = True
while gogo == True:
    maximum = heappop(negativelist)
    if(len(maximumlist) == 10):
        gogo = False
    elif(l2.count(maximum*-1) >= 2):
        if(maximum not in maximumlist):
            maximumlist.append(maximum)
finallist = [i*-1 for i in maximumlist]
print("#5:", finallist)

#6
minlist = set()
heap_list = []
heapify(heap_list)
go = True
for elem in l1:
    heappush(heap_list, elem)
    if(elem % 53 ==0):
        go = True
        while go ==True:
            minimum = heappop(heap_list)
            if(minimum not in minlist):
                minlist.add(minimum)
                go = False
print("#6:", sum(minlist))

#7
end = perf_counter()
print("Total time:", end - start)