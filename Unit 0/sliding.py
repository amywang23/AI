from operator import is_
import sys
from heapq import heappush, heappop, heapify, nsmallest, nlargest
from time import perf_counter

f1, f2, f3 = sys.argv[1], sys.argv[2], sys.argv[3]

with open(f1) as f:
    l1 = [int(line.strip()) for line in f]
with open(f2) as f: 
    l2 = [int(line.strip()) for line in f]
with open(f3) as f:
    l3 = [int(line.strip()) for line in f]

start = perf_counter()

end = perf_counter()
print("Total time:", end - start)