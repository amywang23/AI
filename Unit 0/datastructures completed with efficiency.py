import sys;
from heapq import heappush, heappop, heapify, nsmallest, nlargest

from time import perf_counter
start = perf_counter()
#All your code goes here, including reading in the files and printing your output
f1, f2, f3 = "10kfile1.txt", "10kfile2.txt", "10kfile3.txt"

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
print(len(final))

#2
def removeDupFromSeq(seq):
    alist = set()
    alist2 = alist.add
    return [x for x in seq if not (x in alist or alist2(x))]

uniq = removeDupFromSeq(l1)
result = [int(x) for x in uniq[99::100]]
print(sum(result))
# res = []
# [res.append(x) for x in l1 if x not in res]
# uniq = res[99::100]
# count = sum(uniq)
# print(count)

#3
count1 = 0
for element in set3:
    if element in l1:
        count1 += l1.count(element)
    if element in l2:
        count1 += l2.count(element)
# print(count1)

#4
list = list(set1)
newlist = nsmallest(10, list)
# print(newlist)

#5
# if the count of the number is >= 2 in file 2, add into a list (?). get rid of everything but the first 10?
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
# print(finallist)

#6
minlist = []
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
                minlist.append(minimum)
                go = False
# print(sum(minlist))

#7
end = perf_counter()
print("Total time:", end - start)