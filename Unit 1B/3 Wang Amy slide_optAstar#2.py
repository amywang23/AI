import heapq
import sys
from collections import deque
from time import perf_counter

dict = {"A": (0,0),
        "B": (0,1),
        "C": (0,2),
        "D": (0,3),
        "E": (1,0),
        "F": (1,1),
        "G": (1,2),
        "H": (1,3),
        "I": (2,0),
        "J": (2,1),
        "K": (2,2),
        "L": (2,3),
        "M": (3,0),
        "N": (3,1),
        "O": (3,2)}

dict1 = {
        "0123":	0,
        "0132":	2,
        "0213":	2,
        "0231":	2,
        "0312":	2,
        "0321":	4,
        "1023":	2,
        "1032":	4,
        "1203":	2,
        "1230":	2,
        "1302":	4,
        "1320":	4,      #4 or 6
        "2013":	2,
        "2031":	4,
        "2103":	4,
        "2130":	4,
        "2301":	4,
        "2310":	4,
        "3012":	2,
        "3021":	4,
        "3102":	4,
        "3120":	4,      #4 or 6
        "3201":	4,
        "3210": 6
}

f = sys.argv[1]

with open(f) as f:
    line_list = [line.strip() for line in f]

def print_puzzle(dimen, line):
    #take line (string) : two for loops looping through dimen, print by line _  _  _ 3 ABCDEFG.H
    rows = [line[col: col+dimen] for col in range(0, len(line), dimen)]
    for val in rows:
        print(' '.join(val))
        
def find_goal(line):
    goalgrid = ''.join(sorted(line))
    goal = goalgrid.replace('.', '')               
    return(goal + ".")

def get_children(dimen, line):
    dot = line.index('.')
    final = []
    #move left
    if dot%dimen > 0:
        final.append((switch(line, dot - 1, dot), dot-1, dot))
    #move right
    if dot%dimen < dimen - 1:
        final.append((switch(line, dot, dot + 1), dot+1, dot))
    #move up
    if dot//dimen > 0:
        final.append((switch(line, dot - dimen, dot), dot-dimen, dot))
    #move down
    if dot//dimen < dimen - 1:
        final.append((switch(line, dot, dot + dimen), dot+dimen, dot))
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
    heapq.heappush(fringe, (f, start, 0, f))
    
    while len(fringe) != 0:
        v = heapq.heappop(fringe)
        if checkgoal(v[1]):
            return v
        if v[1] not in closed:
            closed.add(v[1])
            children = get_children(dimen, v[1])
            pastf = v[3]    #second f is remembering the previous f
            for child in children:
                if child[0] not in closed:
                    newf = pastf + fChange(dimen, child[0], child[1], child[2])
                    conflicts = getLinearConflict(child[0])
                    # conflicts = 0
                    f = v[2]+1+newf+conflicts
                    heapq.heappush(fringe, (f,child[0], v[2]+1, newf))
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
    print(parity)
    if dimen%2 == 1:
        return (parity%2==0)
    else:
        pos = start.index('.')
        if(int(pos/dimen) %2 ==0):
            return (parity%2==1)
        else:
            return (parity%2==0)
        
def fChange (dimen, start, p1, p2):
    row1 = int(p1/dimen)
    col1 = p1%dimen
    row2 = int(p2/dimen)
    col2 = p2%dimen
    c = start[p2]
    goalr = dict[c][0]
    goalc = dict[c][1]
    
    # print("row1:", row1, "col1:", col1, "row2:", row2, "col2:", col2, "goalr:", goalr, "goalc:", goalc)
    
    if row1 == row2:    #row didnt change (moved horizontally)
        if col1 < col2:     #old pos is less than new (moved to the right)
            if col1 < goalc:
                return -1
            else:
                return 1
        else:           #moved to the left
            if goalc < col1: 
                return -1
            else:
                return 1
    
    else:   #col didnt change (moved vertically)
        if row1 < row2:     #old pos is less than new (moved down)
            if row1 < goalr:
                return -1
            else:
                return 1
        else:           #moved up
            if goalr < row1: 
                return -1
            else:
                return 1
            
def getLinearConflict(state):
    hsum = 0
    for i in range(4):          #go though rows
        onerow = ""
        for j in range(4):
            char = state[i*4+j]
            if char == '.':
                continue
            pos = dict[char]
            if pos[0] == i:     #final position is this row
                onerow = onerow + str(pos[1])
        if len(onerow) == 2:        #2 chars belong to this row
            if onerow[0] > onerow[1]:
                hsum = hsum + 2
        if len(onerow) == 3:        #3 chars belong to this row
            if onerow[0]>onerow[1] and onerow[1] > onerow[2]:
                hsum = hsum + 4
            else:
                if onerow[0]<onerow[1] and onerow[1] < onerow[2]:
                    hsum = hsum + 0
                else:
                    hsum = hsum + 2
        if len(onerow) == 4:
            hsum = hsum + dict1[onerow]
    
    for i in range(4):          #go though columns
        onecol = ""
        for j in range(4):
            char = state[j*4+i]
            if char == '.':
                continue
            pos = dict[char]
            if pos[1] == i:     #final position is this col
                onecol = onecol + str(pos[0])
        if len(onecol) == 2:        #2 chars belong to this col
            if onecol[0] > onecol[1]:
                hsum = hsum + 2
        if len(onecol) == 3:        #3 chars belong to this col
            if onecol[0]>onecol[1] and onecol[1] > onecol[2]:
                hsum = hsum + 4
            else:
                if onecol[0]<onecol[1] and onecol[1] < onecol[2]:
                    hsum = hsum + 0
                else:
                    hsum = hsum + 2
        if len(onecol) == 4:
            hsum = hsum + dict1[onecol]

    #print_puzzle(4, state)
    # print("hsum=", hsum)
    # print()
    return hsum

start1 = perf_counter()

for index, elem in enumerate(line_list):
    start = perf_counter()
    # print_puzzle(4, elem)
    # if(solvable(4, elem)):
    result = AstarSearch(4, elem)
    init_state = taxiCab(4, elem) + getLinearConflict(elem)
    end = perf_counter()
    print("Line", index, ":", elem, ",", result[2], "moves found in", end-start, "seconds", "estimate: ", init_state)
    # else:
    #     end = perf_counter()
    #     print("Line", index, ":", elem, ", no solution determined in", end-start, "seconds")
    print()
    

end1 = perf_counter()
print("Total time:", end1-start1)