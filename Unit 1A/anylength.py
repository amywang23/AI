from collections import defaultdict, deque
from time import perf_counter
import sys


start = perf_counter()

f1 = sys.argv[1]
f2 = sys.argv[2]

with open(f1) as f:
    l1 = [line.strip() for line in f]

with open(f2) as f:
    l2 = [line.strip() for line in f]

def createDict(l1):
    dict = defaultdict(list)
    for word in l1:
        for j in range(len(word)):
            match = word[:j] + "*" + word[j + 1:]
            dict[match].append(word)
            match1 = word[:j] + '-' + word[j + 1:]  
            dict[match1].append(word)   
            match2 = word[:j] + "*"+ word[j:]
            dict[match2].append(word)
        match3 = word+"*"
        dict[match3].append(word)

    return dict

def findNonSingles(dict):
    nonsingles = set([])
    count = 0
    for key in dict.keys():
        count += 1
        if key not in nonsingles and len(dict[key]) > 1:
            for elem in dict[key]:
                nonsingles.add(elem)
    for key in list(dict):
        if len(dict[key]) == 1:
            del dict[key]  ## reduces dict size
    return nonsingles

def findClumps(dictionary, nonsingles):
    result=[]
    clumps = []
    visit = set()
    wlist = list(nonsingles)

    component = 0
    max = 0
    maxgroup = []
    morethanone = 0
    for startword in wlist:
        if startword not in visit:
            newgroup = BFS(startword, dictionary, visit)
            clumps.append(newgroup)
            component += 1
            if (len(newgroup) > 1):
                morethanone += 1
            if (max < len(newgroup)):
                max = len(newgroup)
                maxgroup = newgroup
            #print("component: ", str(component), ", group len:",  str(len(newgroup)), ", group: ", newgroup)

    #print("clumps number: ", str(len(clumps)), ", more than one word: ", str(morethanone))
    #print("largest clump: ", str(len(maxgroup)), ", ", maxgroup)
    result.append(len(maxgroup))
    result.append(morethanone)
    result.append(maxgroup)
    return result

def BFS(startword, dictionary, visit):       #called by findclumps
    group = [startword]
    visit.add(startword)
    q = deque([startword])
    
    while q:
        for i in range(len(q)):
            word = q.popleft()

            for j in range(len(word)):
                match = word[:j] + "*" + word[j + 1:]
                match1 = word[:j] + '-'+ word[j + 1:]
                match2 = word[:j] + "*"+ word[j:]
                match3 = word+"*"
                allmatchs = dictionary[match] + dictionary[match1] + dictionary[match2]+dictionary[match3]
                
                for dictword in allmatchs:
                    if dictword not in visit:
                        visit.add(dictword)
                        q.append(dictword)
                        group.append(dictword)

    return group


def findMaxLadderAll(maxgroup):
    dict = createDict(maxgroup)

    maxpath = []
    
    maxpath = findMaxLadderOneWord(maxgroup[0], dict)
    maxpath = findMaxLadderOneWord(maxpath[-1], dict) 

    #print("max ladder len: ", str(maxpath))
    #print("max ladder ", maxpath)

    return maxpath

def findMaxLadderOneWord(start, dict):
    
    visit = set([start])
    q = deque()
    path = []
    path.append(start)
    q.append((start, path))
    res = 0
    finalpath=[]
    max = 0
   
    while len(q) > 0:
        for i in range(len(q)):
            word = q.popleft()

            allmatchs = set()

            for j in range(len(word[0])):
                match = word[0][:j] + "*" + word[0][j + 1:]
                match1 = word[0][:j] + '-'+ word[0][j + 1:]
                match2 = word[0][:j] + "*"+ word[0][j:]
                match3 = word[0]+"*"
                allmatchs.update(dict[match] + dict[match1] + dict[match2]+dict[match3])

            for dictword in allmatchs:
                if dictword not in visit and dictword not in word[1]:
                    newpath = []
                    for item in word[1]: newpath.append(item)
                    newpath.append(dictword)
                    visit.add(dictword)
                    q.append((dictword, newpath))
                    if (max < len(newpath)):
                        max=len(newpath)
                        finalpath = newpath

    return finalpath

def ladderLength(start, end, l1, dict):
    if end not in l1:
        return None
    visit = set([start])
    q = deque()
    path = []
    path.append(start)
    q.append((start, path))
    res = 1
    while q:
        for i in range(len(q)):
            v = q.popleft()
            word = v[0]

            if word == end:
                #print(v[1])
                return v[1]
            for j in range(len(word)):
                match = word[:j] + "*" + word[j + 1:]
                match1 = word[:j] + '-'+ word[j + 1:]
                match2 = word[:j] + "*"+ word[j:]
                match3 = word+"*"
                allmatchs = dict[match] + dict[match1] + dict[match2]+dict[match3]
                
                for dictword in allmatchs:
                    if dictword not in visit:
                        newpath = []
                        for item in v[1]: newpath.append(item)
                        newpath.append(dictword)
                        visit.add(dictword)
                        q.append((dictword, newpath))
        res += 1

    return None

start = perf_counter()
dict = createDict(l1)
end = perf_counter()
print('Time to create the data structure was:', (end-start), 'seconds.')
print('There are ', (len(l1)), 'words in this dict.')

start = perf_counter()
for index, elem in enumerate(l2):
    currentline = l2[index].split()
    result = ladderLength(currentline[0], currentline[1], l1, dict)
    #result = ladderLength('tiler', 'atoner', l1, dict)
    if result==None:
        print ("No solution! ", currentline[0], '--', currentline[1])
    else:
        print('Length of solution: ', (len(result)))
        for r in result:
            print(r)
    print()

end = perf_counter()
print('Time to solve all of these puzzles was:', (end - start), 'seconds')

start = perf_counter()
nonsingles = findNonSingles(dict)
print('1) There are ', len(l1)-len(nonsingles), 'singletons.')
result1 = findClumps(dict, nonsingles)
end = perf_counter()
print('2) The biggest subcomponent has ', result1[0], ' words.')
print('3) There are ', result1[1], 'clumps (subgraphs with at least two words).')
print('Questions 1-3 answered in', end-start, 'seconds.')

start = perf_counter()
result2 = findMaxLadderAll(result1[2])
end = perf_counter()
print('4) The longest path is: [[',result2[0],', ', result2[-1], '], ', len(result2), '], found in ', end-start,' seconds.')
print('The solution to this puzzle is:')
print('Length of solution: ', len(result2))
for r in result2:
    print(r)