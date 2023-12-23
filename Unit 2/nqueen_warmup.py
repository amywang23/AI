from time import perf_counter

start = perf_counter()

#print the board in a matrix like a chess board
def printboard(state):
    n = len(state)
    for i in range(n):
        rowstr = []
        for j in range(n):
            if (j!=state[i]):
                rowstr.append(".")
            else:
                rowstr.append("x")
        print(' '.join(rowstr))

#have we reached the goal?
def goal_test(state):
    if (-10000000 in state):
        #print('not solved')
        return False
    n = len(state)
    for k1 in range(n):
        for k2 in range(n):
            if (k1 != k2) and (state[k1]==state[k2]):   #two queens same column
                return False
            r = k1              #row
            c = state[k1]       #col

            for i, j in zip(range(r-1, -1, -1), range(c-1, -1, -1)):  #check upper left diagonal for queens
                if state[i] == j:
                    return False

            for i, j in zip(range(r-1, -1, -1), range(c+1, n, 1)):  #check upper right diagonal for queens
                if state[i] == j:
                    return False

    return True

#can you put the queen in this place?
def ok(state, r, c):
    n = len(state)
    for k in range(n):
        if (k != r) and (state[k]==c):   #two queens same column
            return False
    
    for i, j in zip(range(r-1, -1, -1), range(c-1, -1, -1)):
         if state[i] == j:
            return False

    for i, j in zip(range(r-1, -1, -1), range(c+1, n, 1)):
        if state[i] == j:
            return False

    return True

#whats the next row i can try
def get_next_unassigned_var(state):
    n = len(state)
    for row in range(n):
        if (state[row]==-10000000):  #empty row
            return row
    return -100000000

#sort all the possible choices
def get_sorted_values(state, var):
    res = []
    n = len(state)
    for col in range(n):
        if col not in state and ok(state, var, col):
            newstate = list(state)
            newstate[var] = col
            res.append(newstate)
    return res

#backtracking to find the end state
def csp_backtracking(state):
    size = len(state)

    if goal_test(state):
        return state

    var = get_next_unassigned_var(state)
    for val in get_sorted_values(state, var):
        #print("val", val)
        new_state = val
        result = csp_backtracking(new_state)
        if result is not None:
            return result
    return None

#is the current state ok
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


#print(goal_test([0, 4, 7, 5, 2, 6, 1, 3]))
#printboard([0, 4, 7, 5, 2, 6, 1, 3])
#print(goal_test([0, 4, 7, 5, 2, 6, 1, 3]))
start1 = perf_counter()
blank = -10000000
for idx in range(8,11,1):
    start = perf_counter()
    state = []
    for i in range(idx):
        state.append(blank)
    result = csp_backtracking(state)
    end = perf_counter()
    print("NQueen {} solution : {}, in {} seconds tested={}".format(idx, result, end-start, test_solution(result) ))
    print()
  
end = perf_counter()
print('Total time:', end - start1)