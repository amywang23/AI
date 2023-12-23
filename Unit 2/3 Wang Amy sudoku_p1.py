import math
import sys
from time import perf_counter

start = perf_counter()

allsymbols = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
N = 0
subblock_height = 0
subblock_width = 0
symbol_set = ''

constraints = []     #stores by indices
neighbors = []      #stores by indices

f = sys.argv[1]

with open(f) as f:
    line_list = [line.strip() for line in f]
    
def print_board(line):
    board = newBoard(line)
    for i in range(len(board)):
        if i % subblock_height == 0 and i != 0:
            print(''.join(['-- ']*len(board[0])))

        for j in range(len(board[0])):
            if j % subblock_width == 0 and j != 0:
                print(" | ", end="")

            if j == len(board[0])-1:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

def goal_test(state):
    if ('.' in state):
        return False

    for i in range(N*N):
        for j in neighbors[i]:
            if (i != j) and (state[i]==state[j]):   
                return False
    return True

def get_next_unassigned_var(state):
    for i in range(N*N):
        if state[i] == '.':
            return i  
    return None

def get_sorted_values(state, var):
    res = []
    for value in symbol_set:
        if location_ok(state, var, value):
            newstate = list(state)
            newstate[var] = value
            res.append(newstate)
    return res


def csp_backtracking(state):
    if goal_test(state):
        return state

    row = get_next_unassigned_var(state)        #returns index of next empty spot 
    for val in get_sorted_values(state, row):
        new_state = val
        result = csp_backtracking(new_state)
        if result is not None:
            return result
    return None

def location_ok(state, index, value):
    for j in neighbors[index]:
        if (index != j) and (value==state[j]):   
            return False
    return True


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
            index = i*N+j
            row.append(line[index])
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

# start1 = perf_counter()
for index, line in enumerate(line_list):
    constraints = []
    neighbors = []
    N = int( math.sqrt(len(line)) )
    root = math.sqrt(N)

    if int(root + 0.5) ** 2 == N:       #check if root is int (root is int)
        subblock_height = int(root)
        subblock_width = int(root)
    else:           #root isnt int
        sizepair = findSubblock(N)
        subblock_height = sizepair[1]
        subblock_width = sizepair[0]
        
    symbol_set = allsymbols[0:N]

    constraints = findConstraints()
    # print(constraints)
    neighbors = findNeighbors()
    # print(neighbors)
    
    # start = perf_counter()
    result = csp_backtracking(line)
    str = ""
    #print("result: ", result)
    resultStr = str.join(result)
    # end = perf_counter()
    if result != None:
        # print_board(result)
        print('Line: ', index, ' ', resultStr)
        # res = findInstances(result)
        # print(res)
    else:
        print('Line ', index, ': NO SOLUTION')
    print()
# print("total time:", end - start1)