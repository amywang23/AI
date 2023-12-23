import sys

infinity = 1000000
directions = [-11, -10, -9, -1, 1, 9, 10, 11]
adjacents = [1, 6, 8, 9, 48, 49, 57]
edges = edges=[1,8,9,6,14,15,48,49,57,54,55,62]

# All your other functions

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

def nicely_print(board):
    board_rows = [board[x:x + 8] for x in range(0, 64, 8)]
    for row in board_rows:
        print(" ".join(list(row)))

def find_next_move(board, player, depth):
   # Based on whether player is x or o, start an appropriate version of minimax
    if player == "x":
        return max_move(board,depth)
   # that is depth-limited to "depth".  Return the best available move.
    else:
        return min_move(board,depth)


# All your other functions

def max_move(board, depth):
    possible = possible_moves(board,"x")
    temp = possible[0]
    maxval = min_step(make_move(board,"x",temp), depth, -1 * infinity, infinity)
    for ind in possible:
        result = min_step(make_move(board,"x",ind), depth, -1 * infinity, infinity)
        if result > maxval:
            maxval = result
            temp = ind
    return temp

def min_move(board, depth):
    possible = possible_moves(board,"o")
    temp =possible[0]
    minval = max_step(make_move(board,"o",temp), depth, -1 * infinity, infinity)
    for ind in possible:
        result = max_step(make_move(board,"o",ind), depth, -1 * infinity, infinity)
        if result < minval:
            minval = result
            temp = ind
    return temp
        

def max_step(board, depth, alpha, beta):
    if depth == 0 or game_over(board, "x"):
        return score(board)
    results = list()
    for next_board in possible_moves(board, "x"):
        r = min_step(make_move(board,"x",next_board), depth-1, alpha, beta)
        #alphabeta pruning here
        if r > alpha:
            alpha = r
        results.append(r)
    if len(results) == 0:
        return score(board)
    if max(results)<alpha:
        return max(results)
    return alpha

def min_step(board, depth, alpha, beta):
    if depth == 0 or game_over(board, "o"):
        return score(board)
    results = list()
    for next_board in possible_moves(board, "o"):
        r = max_step(make_move(board,"o",next_board), depth-1, alpha, beta)
        #alphabeta pruning here
        if r > beta:
            beta = r
        results.append(r)
    if len(results) == 0:
        return score(board)
    if max(results)<beta:
        return max(results)
    return beta

def game_over(board, player):
    opponent = get_opponent(player)
    if len(possible_moves(board, player)) == 0 and len(possible_moves(board, opponent)) == 0:
        return True

def score(board):
    xcount = board.count("x")
    ocount = board.count("o")
    xmobile = len(possible_moves(board, "x"))
    omobile = len(possible_moves(board, "o"))
    pmovesdiff = xmobile - omobile
    # if (game_over(board, player)):
    #     diff = xcount - ocount
    #     if diff < 0:
    #         return -infinity
    #     else:
    #         return infinity
    score = 0
    if board[0] == "x":
        score += 150
    if board[7] == "x":
        score += 150
    if board[56] == "x":
        score += 150
    if board[63] == "x":
        score += 150
    if board[0] == "o":
        score -= 150
    if board[7] == "o":
        score -= 150
    if board[56] == "o":
        score -= 150
    if board[63] == "o":
        score -= 150
    for adjacent in adjacents:
        if board[adjacent] == "x":
            score -= 50
        if board[adjacent] == "o":
            score += 50
    for edge in edges:
        if board[edge] == "x":
            score += 100
        if board[edge] == "o":
            score -= 100
    if xcount >= 32 or ocount >= 32:
        score += xcount * 15
        score -= ocount * 15
    else:
        score += 15 * pmovesdiff
    return score

iboard = "..oooxxxo.ooooo.ooooxxxxoooxxxx.ooxxxxxooxxxxxxxxxxxxxx.xxxxxxxx"
iplayer = "o"

depth = 1
#nicely_print(iboard)
for count in range(iboard.count(".")):  # No need to look more spaces into the future than exist at all
   print(find_next_move(iboard, iplayer, depth))
   depth += 1

# class Strategy():

#    logging = True  # Optional

#    def best_strategy(self, board, player, best_move, still_running):

#        depth = 1

#        for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all

#            best_move.value = find_next_move(board, player, depth)

#            depth += 1