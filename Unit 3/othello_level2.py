from othello_imports import possible_moves, make_move
import sys

INFINITY = 1000000
directions = [-11, -10, -9, -1, 1, 9, 10, 11]
weight = [
    100, -10,  10,   3,   3,  10, -10, 100,
    -10, -20,  -3,  -3,  -3,  -3, -20, -10,
     10,  -3,   8,   1,   1,   8,  -3,  10,
      3,  -3,   1,   1,   1,   1,  -3,   3,
      3,  -3,   1,   1,   1,   1,  -3,   3,
     10,  -3,   8,   1,   1,   8,  -3,  10,
    -10, -20,  -3,  -3,  -3,  -3, -20, -10,
    100, -10,  10,   3,   3,  10, -10, 100,
]

# All your other functions

iboard = sys.argv[1]
iplayer = sys.argv[2]

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

def nicely_print(board):
    board_rows = [board[x:x + 8] for x in range(0, 64, 8)]
    for row in board_rows:
        print(" ".join(list(row)))


def find_next_move(board, player, depth):
   # Based on whether player is x or o, start an appropriate version of minimax
    best_move = ''
    best_val = -INFINITY
    opponent = get_opponent(player)
    moves = possible_moves(board, player)
    #print("find next move moves=", moves)
    if (len(moves)==0):
        return ""
    if (len(moves)==1):
        return moves[0]
    for move in moves:
        newBoard = make_move(board, player, move)
        #print("\n-------------------------------------------\nNext move depath",depth, player, "move: ", move, newBoard)
        val = alpha_beta(newBoard, opponent, depth, -INFINITY, INFINITY, player)
        #print(player, "move: ", move, "returned alpha_beta value:", val, "best_val:", best_val)
        if (best_val < val):
            best_val = val
            best_move = move
            #print("updated best move:", move)
    return best_move    #return move with the best "score"
   # that is depth-limited to "depth".  Return the best available move.
   
def alpha_beta(board, token, depth, alpha, beta, player):
    scores = set()
    current_score = 0
    if depth == 0 or game_over(board, player):
        #print("depth=", depth, "????????????????????????", "alpha=", alpha, "beta=", beta)
        #nicely_print(board)
        return score(board, player)
    moves = possible_moves(board, token)
    #print("alpha_beta depth", depth, " token", token, "alpha=", alpha, "beta=", beta, moves)
    if len(moves) == 0:
        #print("alpha_beta no legal move for ", token)
        return alpha_beta(board, get_opponent(token), depth-1, alpha, beta, player)
    for move in moves:
        #print("\nalpha_beta method calling depth", depth, "**************************", token ," move:", move)
        newBoard = make_move(board, token, move)
        #print(token, "move: ", move, newBoard)
        current_score = alpha_beta(newBoard, get_opponent(token), depth-1, alpha, beta, player)

        if token == player:
            alpha = max(alpha, current_score)
            if beta <= alpha:
                #print("alpah_beta pruning alpha")
                break
        else:
            beta = min(beta, current_score)
            if beta <= alpha:
                #print("alpah_beta pruning beta")
                break
        
        #print("alpha_beta method new score: ", "alpha=", alpha, "beta=", beta)
    
    if (token == player):
        best_score = alpha
    else:
        best_score =  beta
    return  best_score     #return the best "score"

def game_over(board, player):
    opponent = get_opponent(player)
    # print("game over: ", player, possible_moves(board, player))
    # print("game over: ", opponent, possible_moves(board, opponent))
    if len(possible_moves(board, player)) == 0 and len(possible_moves(board, opponent)) == 0:
        return True

def score(board, player):
    if (game_over(board, player)):
        x = board.count(player) 
        o = board.count(get_opponent(player))
        diff = x - o
        if diff < 0:
            return -INFINITY
        else:
            return INFINITY

    score = 0
    opponent = get_opponent(player)

    for i in range(64):
        if board[i] == player:
            score += weight[i]
			#print("+++i:", i, "weight:", weight[i], "score:", score)
        elif board[i] == opponent:
            score -= weight[i]
			#print("--i:", i, "weight:", weight[i], "score:", score)
    return score
    
#iboard = "xxoo.xox.....oox......oxo..ooxooo..oox.ox.xxx..oxoox...o.....xox"      #line 1
# iboard = "oooooo..oooooo.oooxoxoooxooooxooxoxxxoxoxoxxxxxoxoooooooxo.oxo.."
# iboard = "ooooooxooooooxxoooxoxoxoxooooxxoxoxoooxoxooxxoxoxooooxooxo.ooooo"
# player = 'x'

#nicely_print(iboard)
for count in range(iboard.count(".")):  # No need to look more spaces into the future than exist at all
   print(find_next_move(iboard, iplayer, depth))
   depth += 1
#    if depth > 3:
#     break

# class Strategy():

#    logging = True  # Optional

#    def best_strategy(self, board, player, best_move, still_running):

#        depth = 1

#        for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all

#            best_move.value = find_next_move(board, player, depth)

#            depth += 1