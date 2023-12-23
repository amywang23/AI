import math
import sys
from collections import defaultdict

allsymbols = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
N = 0
subblock_height = 0
subblock_width = 0
symbol_set = ''

constraints = []            #stores by indices
neighbors = []             #stores by indices
solved = []              #list of indices that are already solved
possiblevalues = []         #list of strings with possible symbols in the indices

f = sys.argv[1]

with open(f) as f:
    line_list = [line.strip() for line in f]

# def print_possibility():
#     space = ' '*(N+1)
#     divider = '-'*(N+2)
   
#     for i in range(N):
#         if i % subblock_height == 0 and i != 0:
#             print(''.join(divider*N))
#         for j in range(N):
#             if j % subblock_width == 0 and j != 0:
#                 print(" | ", end="")
#             idx = i*N+j
#             cell = possiblevalues[idx]+space
#             cell = cell[:N]
#             if j == N-1:
#                 print(cell)
#             else:
#                 print(cell + " ", end="")
#     print()

# def print_board(line):
#     board = newBoard(line)
#     for i in range(len(board)):
#         if i % subblock_height == 0 and i != 0:
#             print(''.join(['-- ']*len(board[0])))
#         for j in range(len(board[0])):
#             if j % subblock_width == 0 and j != 0:
#                 print(" | ", end="")
#             if j == len(board[0])-1:
#                 print(board[i][j])
#             else:
#                 print(str(board[i][j]) + " ", end="")
#     print()

def goal_test(state):
    if ('.' in state):
        return False

    for i in range(N*N):
        for j in neighbors[i]:
            if (i != j) and (state[i]==state[j]):   
                return False
    return True

def get_most_constrained_var(state):
    minv = N
    minidx = -1
    #print("possible: ", possiblevalues)
    allempty = [i for i, x in enumerate(state) if x == '.']
    for i in allempty:
        if len(possiblevalues[i]) > 1:
            if len(possiblevalues[i]) < minv:
                minv = len(possiblevalues[i])
                minidx = i
    return minidx

#sort the possiblevalues into the state inputted
def get_sorted_values(state, idx):
    res = []
    for value in possiblevalues[idx]:
        if location_ok(state, idx, value):
            newstate = state[:idx] + value + state[idx+1:]
            res.append(newstate)
    return res


def csp_backtracking_with_forward_looking(state):
    global solved
    global possiblevalues

    if goal_test(state):
        return state

    idx = get_most_constrained_var(state)
    if idx < 0:
        return None

    oldpossible = list(possiblevalues)
    
    for val in get_sorted_values(state, idx):
        solved = findSolved(val)
        possiblevalues[idx] = val[idx]
        checked_board = val
        for i in range(5):      #do a few loops
            checked_board = forward_looking(checked_board)
            if checked_board == None:
                break
            if goal_test(checked_board):
                return checked_board
           
            checked_board = constraint_propagation(checked_board)
            if checked_board == None:
                break
            if goal_test(checked_board):
                return checked_board

            if len(solved) == 0:        #no new solved after constraint propagation
                break
        if checked_board is not None:
            result = csp_backtracking_with_forward_looking(checked_board)
            if result is not None:
                return result
        possiblevalues = oldpossible.copy()
    return None


def location_ok(state, idx, value):
    for j in neighbors[idx]:
        if (idx != j) and (value==state[j]):   
            return False
    return True

def solveboard(state):
    global solved
    
    for i in range(20):
        state = forward_looking(state)
        if state == None:
            return None
        if goal_test(state):
            return state
        state = constraint_propagation(state)
        if state == None:
            return None
        if goal_test(state):
            return state
        if len(solved) == 0:        #no new solved after constraint propagation
            break
    state = csp_backtracking_with_forward_looking(state)
    return state


def constraint_propagation(state):
    global solved
    newresolved = []
    for ct in constraints:      #loop through all constraints
        dict = defaultdict(list)
        for i in ct:            #loop through all indexes in one constraint
            for c in [*possiblevalues[i]]:  #all chars in possible values
                dict[c].append(i)              #append index to the symbol
        for s in symbol_set:
            if not s in dict.keys():
                return None
            if s in dict.keys() and len(dict[s])==1:    #only on index
                idx = dict[s][0]
                if (state[idx]=="."):           #empty space
                    state = state[:idx] + s + state[idx+1:]
                    newresolved.append(idx)
                    possiblevalues[idx] = s
    solved = newresolved
    return state

def forward_looking(state):
    global solved

    count = 0
    while count < len(solved):
        i = solved[count]
        for j in neighbors[i]:
            if (i != j) and (state[i] in possiblevalues[j]):
                possiblevalues[j] = possiblevalues[j].replace(state[i],'')
                if (len(possiblevalues[j])==0):     #no solution
                    return None
                if (len(possiblevalues[j])==1 and state[j]=='.'):     #solved
                     solved.append(j)
                     state = state[:j] + possiblevalues[j] + state[j+1:]
        count += 1
    return state

def findSolved(state):
    global solved
    solved = []
    for i in range(N*N):
        if state[i] != '.':
            solved.append(i)
    return solved

def findPossible(state):
    possiblevalues = []
    for i in range(N*N):
        if state[i] != '.':
            possiblevalues.append(state[i])
            solved.append(i)
        else:
            possiblevalues.append(symbol_set)
    return possiblevalues

def findNeighbors():
    neighbors = []
    for i in range(N*N):
        nei = set()
        for st in constraints:
            if i in st:
                nei.update(st)
        nei.remove(i)
        neighbors.append(nei)
    return neighbors

def findConstraints():
    constraints = []
    
    for i in range(N):
        row = set()
        for j in range(N):
            row.add(i*N+j)
        constraints.append(row)
   
    for j in range(N):
        col = set()
        for i in range(N):
            col.add(i*N+j)
        constraints.append(col)

    #find block constraints
    for i in range(subblock_width):    #number of blocks from top to bottom
        for j in range(subblock_height): #number of blocks from left to right
            block = set()
            starty = j*subblock_width
            startx = i*subblock_height
            for k in range(subblock_height):
                for l in range(subblock_width):
                    block.add(startx*N+k*N + starty+l)
            constraints.append(block)
    return constraints

def newBoard(line):
    board = []
    for i in range(N):
        row = []
        for j in range(N):
            idx = i*N+j
            row.append(line[idx])
        board.append(row)
    return board

def findFactors(num):
    factors = []
    for i in range(1, num + 1):
       if num % i == 0:
           factors.append(i)
    return factors

def findSubblock(size):
    width = 0
    height = 0

    root = math.sqrt(N)
    factors = findFactors(size)

    prev = 1
    for i in factors:
        if prev < root and i > root:
            width = i
            height = prev
            break
        prev = i
    return (width, height)

def findInstances(state):
    res = []
    for s in symbol_set:
        c = state.count(s)
        res.append(c)
    return res

for index, line in enumerate(line_list):
    constraints = []
    neighbors = []
    solved = []
    checked = []
    possiblevalues = []
    N = int(math.sqrt(len(line)))
    root = math.sqrt(N)

    if int(root + 0.5) ** 2 == N:       #check if root is int (root is int)
        subblock_height = int(root)
        subblock_width = int(root)
    else:       #root isnt int
        sizepair = findSubblock(N)
        subblock_height = sizepair[1]
        subblock_width = sizepair[0]

    subblock_size = subblock_height*subblock_width
    symbol_set = allsymbols[0:subblock_size]
    constraints = findConstraints()
    neighbors = findNeighbors()
    possiblevalues = findPossible(line)
    
    result = solveboard(line)
    if result != None:
        # print_board(result)
        print('Line: ', index, ' ', result)
    else:
        print('Line ', index, ': NO SOLUTION')
    print()