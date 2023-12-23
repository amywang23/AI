import heapq
import sys
from collections import deque
from time import perf_counter

f = sys.argv[1]

with open(f) as f:
    line_list = [line.strip() for line in f]
    

def get_children(dimen, board, cube):
    dot = cube[1]
    final = []
    #move left
    if dot%dimen > 0:
        final.append(switch(board, cube[0], dot - 1, 5))
    #move right
    if dot%dimen < dimen - 1:
        final.append(switch(board, cube[0], dot + 1, 4))
    #move up
    if dot//dimen > 0:
        final.append(switch(board, cube[0], dot - dimen, 1))
    #move down
    if dot//dimen < dimen - 1:
        final.append(switch(board, cube[0], dot + dimen, 0))
    return final

def checkgoal(cube_state): 
    return cube_state == '@@@@@@'

#i1 < i2
def switch(board, cube_state, board_i, direction):
    face = cube_state[direction]
    s1 = board[:board_i]
    s2 = board[board_i + 1:]
    newboard = s1 + face + s2
    
    #cube 'xxxxxx' = 'front, back, up, down, right, left'
    s1 = cube_state[:direction]
    s2 = cube_state[direction + 1:]
    newcube_state = s1 + str(board[board_i]) + s2
    
    if direction ==0:
        newcube_state = rollDown(newcube_state)
    if direction ==1:
        newcube_state = rollUp(newcube_state)
    if direction ==4:
        newcube_state = rollRight(newcube_state)
    if direction ==5:
        newcube_state = rollLeft(newcube_state)
    
    newcube = (newcube_state, board_i)
    return (newboard, newcube)

def rollRight(cube):
    l = list(cube)
    temp = l[2]
    l[2] = l[5]
    l[5] = l[3]
    l[3] = l[4]
    l[4] = temp
    return ''.join(l)
    
def rollLeft(cube):
    l = list(cube)
    temp = l[2]
    l[2] = l[4]
    l[4] = l[3]
    l[3] = l[5]
    l[5] = temp
    return ''.join(l)

def rollUp(cube):
    l = list(cube)
    temp = l[2]
    l[2] = l[0]
    l[0] = l[3]
    l[3] = l[1]
    l[1] = temp
    return ''.join(l)
    
def rollDown(cube):
    l = list(cube)
    temp = l[2]
    l[2] = l[1]
    l[1] = l[3]
    l[3] = l[0]
    l[0] = temp
    return ''.join(l)

def AstarSearch(dimen, board, cube):
    closed = set()
    f = taxiCab(cube[0])
    path = []
    path.append(board + " " + str(cube[1]) + " " + cube[0])
    
    fringe = []
    heapq.heapify(fringe)
    heapq.heappush(fringe, (f, board, cube, path, 0))
    
    while len(fringe) != 0:
        v = heapq.heappop(fringe)
        if checkgoal(v[2][0]):
            return v
        current1 = v[1] + " " + str(v[2][1]) + " " + v[2][0]
        if current1 not in closed:
            closed.add(current1)
            children = get_children(dimen, v[1], v[2])
            for child in children:
                current2 = child[0] + " " + str(child[1][1]) + " " + child[1][0]
                if current2 not in closed:
                    f = taxiCab(child[1][0]) + v[4] +1
                    newpath = []
                    for item in v[3]: newpath.append(item)
                    newpath.append(current2)
                    heapq.heappush(fringe, (f, child[0], child[1], newpath, v[4]+1))
    return None

def taxiCab(cube_state):
    amount = cube_state.count('@')
    return 6-amount

start = perf_counter()

for index, elem in enumerate(line_list):
    elemlist = elem.split(" ")
    
    dimen = int(elemlist[0])
    state = elemlist[1]
    cube_pos = int(elemlist[2])
    cube = ('......', cube_pos)

    result = AstarSearch(dimen, state, cube) #returns f, board, cube, path, 0
    if result != None:
        print("Line", index, ":", elemlist[1], ", Path: ", result[3], ", ", result[4], "moves found in")
    else:
        print("Line", index, ":", elemlist[1], ", no solution determined in")
    print()
    
end = perf_counter()
print("Total time:", end-start)