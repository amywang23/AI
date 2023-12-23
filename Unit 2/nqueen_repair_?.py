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

    for r1 in range(n):
        for r2 in range(n):
            if (r1 != r2) and (state[r1]==state[r2]):   #two queens same column
                return False
            r = r1              #row
            c = state[r1]       #col

            for i, j in zip(range(r-1, -1, -1), range(c-1, -1, -1)):  #checks the upper left diagonal
                if state[i] == j:
                    return False

            for i, j in zip(range(r-1, -1, -1), range(c+1, n, 1)):  #checks the upper right diagonal
                if state[i] == j:
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
    oldt = getAllConflicts(state)
    
    #gets new taxicab after queen moves away from current pos
    #if current pos has 2 queens, need to -1 
    #if current pos has >2, doesnt matter
    if (cols[oldcol] == 2):
        oldt -= 1
    if(leftDiag[row - oldcol + n - 1] == 2):
        oldt -= 1
    if(rightDiag[row + oldcol] == 2):
        oldt -= 1
    for col in range(n):
        if col != oldcol:
            t = oldt

            #if new pos tracking only =1, add one for the queen just moved here
            if (cols[col] == 1):
               t += 1
            if(leftDiag[row - col + n - 1] == 1):
                t += 1
            if(rightDiag[row + col] == 1):
                t += 1
            tlist.append(t)
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
        
        print("State: ", state, ", Taxicab: ", taxicab())

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
    for row in range(len(state)):
        left = state[row]
        middle = state[row]
        right = state[row]
        for compare in range(row + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                print(row, "middle", compare)
                return False
            if left >= 0 and state[compare] == left:
                print(row, "left", compare)
                return False
            if right < len(state) and state[compare] == right:
                print(row, "right", compare)
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
for idx in [31,61]:
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