import random
from time import perf_counter

start = perf_counter()

n = 1
leftDiag = [0] * 180
rightDiag = [0] * 180
cols  = [0] * 80
queenConflicts = [0] * 80

def printboard(state):
    for i in range(n):
        rowstr = []
        for j in range(n):
            if (j!=state[i]):
                rowstr.append(".")
            else:
                rowstr.append("x")
        print(' '.join(rowstr))

def goal_test(state):
    if (None in state):
        return False

    for k1 in range(n):
        for k2 in range(n):
            if (k1 != k2) and (state[k1]==state[k2]):   #two queens same column
                #print("goal_test two on same column")
                return False
            r = k1              #row
            c = state[k1]       #col

            for i, j in zip(range(r-1, -1, -1), range(c-1, -1, -1)):
                if state[i] == j:
                    #print("goal_test upper left diag conflict")
                    return False

            for i, j in zip(range(r-1, -1, -1), range(c+1, n, 1)):
                if state[i] == j:
                    #print("goal_test upper right diag conflict")
                    return False

    return True

def getAllConflicts(state):
    queenConflicts = [0] * 80
    for row in range(n):
        col = state[row]
        if(leftDiag[row - col + n - 1] > 1):
            queenConflicts[row] += 1    

        if(rightDiag[row + col] > 1):
            queenConflicts[row] += 1
        if(cols[col] > 1):
            queenConflicts[row] += 1
    
    return queenConflicts

def findNextQueen(state):
    queenConflicts = getAllConflicts(state)
    #printboard(state)
    max_value = max(queenConflicts)
    maxlist = []
    for i in range(n):
        if queenConflicts[i]==max_value:
            maxlist.append(i)

    r = random.choice(maxlist)
    return r


def getNextMove(state, row):
    minlist = []   #list with all col with min val
    tlist = []    #list with taxicab val for all col
    oldcol = state[row]
    oldt = taxicab()
    for col in range(n):
        if col != oldcol:
            h = oldt
            if (cols[col]>0):
               h += 1
            if(leftDiag[row - col + n - 1] > 0):
                h += 1
            if(rightDiag[row + col] > 0):
                h += 1
            tlist.append(h)
        else:
            tlist.append(1000000)
    min_value = min(tlist)
    for i in range(n):
        if tlist[i]==min_value:
            minlist.append(i)   
    r = random.choice(minlist)
   
    state[row] = r
    return state


def repair(state):

    count = 0
    col = 0
    while count < 100000:
        count += 1

        if goal_test(state):
            return state

        row = findNextQueen(state)
        col = state[row]
        
        #queen moved away so updating the tracking at the old col
        leftDiag[row - col + n - 1] -= 1
        rightDiag[row + col] -= 1
        cols[col] -= 1

        state = getNextMove(state, row)
        
        #queen moved here so updating the tracking at the new col
        col = state[row]
        leftDiag[row - col + n - 1] += 1
        rightDiag[row + col] += 1
        cols[col] += 1

    return None

def taxicab():
    collist = [i for i in cols if i > 1]
    colConflicts = len(collist)
    leftDlist = [i for i in leftDiag if i > 1]
    leftDConflicts = len(leftDlist)
    rightDlist = [i for i in rightDiag if i > 1]
    rightDConflicts = len(rightDlist)
    return colConflicts+leftDConflicts+rightDConflicts

def test_solution(state):
    for var in range(len(state)):
        left = state[var]
        middle = state[var]
        right = state[var]
        for compare in range(var + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                print(var, "middle", compare)
                return False
            if left >= 0 and state[compare] == left:
                print(var, "left", compare)
                return False
            if right < len(state) and state[compare] == right:
                print(var, "right", compare)
                return False
    return True 

# def newBoardRandom():     #Random isn't good
#     board = []
#     for i in range(n):
#         col = random.randrange(0, n-1, 1)
#         board.append(col)
#         leftDiag[i - col + n - 1] += 1
#         rightDiag[i + col] += 1
#         cols[col] += 1
#     return board

def newBoard():
    board = []

    col = 0
    center = int(n/2)
    if (n % 2 == 0):   #for an even number board size
        for i in range(n):
            if i < center:
                col = i*2
            else:
                col = (i*2+1)%n
            board.append(col)
            leftDiag[i - col + n - 1] += 1
            rightDiag[i + col] += 1
            cols[col] += 1
    else:    #for an odd number board size
        for i in range(n-1):
            if i <= center:
                col = i*2
            else:
                col = (i*2+2)%n
            board.append(col)
            leftDiag[i - col + n - 1] += 1
            rightDiag[i + col] += 1
            cols[col] += 1

        board.append(1)    #last queen goes to col 1 since it wont fit
        leftDiag[n - 1 - 1 + n - 1] += 1
        rightDiag[n - 1 + 1] += 1
        cols[1] += 1

    return board


start1 = perf_counter()
blank = None
for idx in range(31,39,1):
    start = perf_counter()
    
    n = idx
    leftDiag = [0] * 180
    rightDiag = [0] * 180
    cols = [0] * 80
    queenConflicts = [0] * 80

    state = newBoard()
    
    result = repair(state)
    end = perf_counter()
    print("NQueen", idx, "solution : ", result, ", in ", end-start, "seconds     tested = ", test_solution(result))
    print()
  
end = perf_counter()
print('Total time:', end - start1)