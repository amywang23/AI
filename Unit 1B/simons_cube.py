import heapq
import sys
from collections import deque
from time import perf_counter

f = sys.argv[1]

with open(f) as f:
    line_list = [line.strip() for line in f]
    
def find_goal(dimen):
    len = dimen*dimen             
    return()

def get_children(dimen, board, cube):
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
def switch(board, i1, i2):
    s1 = board[:i1]
    s2 = board[i1 + 1: i2]
    s3 = board[i2 + 1:]
    final = s1 + board[i2] + s2 + board[i1] + s3
    return (final)

def rollRight(cube):
    l = cube.split()
    temp = l[2]
    l[2] = l[5]
    l[5] = l[3]
    l[3] = l[4]
    l[4] = temp
    return ''.join(l)
    
def rollLeft(cube):
    l = cube.split()
    temp = l[2]
    l[2] = l[4]
    l[4] = l[3]
    l[3] = l[5]
    l[5] = temp
    return ''.join(l)

def rollUp(cube):
    l = cube.split()
    temp = l[2]
    l[2] = l[0]
    l[0] = l[3]
    l[3] = l[1]
    l[1] = temp
    return ''.join(l)
    
def rollDown(cube):
    l = cube.split()
    temp = l[2]
    l[2] = l[1]
    l[1] = l[3]
    l[3] = l[0]
    l[0] = temp
    return ''.join(l)

def AstarSearch(dimen, board, cube):
    closed = set()
    f = taxiCab(dimen, start)
    
    fringe = []
    heapq.heapify(fringe)
    heapq.heappush(fringe, (f, board, cube, 0))
    
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