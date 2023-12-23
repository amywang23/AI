import random
import sys

width = 10
height = 20
scores = [40, 100, 300, 1200]
neg_inf = -10000000

near_wall = 0
touch_edges = 0
row_placement = 0 

CO_BOARD_HEIGHT = -20
CO_WELL_DEPTH = -10
CO_HOLES_NUMBER = -10
CO_LINES_REMOVED = 100
CO_NEAR_WALL = 30
CO_EDGE_NUMBER = 30
CO_ROW_PLACEMENT = 50
CO_EMPTY_SPACES = 20

picked_strategy = [CO_BOARD_HEIGHT,CO_WELL_DEPTH,CO_HOLES_NUMBER,CO_LINES_REMOVED,CO_NEAR_WALL,CO_EDGE_NUMBER,CO_ROW_PLACEMENT,CO_EMPTY_SPACES]

I0 = [['#','#','#','#']]
I1 = [['#'], ['#'],['#'], ['#']]
O = [['#','#'],['#','#']]
T0 = [[' ','#', ' '],['#','#','#']]
T1 = [['#', ' '],['#','#'],['#', ' ']]
T2 = [['#','#','#'],[' ', '#',' ']]
T3 = [[' ', '#'],['#','#'],[' ', '#']]
S0 = [[' ','#', '#'],['#','#',' ']]
S1 = [['#', ' '],['#','#'],[' ', '#']]
Z0 = [['#', '#', ' '],[' ', '#','#']]
Z1 = [[' ', '#'],['#','#'],['#', ' ']]
J0 = [['#',' ', ' '],['#','#','#']]
J1 = [['#', '#'],['#',' '],['#', ' ']]
J2 = [['#','#','#'], [' ',' ', '#']]
J3 = [[' ', '#'],[' ','#'],['#', '#']]
L0 = [[' ',' ', '#'],['#','#','#']]
L1 = [['#', ' '],['#',' '],['#', '#']]
L2 = [['#','#','#'], ['#',' ', ' ']]
L3 = [['#', '#'],[' ','#'],[' ', '#']]

lines_cleared = 0
col_height = [0,0,0,0,0,0,0,0,0,0]      #current board height for each col
piece_diff =[[0,0,0,0],[0],[0,0],[0,0,0],[0,1],[1,0,1],[1,0],[0,0,1],[1,0],
[1,0,0],[0,1],[0,0,0],[0,2],[1,1,0],[0,0],[0,0,0],[0,0],[0,1,1],[2,0]]      #piece block start index from bottom for each col

dict1 = {
    'I': [I0,I1],
    'O': [O],
    'T': [T0,T1,T2,T3],
    'S': [S0,S1],
    'Z': [Z0,Z1],
    'J': [J0,J1,J2,J3],
    'L': [L0,L1,L2,L3]
}
dict2 = {
    'I': 0,
    'O': 2,
    'T': 3,
    'S': 7,
    'Z': 9,
    'J': 11,
    'L': 15
}

def convert_index_to_rowcol(index):
    row = index / width
    col = index % width

    return (row, col)

def convert_rowcol_to_index(row, col):
    idx = row*width + col

    return idx

def find_col_height(board):
    global col_height
    for i in range(10):     #go through cols
        for j in range(20):     #go through rows
            idx = convert_rowcol_to_index(j, i)
            if (board[idx]=='#'):
                col_height[i] = j
                break
    #print("col height", col_height)
    return col_height

def replace_cell(board, row, col, char):
    idx = convert_rowcol_to_index(row, col)
    board = board[:idx] + char + board[idx+1:]

    return board

def nicely_print(board):
    board_rows = [board[x:x + width] for x in range(0, width*height, width)]
    count = 0
    for row in board_rows:
        if (count < 10):
            print(count, "  ", " ".join(list(row)))
        else:
            print(count, " ", " ".join(list(row)))
        count += 1

def update_board(board):
    global lines_cleared
    newboard = ''
    lines_cleared = 0

    for i in range(height-1, -1, -1):
        str = board[i*width:(i+1)*width]
        if str != "##########":
            newboard = str + newboard
        else:
            lines_cleared += 1

    if len(newboard) < width*height:
        fillval = " " * (width*height-len(newboard))
        newboard = fillval + newboard
        
    return newboard

def place(p, diffidx, j, board):  # p=piece, i=idx of this piece, j=col
    global by_wall, touch_edges, row_placement

    updatedboard = board
    newboard = board
    prows = len(p)       #height of the piece
    pcols = len(p[0])   

    jj = j + pcols -1               #right edge of the piece
    if (width - 1 - jj > j ):       #calculate which side is closer to wall
        by_wall = width - j         #closer to the wall gets larger value
    else:
        by_wall = width - (width - 1 - jj)

    touch_edges = 0
    row_placement = 0

    minh = 20           #the starting row for this piece
    for k in range(pcols):
        diff = piece_diff[diffidx][k]
        if col_height[j+k]-1+diff < minh:
            minh = col_height[j+k]-1+diff 

    print('j', j, "minh", minh, "diffidx", diffidx, p)
    row_placement = minh
    if (minh + 1 - prows < 0):
        print("GAME OVER")
        updatedboard = "GAME OVER"
    else:
        for ii in range(prows):
            for k in range(pcols):
                if p[prows-ii-1][k] == '#':
                    newboard = replace_cell(newboard, minh-ii, j+k, "#")
                    #calculate edges that touch original blocks
                    #print("&&&&&&&&&& ii", ii, "k", k)
                    if ii==0 and minh<height: # bottom row
                        #print("bottom row")
                        if (minh == height -1):
                            touch_edges += 1
                        else:
                            char = board[convert_rowcol_to_index(minh+1,j+k)] #find the block below
                            if (char=="#"):
                                touch_edges += 1
                    if k == 0:      #left column
                        #print("left col")
                        if (j==0):  #touch the wall
                            touch_edges += 1
                        else:
                            char = board[convert_rowcol_to_index(minh-ii,j-1)] #find the block below
                            if (char=="#"):
                                touch_edges += 1
                    if k == pcols-1:      #right column
                        #print("right col")
                        if (j+pcols==width+1):  #touch the wall
                            touch_edges += 1
                        else:
                            char = board[convert_rowcol_to_index(minh-ii,j+pcols)] #find the block below
                            if (char=="#"):
                                touch_edges += 1


        nicely_print(newboard)
        updatedboard = update_board(newboard)
        if (updatedboard!=newboard):
            print("!!!!!!!!!!!!!!!!!!!!!!!board updated")
            nicely_print(updatedboard)
    return updatedboard

def make_new_board():
    iboard = "          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     ## #####  ########  ######### ######### ######### ######### ########## #### # # # # ##### ###   ########"
    nicely_print(iboard)
    print("*************************************new board\n")
    return iboard

def choose_piece():
    piecename = random.sample("IOTSZJL", 1)
    
    print("piecename", piecename)
    return piecename[0]

def find_well_depth(board):
    max = 0

    for i in range(width):
        count = 0
        for j in range(height):
            if board[j*width+i] == ' ':
                count += 1
            else:
                break
        if max < count:
            max = count

    return max

def find_holes(board):
    count = 0
    for i in range(10, width*height):
        if board[i] == ' ' and board[i-width] == '#':
            count += 1

    return count

def heuristic(board, strategy):
    global by_wall, touch_edges, row_placement
    if board == "GAME OVER":
        return neg_inf

    #strategy = [BOARD_HEIGHT, WELL_DEPTH, HOLES_NUMBER, LINES_REMOVED]
    #a, b, c = strategy # As many variables as you want!
    idx = board.find("#")
    max_col_height = height - int(idx / width)
    welldepth = find_well_depth(board)
    holes = find_holes(board)
    empty_spaces = len(board.replace("#",""))

    print("@@@@@@@@@@@@@@@@@@ max_height", max_col_height,"welldepth", welldepth, "holes", holes, "linescleared", lines_cleared,"wall",by_wall,"edge",touch_edges,"rowplace", row_placement)
    value = 0
    value += strategy[0] * max_col_height       #a * (perhaps highest column height?)
    value += strategy[1] * welldepth            #b * (perhaps deepest well depth?)
    value += strategy[2] * holes                #c * (perhaps number of holes in board, ie empty spaces with a filled space above?)
    value += strategy[3] * lines_cleared        #d * (perhaps the number of lines that were just cleared, in the move that made this board?)
                # add as many variables as you want - whatever you think might be relevant!
    
    value += strategy[4] * by_wall
    value += strategy[5] * touch_edges
    value += strategy[6] * row_placement
    value += strategy[7] * empty_spaces
    # if (board.replace(" ","") == ""):      #whole board cleared
    #     value += 1000

    return value


def play_game(strategy):
    global lines_cleared
    board = make_new_board()
    points = 0
    gameover = False
    while not gameover:
        find_col_height(board)
        piecename = choose_piece()      #"T"
        piecelist = dict1[piecename]
        i = dict2[piecename]
        count = 0               #orientation order
        maxscore = neg_inf
        maxboard = ''
        max_lines_cleared = 0
        for p in piecelist:
            prows = len(p)       #height of the piece
            pcols = len(p[0])    #width of the piece
            print("\n"+piecename+"**************************************************", "cols=",pcols,"rows=",prows, p)
    
            drop_col_end = width - pcols
            for j in range(drop_col_end+1): #drop from left to right cols
            #for each column on the board where this orientation will fit:
                poss_board = place(p, i+count, j, board)
                poss_score = heuristic(poss_board, picked_strategy)
                print("lines_cleared", lines_cleared, "poss_score", poss_score)
                print("-------------------------------------")
                if poss_board == "GAME OVER":
                    continue
                if poss_score > maxscore:
                    maxscore = poss_score
                    maxboard = poss_board
                    max_lines_cleared = lines_cleared
                # Keep track of the board with the highest heuristic score however you like!
            count += 1
        print("maxboard", maxboard)
        if maxboard == '':
            gameover = True
            break
        board = maxboard #(the board with the highest heuristic score)
        if max_lines_cleared > 0:
            points += scores[lines_cleared-1] #reminder: 1 row cleared --> 40 points, 2 --> 100, 3 --> 300, 4 --> 1200
            print("lines_cleared", max_lines_cleared, "points", points)
        #break
    return points

def generate_strategy():
    strategy = []
    for i in range(8):
        if i < 3:
            strategy.append(random.random()*-1)
        else:
            strategy.append(random.random())
    print("generated strategy", strategy)
    return strategy

generate_strategy()
total = play_game(0)
print("total points", total)








