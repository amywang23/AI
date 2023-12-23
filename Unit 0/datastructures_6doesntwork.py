import sys;
from heapq import heappush, heappop, heapify

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

# print(len(final))

#2
res = []
[res.append(x) for x in l1 if x not in res]
uniq = res[99::100]
count = sum(uniq)
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
list.sort()
newlist = [x for x in list[:10:]]
# print(newlist)

#5
# if the count of the number is >= 2 in file 2, add into a list (?). get rid of everything but the first 10?
newlist2 = []
for elem in l2:
    if l2.count(elem) >= 2:
        newlist2.append(elem)
newset = set(newlist2)
newlist3 = sorted(newset)
newlist3.sort(reverse = True)
result = [x for x in newlist3[:10:]]
# print(result)

#6
finallist = []
min = l1[0]
for index in range(len(l1)):
    if (l1[index] % 53) == 0:
        #print(l1[:index:])
        for ele in l1[:index:]:
            if ele < min:
                min = ele
        #         print("test", min)
        # print(min in finallist)
        if (min in finallist) == False:
            finallist.append(min)
print(finallist)

#7
end = perf_counter()
print("Total time:", end - start)