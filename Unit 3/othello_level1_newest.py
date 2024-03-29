from othello_imports import possible_moves, make_move
import sys

maxx = 1000000
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

def nicely_print(board):
    board_rows = [board[x:x + 8] for x in range(0, 64, 8)]
    for row in board_rows:
        print(" ".join(list(row)))


def find_next_move(board, player, depth):
   # Based on whether player is x or o, start an appropriate version of minimax
    best_move = -1
    best_val = -maxx
    opponent = get_opponent(player)
    for move in possible_moves(board, player):
        newBoard = make_move(board, player, move)
        # print("\nNext move", player, "move: ", move, newBoard)
        if player == "x":
            val = max_step(newBoard, opponent, depth)
        if player == "o":
            val = min_step(newBoard, opponent, depth)
        # print(player, "move: ", move, "returned min_max value:", val, "best_val:", best_val)
        if (best_val < val):
            best_val = val
            best_move = move
            # print("updated best move:", move)
    return best_move    #return move with the best "score"
   # that is depth-limited to "depth".  Return the best available move.
   
def max_step(board, token, depth):
    if depth == 0 or game_over:
        return score(board)
    results = list()
    current_player = token
    for next_board in possible_moves(board, current_player):
        results.append(min_step(make_move(board, current_player, next_board), current_player, depth-1))
    return max(results)

def min_step(board, token, depth):
    if depth == 0 or game_over:
        return score(board)
    results = list()
    current_player = token
    for next_board in possible_moves(board, current_player):
        results.append(max_step(make_move(board, current_player, next_board), current_player, depth-1))
    return min(results)

def game_over():
    opponent = get_opponent(player)
    if len(possible_moves(board, player)) == 0 and len(possible_moves(board, opponent)) == 0:
        return True

def score(board):
    if (game_over()):
        x = board.count(player) 
        o = board.count(get_opponent(player))
        diff = x - o
        if diff < 0:
            return -maxx
        else:
            return maxx

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
    
# board = "xxoo.xox.....oox......oxo..ooxooo..oox.ox.xxx..oxoox...o.....xox"      #line 1
# player = 'x'


for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
   print(find_next_move(board, player, depth))
   depth += 1