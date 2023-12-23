import sys
from collections import defaultdict, deque
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

def BFS(dimen, line):
    fringe = deque()
    visited = set()
    moves = 0
    #add grid into both queue and set
    fringe.append((moves, line))
    visited.add(line)
    while len(fringe) != 0:
        v = fringe.popleft()
        #youre done if true
        if checkgoal(v[1]):
            return v
        children = get_children(dimen, v[1])
        for child in children:
            if child not in visited:
                #move+1
                fringe.append((v[0]+1,child))
                visited.add(child)
    return None

def biBFS(dimen, start, end):
    q1 = deque()
    q2 = deque()
    visited1 = set()
    visited2 = set()
    moves1 = 0
    moves2 = 0
    path1 = []
    path2 = []
    path1.append(start)
    path2.append(end)
    q1.append((moves1, start, path1))
    q2.append((moves2, end, path2))
    visited1.add(start)
    visited2.add(end)
    map1 = defaultdict(list)
    map2 = defaultdict(list)
    map1[start] = path1
    map2[end] = path2
    
    while len(q1) != 0 and len(q2) != 0:
        v1 = q1.popleft()
        v2 = q2.popleft()
        #youre done if true
        if v1[1] == end:
            return v1[2]
        if v2[1] == start:
            return v2[2]
        
        children1 = get_children(dimen, v1[1])
        children2 = get_children(dimen, v2[1])
        
        for child in children1:
            if child not in visited1:
                npath = []
                for elem in v1[2]:
                    npath.append(elem)
                npath.append(child)
                q1.append((v1[0]+1,child, npath))
                visited1.add(child)
                map1[child] = npath
                if child in visited2:
                    list1 = map2[child]
                    list1.pop()
                    list1.reverse()
                    return map1[child] + list1
        for child in children2:
            if child not in visited2:
                npath = []
                for elem in v2[2]:
                    npath.append(elem)
                npath.append(child)
                q2.append((v2[0]+1,child, npath))
                visited2.add(child)
                map2[child] = npath
                if child in visited1:
                    list2 = map2[child]
                    list2.pop()
                    list2.reverse()
                    return map1[child] + list2
    return None

# for loop, separate size of puzzle and the actual puzzle, input into the function
for index, elem in enumerate(line_list):
    elemlist = elem.split(" ")
    goal = find_goal(elemlist[1])
    start = perf_counter()
    result = BFS(int(elemlist[0]), elemlist[1])
    end = perf_counter()
    print("Line", index, ":", elemlist[1], ",", result[0], "moves found in", end-start, "seconds")
    start = perf_counter()
    result = biBFS(int(elemlist[0]), elemlist[1], goal)
    end = perf_counter()
    print("Line", index, ":", elemlist[1], ",", len(result)-1, "moves found in", end-start, "seconds")
    print()