import sys
from collections import deque
from time import perf_counter

line_list = ["3 FDGHE.CBA", "3 HFGBEDC.A"]
    
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

def BFS(dimen, line):
    fringe = deque()
    visited = set()
    moves = 0
    path = []
    path.append(line)
    #add grid into both queue and set
    fringe.append((moves, line, path))
    visited.add(line)
    while len(fringe) != 0:
        v = fringe.popleft()
        #youre done if true
        if checkgoal(v[1]):
            print(*v[2], sep=", ")
            print(v[0])
            print(len(v[2]))
            return v
        children = get_children(dimen, v[1])
        for child in children:
            if child not in visited:
                newp = []
                for elem in v[2]: newp.append(elem)
                newp.append(child)
                #move+1
                fringe.append((v[0]+1,child, newp))
                visited.add(child)
    return None

# for loop, separate size of puzzle and the actual puzzle, input into the function
for index, elem in enumerate(line_list):
    start = perf_counter()
    elemlist = elem.split(" ")
    result = BFS(int(elemlist[0]), elemlist[1])
    end = perf_counter()
    print("Line", index, ":", elemlist[1], ",", result[0], "moves found in", end-start, "seconds")