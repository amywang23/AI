import random
from time import perf_counter

start = perf_counter()

n = 1
leftDiag = [0] * 80 #keeps track of the queens in the left to right diagonal
rightDiag = [0] * 80 #keeps track of the queens in the right to left diagonal

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

def location_ok(state, r, c):
    if c in state:  #column number already in the state
        return False

    if leftDiag[r - c + n - 1] != 0:
        return False
        
    if rightDiag[r + c] != 0:
        return False

    return True

def get_next_unassigned_var(state):
    candidates = []
    for row in range(n):
        if (state[row]== None):  #finds empty row
            candidates.append(row)
    if len(candidates) > 2:         #picks the center of them all
        center = int (len(candidates)/2)
        return candidates[center]
    if len(candidates) > 0: 
        return candidates[0]

    return None

def get_sorted_values(state, row):
    result = []
    for col in range(n):
        if col not in state and location_ok(state, row, col):
            newstate = list(state)
            newstate[row] = col
            result.append(newstate)
    random.shuffle(result)  #returns the results in a random order
    return result


def csp_backtracking(state):
    if goal_test(state):
        return state

    row = get_next_unassigned_var(state)
    for val in get_sorted_values(state, row):
        new_state = val
        col = val[row]
        leftDiag[row - col + n - 1] = 1
        rightDiag[row + col] = 1
        result = csp_backtracking(new_state)
        if result is not None:
            return result
        leftDiag[row - col + n - 1] = 0
        rightDiag[row + col] = 0
    return None

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

start1 = perf_counter()
blank = None
for index in [31,41]:
    start = perf_counter()
    state = [blank] * index
    n = index
    leftDiag = [0] * 80
    rightDiag = [0] * 80
    result = csp_backtracking(state)
    end = perf_counter()
    print("NQueen", index, "solution : ", result, ", in ", end-start, "seconds     tested = ", test_solution(result))
    print()
  
end = perf_counter()
print('Total time:', end - start1)