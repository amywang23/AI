import sys; args = sys.argv[1:]
# Arnav Kadam
LIMIT_AB = 15
import random, time, re
# Arnav Kadam, pd. 6, 2023

indices = [[] for i in range(64)]

def input():
    notation, moves, token, board = [ltr+str(i) for i in range(1, 9)  for ltr in "ABCDEFGH"], [], "", "...........................ox......xo..........................."
    for item in args:
        if len(item) == 64:
            board = item
            board = board.lower()
        elif item == "X" or item == "x": token = "x"
        elif item == "O" or item == "o": token = "o"
        else:
            if item.upper() in notation: moves.append(notation.index(item.upper()))
            elif len(item) <=2 and item!=-2: moves.append(int(item))
            else:
                i = 0
                while i < len(item):
                    if item[i] == "_": moves.append(int(item[i+1]))
                    elif item[i]!="-": moves.append(int(item[i:i+2]))
                    i+=2
    if not token:
        if board.count(".") % 2 == 0: token = "x"
        else: token = "o"
    return (board, token, moves)

def parseArgs(args):
    brd, tkn, moves = "...........................ox......xo...........................", "", []
    for arg in args:
        if re.seach(r"^[oxOX.]{64}$", arg): brd = arg
        if re.search(r"^[-_1-5]\d|6[0-3]+$", arg): moves+=[int(arg[i:i+2].replace("_","")) for i in range(0, len(arg), 2)]
        if re.search(r"/^[xoXO]$", arg): tkn = arg.lower()
    if not tkn: 
        tkn = "xo"[brd.count(".")&1]
    if not possible(brd, tkn): tkn = "xo"[tkn == "x"]

def display(board):
    for i in range(64):
        if i % 8 == 7:
            print(board[i])
        else:
            print(board[i] + "", end="")

def snapshot(board, token, move):
    eTkn = "x" if token == "o" else "o"
    if move == -1: 
        temp = eTkn
        eTkn = token
        token = temp
    choices = [*possible(board, eTkn).keys()]
    newBoard = "".join([(board[i], "*")[i in choices] for i in range(64)])
    if move != -1: print(f'{token} plays to {move}')
    display(newBoard)
    print()
    print(board + " " + str(board.count("x")) + "/" + str(board.count("o")))
    if "." not in board or "x" not in board or "o" not in board: return
    print("Possible moves for " + eTkn + ": ", end = "")
    counter = 0

    for item in choices:
        if counter != len(choices)-1: 
            print(str(item)+", ", end = "")
        else: print(str(item))
        counter+=1
    print()

def lookUp():
    global indices
    switches = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (-1, -1), (1, 1), (1, -1)]
    for i in range(64):
        for coords in switches:
            coordinates = [int(i/8), int(i % 8)]
            temp = []
            coordinates[0] = coordinates[0] + coords[0]
            coordinates[1] = coordinates[1] + coords[1]
            while(coordinates[0] >= 0 and coordinates[0] <= 7 and coordinates[1] >= 0 and coordinates[1] <=7):
                temp.append(coordinates[0]*8 + coordinates[1])
                coordinates[0] = coordinates[0] + coords[0]
                coordinates[1] = coordinates[1] + coords[1]
            if len(temp) > 1: indices[i].append(temp)

def possible(board, token):
    global indices
    etkn = 'xo'[token == 'x']
    choices = [i for i in range(64) if board[i] == "."]
    moves = dict()
    for num in choices:
        tempLst = indices[num]
        for list in tempLst:
            eTkn = False
            for idx in list:
                if board[idx] == token:
                    if eTkn:
                        if not num in moves: moves[num] = []
                        for index in list:
                            if index != idx: moves[num].append(index)
                            else: break
                        break
                    else: break
                elif board[idx] == etkn:
                    if not eTkn: eTkn = True
                else:
                    break
    return moves

def makeMoves(board, move, token, choices):
    tmpBoard = [*board]
    changes = choices[move] + [move]
    for idx in changes:
        tmpBoard[idx] = token
    return "".join(tmpBoard)

def alphabeta(brd, tkn, lower, upper):
    eTkn = "x" if tkn == "o" else "o"
    combined = possible(brd, tkn) #choices and type of moves
    moves = [*combined.keys()] 
    if not moves:
        if not possible(brd, eTkn):
            return (brd.count(tkn) - brd.count(eTkn), []) #score, num tokens
        ab = alphabeta(brd, eTkn, -upper, -lower)
        score = -ab[0]
        return (score, ab[1] + [-1])
    best = (lower-1, [])
    for move in moves:
        ab = alphabeta(makeMoves(brd, move, tkn, combined), eTkn, -upper, -lower)
        score = -ab[0]
        if score < lower: continue
        if score > upper: return (score, [])
        else:
            best = (score, ab[1] + [move])
        lower = score+1
    return best

cache = {}
def negamax(brd, tkn):
    eTkn = "x" if tkn == "o" else "o"
    if brd.count(".") == 0:
        return (brd.count(tkn) - brd.count(eTkn), []) #score, num tokens 
    combined = possible(brd, tkn) #choices and type of moves
    moves = [*combined.keys()] 
    optimal = (-9999, [])
    if not moves:
        if not possible(brd, eTkn):
            return (brd.count(tkn) - brd.count(eTkn), []) #score, num tokens
        nm = negamax(brd, eTkn)
        if -nm[0] > optimal[0]:
            optimal = (-nm[0], nm[1] + [-1])
        cache[(brd, tkn)] = optimal[0]

    for move in moves:
        newBrd = makeMoves(brd, move, tkn, combined)
        if (newBrd, eTkn) in cache and cache[(newBrd, eTkn)] <= optimal[0]: continue
        nm = negamax(newBrd, eTkn)
        cache[(newBrd, eTkn)] = -nm[0]
        if -nm[0] > optimal[0]:
            optimal = (-nm[0], nm[1] + [move])
        cache[(brd, tkn)] = optimal[0]

    return optimal

def quickMove(arg1, arg2, arg3):
    global count2
    board, token = arg1, arg2
    if arg3: combined = arg3
    else: 
        combined = possible(board, token) #choices and type of moves
    choices = [*combined.keys()]
    if not choices: return choices
    corners = [0, 7, 63, 56]
    deathRow = [9, 10, 11, 12, 13, 14, 15, 17, 22, 25, 30, 33, 38, 41, 46, 49, 54]
    cX = [9, 14, 49, 54]
    test, test1, test2, test3, = [1, 8 , 9], [6, 14, 15], [48, 49, 57], [55, 62, 54]
    edges = [0, 1, 2, 3, 4, 5, 6, 7, 8, 16, 24, 32, 40, 48, 56, 15, 23, 31, 38, 47, 55, 63, 62, 61, 60, 59, 58, 57] #all edges

    #if board.count(".") < LIMIT_AB and arg3:
    #    res = alphabeta(board, token, -64, 64)
        #res = negamax(board, token)
    #    return res[1][-1]

    #corner grabbing
    for item in choices: 
        if item in corners: return item

    #safe edge
    bestOptions = []
    for idx in choices:
        if (idx in test and board[0] == ".") or (idx in test1 and board[7] == ".") or (idx in test2 and board[56] == ".") or (idx in test3 and board[63] == "."): x = 1
        else: bestOptions.append(idx)

    #limit mobilitiy
    mobility = []
    for item in bestOptions:
         tmpBoard = makeMoves(board, item, token, combined)
         token = 'xo'[token == 'x'] #switch token to o
         tmpPossible = [*possible(tmpBoard, token).keys()] #see possible choices for o
         token = 'xo'[token == 'x'] #switch token back to x
         tmpPossible = [item for item in tmpPossible if item not in deathRow]
         mobility.append((len(tmpPossible), item))
    mobility = sorted(mobility)

    if mobility: return mobility[0][1]
    return choices[0]
        
def tournament():
    time1 = time.process_time()
    myTokens, totalTokens, score, worst1, worst2, data, tkn, eTkn, moveChecker = 0, 0, 0, 64, 64, dict(), "x", "o", True

    for i in range(100):
        brd, transcript, myMove = "...........................ox......xo...........................", "", moveChecker
        eTkn = "x" if tkn == "o" else "o"
        while True: #one game
            if myMove:
                moves = possible(brd, tkn)
                if not moves:
                    moves = possible(brd, eTkn)
                    if not moves: #game is over
                        score = brd.count(tkn) - brd.count(eTkn)
                        myTokens+= brd.count(tkn)
                        totalTokens+= 64 - brd.count(".")
                        data[i] = [score, tkn, transcript]
                        break
                    else:
                        transcript+="-1"
                        move = [*moves.keys()][random.randint(0, len(moves)-1)]
                        brd = makeMoves(brd, move, eTkn, moves)
                        if len(str(move)) == 1: transcript+="_" + str(move)
                        else: transcript+=str(move)
                else:
                    move = quickMove(brd, tkn, moves)
                    brd = makeMoves(brd, move, tkn, moves)
                    if len(str(move)) == 1: transcript+="_" + str(move)
                    else: transcript+=str(move)
                    myMove = False
            else:
                moves = possible(brd, eTkn)
                if not moves:
                    moves = possible(brd, tkn)
                    if not moves: #game is over
                        score = brd.count(tkn) - brd.count(eTkn)
                        myTokens+= brd.count(tkn)
                        totalTokens+= 64 - brd.count(".")
                        data[i] = [score, tkn, transcript]
                        break
                    else:
                        transcript+="-1"
                        move = quickMove(brd, tkn, moves)
                        brd = makeMoves(brd, move, tkn, moves)
                        if len(str(move)) == 1: transcript+="_" + str(move)
                        else: transcript+=str(move)
                else:
                    move = [*moves.keys()][random.randint(0, len(moves)-1)]
                    brd = makeMoves(brd, move, eTkn, moves)
                    if len(str(move)) == 1: transcript+="_" + str(move)
                    else: transcript+=str(move)
                    myMove = True
        moveChecker = True if moveChecker == False else False
        tkn = 'xo'[tkn == 'x']
        eTkn = 'xo'[eTkn == 'x']
    w1, w2, = 0, 0
    for i in range(100):
        if data[i][0] < worst1: 
            worst1 = data[i][0]
            w1 = i
        elif data[i][0] < worst2: 
            worst2 = data[i][0]
            w2 = i
    time2 = time.process_time()
    #print stats
    for i in range (0, 100, 10):
        line = "".join([("  " + str(data[x][0]), "   " + str(data[x][0]))[len(str(data[x][0])) == 1] for x in range(i, i+10)])
        print(line)

    print()
    print()
    print(f'My tokens: {myTokens}; Total Tokens: {totalTokens}')
    print(f'Score: {round(myTokens/totalTokens*100, 1)}%')
    print(f'NM/AB Limit: {LIMIT_AB}')
    print(f'Game {w1} as {data[w1][1]} => {data[w1][0]}:')
    print(data[w1][2])
    print(f'Game {w2} as {data[w2][1]} => {data[w2][0]}:')
    print(data[w2][2])
    print(f'Elapsed time: {round(time2-time1, 2)}s')
             
def main():
    global indices
    lookUp()
    if args:
        # Othello 3
        brd, tkn, moves = input()
        snapshot(brd, tkn, -1)
        for move in moves:
            if move < 0: 
                continue
            combined = possible(brd, tkn)
            if not combined: 
                tkn = 'xo'[tkn == 'x']
                combined = possible(brd, tkn)
            brd = makeMoves(brd, move, tkn, combined)
            snapshot(brd, tkn, move)
            tkn = 'xo'[tkn == 'x']

        # Othello 4
        combined = possible(brd, tkn)
        if not combined: 
            tkn = 'xo'[tkn == 'x']
            combined = possible(brd, tkn)
        if "." in brd and "x" in brd and "o" in brd:
            qm = quickMove(brd, tkn, [])
            print(f'My preferred move is {qm}')

        # Othello 5/6
        if brd.count(".") < LIMIT_AB and "." in brd and "x" in brd and "o" in brd:
            #check for alphabeta
            res = alphabeta(brd, tkn, -64, 64)
            print("Min score: " + str(res[0]), end = "")
            print("; " + "Move sequence: " + str([*res[1]]))
            return res[1][-1]

    else: tournament()

main()
# Arnav Kadam, pd. 6, 2023