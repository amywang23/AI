import sys
resultText = ["loss","tie","win"]
ai = "X"
player = "O"
players = ["X","O"]

arg = sys.argv[1]

def print_board(state):
    print(state[0:3], "   012")
    print(state[3:6], "   345")
    print(state[6:9], "   678")
    print()

def winner(state):
    if state[0] != "." and state[0] == state[1] and state[1] == state[2]: 
        return state[0]
    if state[3] != "." and state[3] == state[4] and state[4] == state[5]: 
        return state[3]
    if state[6] != "." and state[6] == state[7] and state[7] == state[8]: 
        return state[6]
    if state[0] != "." and state[0] == state[3] and state[3] == state[6]: 
        return state[0]
    if state[1] != "." and state[1] == state[4] and state[4] == state[7]: 
        return state[1]
    if state[2] != "." and state[2] == state[5] and state[5] == state[8]: 
        return state[2]
    if state[0] != "." and state[0] == state[4] and state[4] == state[8]: 
        return state[0]
    if state[2] != "." and state[2] == state[4] and state[4] == state[6]: 
        return state[2]
    return None
    
def goal_test(state):
    if (winner(state) != None):
        return True
    if '.' not in state:
        return True
    return False

def getEmptySpaces(state):
    spaces = ""
    for i in range(9):
        if (state[i] == "."):
            spaces = spaces + str(i)
    if (len(spaces) > 0):
        return ",".join(spaces)
    else:
        return spaces

def getCurrentPlayer(state):
    xcount = state.count("X")
    ocount = state.count("O")
    if (xcount == ocount):
        return 0
    else:
        return 1

def possible_next_boards(state, current_player):
    results = []
    for i in range(9):
        if (state[i] == "."):
            results.append(state[:i] + players[current_player] + state[i+1:])
    return results

def max_step(state):
    global ai
    global player
    score = 0
    winning_player = winner(state)
    if winning_player == ai:
        score = 1
    if winning_player == player:
        score = -1
    if goal_test(state):
        return score
    results = list()
    current_player = getCurrentPlayer(state)
    for next_board in possible_next_boards(state, current_player):
        results.append(min_step(next_board))
    return max(results)

def min_step(state):
    global ai
    global player
    score = 0
    winning_player = winner(state)
    if winning_player == ai:
        score = 1
    if winning_player == player:
        score = -1
    if goal_test(state):
        return score
    results = list()
    current_player = getCurrentPlayer(state)
    for next_board in possible_next_boards(state, current_player):
        results.append(max_step(next_board))
    return min(results)

def play():
    global ai
    global player
    if arg != ".........":
        temp = getCurrentPlayer(arg)
        if temp == 1:
            order = "O"
        else:
            order = "X"
    else:
        order = input("Should I be X or O?  ")
    print()
    board = arg
    if (order == "X" or order == "x"):      #AI goes first
        ai = "X"
        player = "O"
    else:                   #Player goes first
        ai = "O"
        player = "X"
    current_player = getCurrentPlayer(board)
    while (goal_test(board) == False):
        print("Current board: player")
        print_board(board)
        if (players[current_player] == ai):       #AI moves
            results = [-2]*9
            for i in range(9):
                if (board[i] == "."):
                    newboard = board[:i] + players[current_player] + board[i+1:]
                    result = min_step(newboard)
                    print("Moving at", i, "results in a", resultText[result+1], ".")
                    results[i] =result
            max_value = max(results)
            index = results.index(max_value)
            print()
            print("I choose space", index)
            print()
            board = board[:index] + players[current_player] + board[index+1:]
            print("Current board:")
            print_board(board)
            if(winner(board) == ai):
                print()
                print("I win!")
                break
            if not "." in board:
                print()
                print("We tied!")
                break
        else:         #player moves
            print("You can move to any of these spaces:", getEmptySpaces(board) )
            playermove = input("Your choice?     ")
            print()
            playerindex = int(playermove)
            board = board[:playerindex] + players[current_player] + board[playerindex+1:]
            if(winner(board) == player):
                print()
                print("You win!")
                break
            if not "." in board:
                print()
                print("We tied!")
                break
        current_player = (current_player+1) % 2
    return

play()