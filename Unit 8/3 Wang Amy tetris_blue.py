import sys

width = 10
height = 20
scores = [40, 100, 300, 1200]

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

pieces = []
pieces.append(I0)
pieces.append(I1)
pieces.append(O)
pieces.append(T0)
pieces.append(T1)
pieces.append(T2)
pieces.append(T3)
pieces.append(S0)
pieces.append(S1)
pieces.append(Z0)
pieces.append(Z1)
pieces.append(J0)
pieces.append(J1)
pieces.append(J2)
pieces.append(J3)
pieces.append(L0)
pieces.append(L1)
pieces.append(L2)
pieces.append(L3)

col_height = [0,0,0,0,0,0,0,0,0,0]      #current board height for each col
piece_diff =[[0,0,0,0],[0],[0,0],[0,0,0],[0,1],[1,0,1],[1,0],[0,0,1],[1,0],
[1,0,0],[0,1],[0,0,0],[0,2],[1,1,0],[0,0],[0,0,0],[0,0],[0,1,1],[2,0]]      #piece block start index from bottom for each col

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
    # print("col height", col_height)
    return col_height

def replace_cell(board, row, col, char):
    idx = convert_rowcol_to_index(row, col)
    board = board[:idx] + char + board[idx+1:]

    return board

def nicely_print(board):
    board_rows = [board[x:x + width] for x in range(0, width*height, width)]
    count = 0
    for row in board_rows:
        # if (count < 10):
        #     print(count, "  ", " ".join(list(row)))
        # else:
        #     print(count, " ", " ".join(list(row)))
        count += 1

def update_board(board):
    newboard = ''

    for i in range(height-1, -1, -1):
        str = board[i*width:(i+1)*width]
        if str != "##########":
            newboard = str + newboard

    if len(newboard) < width*height:
        fillval = " " * (width*height-len(newboard))
        newboard = fillval + newboard
        
    return newboard

outputfile = open('tetrisout.txt', 'w')

iboard = sys.argv[1]
    
# iboard = "          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     ## #####  ########  ######### ######### ######### ######### ########## #### # # # # ##### ###   ########"

# nicely_print(iboard)
#print(iboard)
# print("*************************************\n")

find_col_height(iboard)

for i in range(len(pieces)):   #go through all pieces and orientations
    # if i != 1:
    #     continue
    p = pieces[i]        #current piece
    prows = len(p)       #height of the piece
    pcols = len(p[0])    #width of the piece


    # print("\n**************************************************","i=",i,"cols=",pcols,"rows=",prows, p)
    drop_col_end = width - pcols
    for j in range(drop_col_end+1): #drop from left to right cols
        newboard = iboard
        
        minh = 20           #the starting row for this piece
        for k in range(pcols):
            diff = piece_diff[i][k]
            if col_height[j+k]-1+diff < minh:
                minh = col_height[j+k]-1+diff 

        # print('j', j, "minh", minh)
        if (minh + 1 - prows < 0):
            # print("GAME OVER")
            print("GAME OVER", file=outputfile)
        else:
            for ii in range(prows):
                for k in range(pcols):
                    if p[prows-ii-1][k] == '#':   #start from bottom of the piece
                        newboard = replace_cell(newboard, minh-ii, j+k, "#")

            nicely_print(newboard)
            updatedboard = update_board(newboard)
            # if (updatedboard!=newboard):
                # print("!!!!!!!!!!!!!!!!!!!!!!!board updated")
                # nicely_print(updatedboard)
            print(updatedboard, file=outputfile)
        # print("-------------------------------------")