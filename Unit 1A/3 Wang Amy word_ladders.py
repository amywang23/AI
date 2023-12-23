from configparser import NoOptionError
import sys
from collections import deque, defaultdict
from time import perf_counter

f1 = sys.argv[1]
f2 = sys.argv[2]

with open(f1) as f:
    l1 = [line.strip() for line in f]

with open(f2) as f:
    l2 = [line.strip() for line in f]

    
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

def BFS(start, end, dict):
    q = deque()
    visited = set()
    moves = 0
    path = [start]
    q.append((start, path)) #push start word and path in
    visited.add(start)
    while len(q) != 0:
        v = q.popleft()
        if v[0] == end:
            return v[1]  #returning the path only
        for index in range(0,len(v[0])):
            match = v[0][:index] + "." + v[0][index + 1:]
            for wordstep in dict[match]:
                if wordstep not in visited:
                    newp = []
                    for elem in v[1]: newp.append(elem)
                    newp.append(wordstep)
                    q.append((wordstep, newp))
                    visited.add(wordstep)
    return None

def createDict(l1):
    dict = defaultdict(list)
    for elem in l1:
        for index in range(0,len(elem)):
            match = elem[:index] + "." + elem[index + 1:]
            dict[match].append(elem)
    return dict

# for loop, separate size of puzzle and the actual puzzle, input into the function
start = perf_counter()
dict = createDict(l1)
end = perf_counter()
print("Time used to generate data structure: ", end-start)
for index, elem in enumerate(l2):
    start = perf_counter()
    elemlist = elem.split(" ")
    result = BFS((elemlist[0]), elemlist[1], dict)
    end = perf_counter()
    if result == None:
        print("Length of ladder:0", " Time:", end-start, "seconds")
    else:
        print("Length of ladder:", len(result), " Each word in ladder:", result, ",", " Time:", end-start, "seconds")