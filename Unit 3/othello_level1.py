import sys

directions = [-11, -10, -9, -1, 1, 9, 10, 11]

# All your other functions

board = sys.argv[1]
player = sys.argv[2]

depth = 1

def convert_board(board):
    newboard = "??????????"
    for i in range(8):
        newboard += "?"+ board[i*8:i*8+8] + "?"
    newboard += "??????????"
    return newboard

def get_opponent(token):
    if (token == "x"):
       return("o")
    else:
        return("x")

def convert_index(index, num):
    if (num == 0):   #convert from 8*8 to 10*10
        row = int(index / 8)
        newindex = index + 10 + 2*row + 1
    else:               #convert from 10*10 to 8*8
        row = int(index / 10) - 1
        newindex = index - 10 - 2*row - 1
    return newindex

def convert_moves(moves):
    movelist = list(moves)
    for i in range(len(movelist)):
        movelist[i] = convert_index(movelist[i], 1)

    return movelist

def possible_moves(board, token):
    board = convert_board(board)
    opponent = get_opponent(token)
    
    moves = set()
    for i in range(0, len(board)):
        if board[i] == token:
            for dir in directions:
                if board[i+dir] == opponent:
                    isFound = False
                    counter = 2
                    while isFound == False:
                        newindex = i+dir*counter
                        temp = board[newindex]
                        if temp == '?' or temp == '.' or temp == token:
                            isFound = True
                            if temp == ".":
                                moves.add(newindex)
                        counter += 1
    return sorted(convert_moves(moves))

def make_move(board, token, move):
    opponent = get_opponent(token)
    past_board = convert_board(board)
    past_move = convert_index(move, 0)

    for direction in range(8):       #check if neighbor happens to be an opponent
        nidx = directions[direction] + past_move
        if (past_board[nidx]==opponent):
            past_board = play(past_board, token, opponent, past_move, direction)
    return past_board.replace("?","")


#extended board, move is the index for placing token, direction is position of opponent 
def play(board, token, opponent, move, direction):
    newboard = board
    i = move + directions[direction]        #neighbor
    if (board[i] != opponent):              #this neighbor must be opponent
        return board
    flips = []              #indices for the pegs that need to flip
    temp = False
    
    while i>=0 and i <100 and board[i] != "?":
        if (board[i] == opponent):
            flips.append(i)
            i = i + directions[direction]
            continue
        if (board[i] == token):
            temp = True
            break
        if (board[i] == "." or board[i] == "?"):        #border or empty space
            break
    if (temp):
        for j in flips:
            newboard = newboard[:j] + token + newboard[j+1:]
        newboard = newboard[:move] + token + newboard[move+1:]
    return newboard

def nicely_print(board):
    board_rows = [board[x:x + 8] for x in range(0, 64, 8)]
    for row in board_rows:
        print(" ".join(list(row)))

def dual_print(board, other):
    board_rows = [board[x:x + 8] for x in range(0, 64, 8)]
    other_rows = [other[x:x + 8] for x in range(0, 64, 8)]
    for count in range(8):
        print(" ".join(list(board_rows[count])) + "      " + " ".join(list(other_rows[count])))

def find_next_move(board, player, depth):
   # Based on whether player is x or o, start an appropriate version of minimax
    token = player
    best_move = 0
    opponent = get_opponent(token)
    for move in possible_moves(board, opponent, depth):
        return 0
    return best_move    #return move with the best "score"
   # that is depth-limited to "depth".  Return the best available move.
   
def min_max(board, opponent, depth):
    scores = set()
    if depth == 0 or game_over:
        scores.add(score(board))
    if possible_moves(board, opponent, depth+1) != None:
        return min_max(board, opponent, depth-1)
    scores = sorted(scores)
    return scores[len(scores)-1]      #return the best "score"

def game_over():
    opponent = get_opponent(player)
    if possible_moves(board, player) == 0 and possible_moves(board, opponent) == 0:
        return True

def score(board):
    score = 0
    opponent = get_opponent(player)
    me = player
    if board[0] == me:
        score += 100
    if board[7] == me:
        score += 100
    if board[55] == me:
        score += 100
    if board[63] == me:
        score += 100
    if board[0] == opponent:
        score -= 100
    if board[7] == opponent:
        score -= 100
    if board[55] == opponent:
        score -= 100
    if board[63] == opponent:
        score -= 100
    
    if board.count(player) > board.count(opponent):
        score += 1000
    if board.count(opponent) > board.count(player):
        score -= 1000
    return score
    
    
for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
   print(find_next_move(board, player, depth))
   depth += 1