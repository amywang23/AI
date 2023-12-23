
import sys

width = 10
height = 20
scores = [40, 100, 300, 1200]

I0 = [['#','#','#','#']]
I1 = [['#'], ['#'],['#'], ['#']]
pieces = []
pieces.append(I0)
pieces.append(I1)

drop_col_start = [0,0]
drop_col_end = [6,9]        #inclusive

col_height = [0,0,0,0,0,0,0,0,0,0]

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
    print("col height", col_height)
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



def game_over(board):
    return True

    
iboard = "          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     ## #####  ########  ######### ######### ######### ######### ########## #### # # # # ##### ###   ########"

nicely_print(iboard)
#print(iboard)
print("*************************************\n")

find_col_height(iboard)

for i in range(len(pieces)):   #go through all pieces and orientations
    p = pieces[i]        #current piece
    prows = len(p)       #height of the piece
    pcols = len(p[0])    #width of the piece

    print("\n**************************************************",i)
    for j in range(drop_col_start[i], drop_col_end[i]+1): #drop from left to right cols
        newboard = iboard
        if prows == 1:      #only one row
            minh = 20
            minc = -1
            for k in range(pcols):
                if col_height[k+j] < minh:
                    minh = col_height[k+j]
                    minc = k+j
            print('j', j, "minh", minh, "minc", minc)
            if (minh == 0):
                print("GAME OVER")
            else:
                for k in range(pcols):
                    newboard = replace_cell(newboard, minh-1, k+j, "#") 
            nicely_print(newboard)
            print("-------------------------------------")

        if pcols == 1:  #only one col
            minh = 20

            for k in range(pcols):
                if col_height[k+j] < minh:
                    minh = col_height[k+j]
                   
            print('j', j, "minh", minh)
            if (minh - prows < 0):
                print("GAME OVER")
            else:
                for k in range(prows+1):
                    newboard = replace_cell(newboard, minh-k, j, "#") 
            nicely_print(newboard)
            print("-------------------------------------")


