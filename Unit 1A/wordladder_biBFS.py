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

def biBFS(start, end, dict):
    q1 = deque()
    q2 = deque()
    visited1 = set()
    visited2 = set()
    visited1.add(start)
    visited2.add(end)
    path1 = []
    path2 = []
    path1.append(start)
    path2.append(end)
    q1.append(( start, path1))
    q2.append(( end, path2))
    map1 = defaultdict(list)
    map2 = defaultdict(list)
    map1[start] = path1
    map2[end] = path2
    while len(q1) != 0 and len(q2) != 0:
        for elem in range(len(q1)):
            v= q1.popleft()
            word = v[0]
            if word == end or word in visited2:
                list2 = map2[word]
                list2.pop()
                list2.reverse()
                print(word)
                print(map1[word])
                print(map2[word])
                return map1[word] + list2
            for index in range(0,len(word)):
                match = word[:index] + "." + word[index + 1:]
                for wordstep in dict[match]:
                    if wordstep not in visited1:
                        newp = []
                        for elem in v[1]: newp.append(elem)
                        newp.append(wordstep)
                        q1.append((wordstep, newp))
                        visited1.add(wordstep)
                        map1[wordstep] = newp
        for elem in range(len(q2)):
            v= q2.popleft()
            word = v[0]
            if word == start or word in visited1:
                list2 = map2[word]
                list2.pop()
                list2.reverse()
                print(word)
                print(map1[word])
                print(map2[word])
                return map1[word] + list2
            for index in range(0,len(word)):
                match = word[:index] + "." + word[index + 1:]
                for wordstep in dict[match]:
                    if wordstep not in visited2:
                        newp = []
                        for elem in v[1]: newp.append(elem)
                        newp.append(wordstep)
                        q2.append((wordstep, newp))
                        visited2.add(wordstep)
                        map2[wordstep] = newp
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
        print("Length of BFS ladder:0", " Time:", end-start, "seconds")
    else:
        print("Length of BFS ladder:", len(result), " Each word in ladder:", result, ",", " Time:", end-start, "seconds")
    start = perf_counter()
    elemlist = elem.split(" ")
    result = biBFS((elemlist[0]), elemlist[1], dict)
    end = perf_counter()
    if result == None:
        print("Length of biBFS ladder:0", " Time:", end-start, "seconds")
    else:
        print("Length of biBFS ladder:", len(result), " Each word in ladder:", result, ",", " Time:", end-start, "seconds")
    print()