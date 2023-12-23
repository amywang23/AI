import heapq
import sys
from collections import deque
from time import perf_counter

f = sys.argv[1]

with open(f) as f:
    line_list = [line.strip() for line in f]
    
def find_goal(line):
    goalgrid = ''.join(sorted(line))
    goal = goalgrid.replace('.', '')               
    return(goal + ".")

def get_children(dimen, line):
    dot = line.index('.')
    final = []
    #move left
    if dot%dimen > 0:
        final.append(switch(line, dot - 1, dot))
    #move right
    if dot%dimen < dimen - 1:
        final.append(switch(line, dot, dot + 1))
    #move up
    if dot//dimen > 0:
        final.append(switch(line, dot - dimen, dot))
    #move down
    if dot//dimen < dimen - 1:
        final.append(switch(line, dot, dot + dimen))
    return final

def checkgoal(line):
    return line == find_goal(line)

#i1 < i2
def switch(line, i1, i2):
    s1 = line[:i1]
    s2 = line[i1 + 1: i2]
    s3 = line[i2 + 1:]
    final = s1 + line[i2] + s2 + line[i1] + s3
    return (final)

def AstarSearch(dimen, start):
    closed = set()
    f = taxiCab(dimen, start)
    
    fringe = []
    heapq.heapify(fringe)
    heapq.heappush(fringe, (f, start, 0))
    
    while len(fringe) != 0:
        v = heapq.heappop(fringe)
        if checkgoal(v[1]):
            return v
        if v[1] not in closed:
            closed.add(v[1])
            children = get_children(dimen, v[1])
            for child in children:
                if child not in closed:
                    f = taxiCab(dimen, child) + v[2]+1
                    heapq.heappush(fringe, (f,child, v[2]+1))
    return None


def checkParity(start):
    count = 0
    for i in range(len(start)):
        for j in range(i+1, len(start)):
            if start[i] != '.' and start[j] != '.':
                if start[i] > start[j]:
                    count += 1
    return count

def taxiCab(dimen, start):
    goal = find_goal(start)
    sum = 0
    for i in range(dimen*dimen):
        if start[i] == '.':
            continue
        goalpos = goal.index(start[i])
        row1 = int(i/dimen)
        col1 = i%dimen
        row2 = int(goalpos/dimen)
        col2 = goalpos%dimen
        sum += abs(row2-row1) + abs(col2-col1)
    return sum

def solvable(dimen, start):
    parity = checkParity(start)
    if dimen%2 == 1:
        return (parity%2==0)
    else:
        pos = start.index('.')
        if(int(pos/dimen) %2 ==0):
            return (parity%2==1)
        else:
            return (parity%2==0)

for index, elem in enumerate(line_list):
    start = perf_counter()
    elemlist = elem.split(" ")
    
    if(solvable(int(elemlist[0]), elemlist[1])):
        result = AstarSearch(int(elemlist[0]), elemlist[1])
        end = perf_counter()
        print("Line", index, ":", elemlist[1], ",", result[2], "moves found in", end-start, "seconds")
    else:
        print("Line", index, ":", elemlist[1], ", no solution determined in", end-start, "seconds")
    print()