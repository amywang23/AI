import sys

maxx = 1000000
directions = [-11, -10, -9, -1, 1, 9, 10, 11]
corners = [0, 7, 56, 63]
adjacents = [1, 6, 8, 9, 14, 15, 48, 49, 54, 55, 57, 62]
edges = [2,3,4,5,16,24,32,40,23,31,39,47, 58, 59, 60, 61]

# All your other functions

iboard = sys.argv[1]
iplayer = sys.argv[2]

depth = 1

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

#find the moves that you can make
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

#make the actual move
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

#convert line into actual board
def convert_board(board):
    newboard = "??????????"
    for i in range(8):
        newboard += "?"+ board[i*8:i*8+8] + "?"
    newboard += "??????????"
    return newboard

#who is your opponent
def get_opponent(token):
    if (token == "x"):
       return("o")
    else:
        return("x")

#the corresponding index for the two sizes of boards
def convert_index(index, num):
    if (num == 0):   #convert from 8*8 to 10*10
        row = int(index / 8)
        newindex = index + 10 + 2*row + 1
    else:               #convert from 10*10 to 8*8
        row = int(index / 10) - 1
        newindex = index - 10 - 2*row - 1
    return newindex

#board prints like a board
def nicely_print(board):
    board_rows = [board[x:x + 8] for x in range(0, 64, 8)]
    for row in board_rows:
        print(" ".join(list(row)))

#whats the next move that you could play
def find_next_move(board, player, depth):
   # Based on whether player is x or o, start an appropriate version of minimax
    scores = {}
    best_move = ''
    opponent = get_opponent(player)
    moves = possible_moves(board, player)
    for move in moves:
        newBoard = make_move(board, player, move)
        
        # SWAPPED
        val = min_max(newBoard,depth-1, opponent)
        scores[move]=val
    if player == "x":
        return max(scores,key=scores.get)
    elif player == "o":
        return min(scores,key=scores.get)
    return best_move    #return move with the best "score"
   # that is depth-limited to "depth".  Return the best available move.
   
#algorithm used to play
def min_max(board, depth, player):
    opponent = get_opponent(player)
    me = player
    scores = set()
    current_score = 0
    if depth == 0:
        return score(board, player)
    if (game_over(board, player)):
        xcount = board.count("x") 
        ocount = board.count("o")
        diff = xcount - ocount
        if diff < 0:
            return -maxx
        else:
            return maxx
    # moves = possible_moves(board, token)
    moves = possible_moves(board, player)
    if len(moves) == 0:
        return min_max(board,depth, opponent)
    if me == "x":
        for move in moves:
            newBoard = make_move(board, me, move)
            current_score = min_max(newBoard, depth-1, me)
            scores.add(current_score)
    elif me == "o":
        for move in moves:
            newBoard = make_move(board, me, move)
            current_score = min_max(newBoard,depth-1, me)
            scores.add(current_score)
    if (me == "x"):
        best_score =  max(scores)
    else:
        best_score =  min(scores)
    return  best_score     #return the best "score"

#did you win
def game_over(board, player):
    opponent = get_opponent(player)
    if len(possible_moves(board, player)) == 0 and len(possible_moves(board, opponent)) == 0:
        return True
    return False

#keeping track of the scores of possible moves -> what would be the most optimal move
def score(board, player):
    opponent = get_opponent(player)
    xcount = board.count("x") 
    ocount = board.count("o")
    xmobile = len(possible_moves(board, "x"))
    omobile = len(possible_moves(board, "o"))
    pmovesdiff = xmobile - omobile
    score = 0
    for corner in corners:
        if board[corner] == "x":
            score += 2000
        if board[corner] == "o":
            score -= 2000
    for adjacent in adjacents:
        for corner in corners:
            if board[corner] == None:    
                if board[adjacent] == player:
                    score -= 500
                if board[adjacent] == opponent:
                    score += 500
            elif board[corner] == player:
                if board[adjacent] == player:
                    score += 500
                if board[adjacent] == opponent:
                    score -= 500
    for edge in edges:
        if board[edge] == "x":
            score += 250
        if board[edge] == "o":
            score -= 250
    if xcount >=32  or ocount >= 32:
        score += xcount * 10
        score -= ocount * 10
    score += 20 * pmovesdiff
    return score

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