import sys
import math

state = "........."

def goaltest(state):
    if state[0] == state[1] and state[1] == state[2] and state[0] != '.':
        return True
    if state[3] == state[4] and state[4] == state[5] and state[3] != '.':
        return True
    if state[6] == state[7] and state[7] == state[8] and state[6] != '.':
        return True
    if state[0] == state[3] and state[3] == state[6] and state[0] != '.':
        return True
    if state[1] == state[4] and state[4] == state[7] and state[1] != '.':
        return True
    if state[2] == state[5] and state[5] == state[8] and state[2] != '.':
        return True
    if state[0] == state[4] and state[4] == state[8] and state[0] != '.':
        return True
    if state[2] == state[4] and state[4] == state[6] and state[2] != '.':
        return True
    if "." not in state:
        return 0
    return None
    # if "." in state:
    #     return None
    # else:
    #     for row in range(3): #rows
    #         ind = row*3
    #         if state[ind] != ".":
    #             if state[ind] == state[ind+1] and state[ind+1] == state[ind+2]:
    #                 if state[ind] == 'X':
    #                     return 1
    #                 if state[ind] == 'O':
    #                     return -1
                
    #     for col in range(3): #cols
    #         ind = col*3
    #         if state[col] != ".":
    #             if state[col] == state[col+3] and state[col+3] == state[col+6]:
    #                 if state[col] == 'X':
    #                     return 1
    #                 if state[col] == 'O':
    #                     return -1
                
    #     if state[4] != ".": #diagonals
    #         if state[0] == state[4] and state[4] == state[8]:
    #             if state[0] == 'X':
    #                 return 1
    #             if state[0] == 'O':
    #                 return -1
    #         if state[2] == state[4] and state[4] == state[6]:
    #             if state[2] == 'X':
    #                 return 1
    #             if state[2] == 'O':
    #                 return -1    
    #     return 0
            
boardcount = []

def min_step(state):
    if goaltest(state) != None:
        boardcount.append(state)
    else:
        for i in range(0, len(state)):
            if state[i] == ".":
                max_step(state[:i] + "X" + state[i+1:])
    
def max_step(state):
    if goaltest(state) != None:
        boardcount.append(state)
    else:
        for i in range(0, len(state)):
            if state[i] == ".":
                min_step(state[:i] + "O" + state[i+1:])
        
min_step(state)        
boardcountf = set(boardcount)
print("Number of games: ", len(boardcount), "Number of final boards = ", len(boardcountf))
