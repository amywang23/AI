from re import search
import sys
from collections import deque

startState = ".xxxxxxxxxxxxxx"

#posible moves, index 0 is the very top of the board -> jump over peg 1, land on peg 3
moves = { 0: [(1,3), (2,5)],
         1: [(3,6), (4,8)],
         2: [(4,7), (5,9)],
         3: [(1,0), (4,5), (6, 10), (7,12)],
         4: [(7,11), (8,13)],
         5: [(2,0), (4,3), (8, 12), (9, 14)],
         6: [(3,1), (7,8)],
         7: [(4,2), (8,9)],
         8: [(4,1), (7,6)],
         9: [(8,7), (5,2)],
         10: [(11,12)],
         11: [(7,4), (12,13)],
         12: [(7,3), (8,5), (11, 10), (13, 14)],
         13: [(8,4), (12,11)],
         14: [(9,5), (13,12)]
        }

def printBoard(str):
    pegs = [*str]
    print("        %s" % pegs[0])
    print("       %s %s" % (pegs[1], pegs[2]))
    print("      %s %s %s" % (pegs[3], pegs[4], pegs[5]))  
    print("     %s %s %s %s" % (pegs[6], pegs[7], pegs[8], pegs[9]))
    print("    %s %s %s %s %s" % (pegs[10], pegs[11], pegs[12], pegs[13], pegs[14]))
    
def findGoal(line):
    goalGrid = ''.join(sorted(line))
    goal = goalGrid.replace('.', '')               
    return(goal + ".")

def getChildren(boardState):
    result = []
    for elem in range(0, 15):
        if pegCheck(boardState, elem):
            jumps = moves[elem]
            for over, land in jumps:
                if pegCheck(boardState, over) and not pegCheck(boardState, land):
                    # print("Landing is:", land)
                    # print("Jumping oevr:", over)
                    child = switch(boardState, elem, land)
                    # print(child)
                    child = removePeg(child, over)
                    # print(child)
                    result.append(child)
    return result

def checkGoal(state):
    return state == 'x..............'

def switch(state, over, land):
    if over < land:
        start = over
        end = land
    else:
        start = land
        end = over
    s1 = state[:start]
    s2 = state[start + 1: end]
    s3 = state[end + 1:]
    # print("s1: " + s1, " /// s2: " + s2, "/// s3: " + s3)
    final = s1 + state[end] + s2 + state[start] + s3
    return (final)

#Both BFS and DFS searches are in this method!
def bfsDfs(state, searchType):
    fringe = deque()
    visited = set()
    path = [state]
    level = 0
    
    print(searchType)
    
    fringe.append((level, state, path))
    visited.add(state)
    
    while len(fringe) > 0:
        if searchType == 'DFS':
            v = fringe.pop()
        else:
            v = fringe.popleft()
        if checkGoal(v[1]):
            return v[2]
        children = getChildren(v[1])
        
        
        for child in children:
            if child not in visited:
                #move+1
                newpath = []
                for item in v[2]: newpath.append(item)
                newpath.append(child)
                fringe.append((v[0]+1, child, newpath))
                visited.add(child)
                
    return None

def pegCheck(state, index):
    peg = state[index:index+1]
    return peg != '.'

def removePeg(state, index):
    state = state[:index] + '.' + state[index+1:]
    return state

# printBoard(startState)
# print(getChildren(startState))
result = bfsDfs(startState, "BFS")
for elem in result:
    printBoard(elem)
    
result2 = bfsDfs(startState, "DFS")
for elem in result2:
    printBoard(elem)