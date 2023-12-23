from configparser import NoOptionError
import sys
from collections import deque, defaultdict
from time import perf_counter
from venv import create

#1 create all the dicts (occurs in creating dict method) and loop through all the keys to see which keys only have one value (singleton) (add all singles into a set, print length of set)
#3 create dict, loop through all words in list, use dfs to find clumps

with open("words_06_letters.txt") as f:
    l1 = [line.strip() for line in f]

with open("puzzles_normal.txt") as f:
    l2 = [line.strip() for line in f]

    
def find_goal(line):
    goalgrid = ''.join(sorted(line))
    goal = goalgrid.replace('.', '')               
    return(goal + ".")

def checkgoal(line):
    return line == find_goal(line)

#i1 < i2
def switch(line, i1, i2):
    s1 = line[:i1]
    s2 = line[i1 + 1: i2]
    s3 = line[i2 + 1:]
    final = s1 + line[i2] + s2 + line[i1] + s3
    return (final)

def BFS(start, wlist, dict, visited):
    g = [start]
    visited.add(start)
    q = deque([start])
    
    while q:
        for i in range(len(q)):
            v = q.popleft()
            for index in range(0,len(v)):
                match = v[:index] + "." + v[index + 1:] 
                for wordstep in dict[match]:
                    if wordstep not in visited:
                        visited.add(wordstep)
                        q.append(wordstep)
                        g.append(wordstep)
                        wlist.remove(wordstep)
    return g

def createDict(l1):
    dict = defaultdict(list)
    for elem in l1:
        for index in range(0,len(elem)):
            match = elem[:index] + "." + elem[index + 1:]
            dict[match].append(elem)
    return dict

def findSingle(dict, l1):
    notsingles = set()
    for k in dict:
        if len(dict[k]) > 1:
            for elem in dict[k]:
                notsingles.add(elem)
    print("# of singletons: ", str(len(l1) - len(notsingles)))
    
def findClump(wlist):
    dict = createDict(wlist)
    clump=[]
    visited = set()
    num = 0
    max = 0
    maxes = []
    morethanone = 0
    for start in list(wlist):
        if start not in visited:
            newg = BFS(start, wlist, dict, visited)
            print(newg)
            clump.append(newg)
            wlist.remove(start)
            num += 1
            if len(newg) > 1:
                morethanone +=1
            if max < len(newg):
                max = len(newg)
                maxes = newg
                
    print("clump #:", len(clump))
    print("largest clump #:", len(maxes))            
                
    maxDict = createDict(maxes)
    maxlen = 0
    maxPath = []
    for elem in maxes:
        onerunPath = maxLadderLength(elem, maxDict)
        if maxlen < len(onerunPath):
            maxlen = len(onerunPath)
            maxPath = onerunPath
    print("Max length:", maxlen)
    print("Max path:", maxPath)
    return clump
    
def maxLadderLength(start, dict):
    visited = set([start])
    q = deque()
    max = 0
    finalPath = []
    path = [start]
    q.append((start, path)) #push start word and path in
    
    res = 0
    
    while q:
        for i in range(len(q)):
            v = q.popleft()
            for index in range(0,len(v[0])):
                match = v[0][:index] + "." + v[0][index + 1:] 
                for wordstep in dict[match]:
                    if wordstep not in visited:
                        newp = []
                        for elem in v[1]: newp.append(elem)
                        newp.append(wordstep)
                        q.append((wordstep, newp))
                        visited.add(wordstep)
                        if max < len(newp):
                            max = len(newp)
                            finalPath = newp
        res += 1
    return finalPath

# for loop, separate size of puzzle and the actual puzzle, input into the function
start = perf_counter()
dict = createDict(l1)
end = perf_counter()
print("Time used to generate data structure: ", end-start)
# print(findSingle(dict, l1))
findClump(l1)