from collections import deque
from time import perf_counter
#AAA..B
#..C..B
#XXC..B
#D.C.EE
#D...F.
#GGG.F.

start = perf_counter()

line_list = ["AAA..B..C..BXXC..BD.C.EED...F.GGG.F."]

def print_puzzle(size, strRep):
    matrixRep = [strRep[x: x+size] for x in range(0, len(strRep), size)]
    for y in matrixRep:
        print(' '.join(y))

#result is [], the idx is not a head
#result is [a,b,c] a is the head index
#b is number of blocks in this car 2/3, c is the direction 0 for row/1 for col
def isHead(state, idx):
    row = idx/6
    col = idx%6
    letter = state[idx:idx+1]
    result = []

    if letter=='.':
        return result
    if(col!=0):
        if letter==state[idx-1:idx]:
            return result
    if(row!=0):
        if letter==state[idx-6:idx-6+1]:
            return result
    if(col!=5):
        nextletter = state[idx+1:idx+2]
        if letter==nextletter:
            result.append(idx)
            if col<4 and letter==state[idx+2:idx+3]:
                result.append(3)
            else:
                result.append(2)
            result.append(0)
            return result
    if(row!=5):
        nextletter = state[idx+6:idx+6+1]
        if letter==nextletter:
            result.append(idx)
            if row<4 and letter==state[idx+12:idx+12+1]:
                result.append(3)
            else:
                result.append(2)
            result.append(1)
            return result
    
    return result

def testGoal(strRep):
    return strRep[16:18] == "XX"

# swap two charactors in string
# loc1 < loc2
def swap(string, p1, p2):
    if p1 < p2:
        loc1 = p1
        loc2 = p2
    else:
        loc2 = p1
        loc1 = p2
    return string[:loc1] + string[loc2:loc2+1] + string[loc1 + 1: loc2] + string[loc1: loc1+1] + string[loc2+1:]

#length of car, direction 0 row/1 col
def movecar(string, start, end, length, rowcol, direction):
    newstring = swap(string, start, end)
    if (rowcol == 0):       #horizontal
        if direction==0:    #move left
            newstring = swap(newstring, start+1, end+1)
            if (length==3):
                newstring = swap(newstring, start+2, end+2)
        if direction==1:    #move right
            newstring = swap(newstring, start-1, end-1)
            if (length==3):
                newstring = swap(newstring, start-2, end-2)
    
    if (rowcol == 1):       #vertical
        if direction==0:    #move up
            newstring = swap(newstring, start+6, end+6)
            if (length==3):
                newstring = swap(newstring, start+12, end+12)
        if direction==1:    #move down
            newstring = swap(newstring, start-6, end-6)
            if (length==3):
                newstring = swap(newstring, start-12, end-12)
    return newstring
    


# size -- board size
# loc -- "." location in the board status string
#
def get_children(state):

    res = []
    for idx in range(len(state)):
        #if idx!=23:
        #    continue
        h = isHead(state, idx)
        if (len(h)!=0):     #is a head of a car
            row = int(idx / 6)
            col = idx % 6
            #print("row ", row, "col", col)
            newstate = ""
            if h[2] == 0:    #horizontal
                currentone =state[idx:idx+h[1]]
                endidx = idx+h[1]-1 
                #print("idx", idx, "endidx", endidx, h, currentone)
                if(col>0):
                    for i in range(col):
                        if state[idx-i-1:idx] == ".":
                            newstate = movecar(state, idx, idx-i-1, h[1], 0, 0)
                            res.append(newstate)
                            #print("left newstate", i, newstate)
                        else:
                            break
                rightmove = 6-col-h[1]
                if(rightmove>0):
                    for i in range(rightmove):
                        if state[endidx+1+i:endidx+2+i] == ".":
                            newstate = movecar(state, endidx, endidx+1+i, h[1], 0, 1)
                            res.append(newstate)
                            #print("right newstate", i, newstate)
                        else:
                            break
                
                
            if h[2] == 1:    #vertical
                currentone =state[idx:idx+1] + state[idx+6:idx+6+1]
                if h[1]==3:
                     currentone = currentone+state[idx+12:idx+12+1] 
                endidx = idx+6*(h[1]-1) 
                #print("idx", idx, "endidx", endidx, h, currentone)

                if(row>0):
                    for i in range(row):
                        if state[idx-6*(i+1):idx-6*(i+1)+1] == ".":
                            newstate = movecar(state, idx, idx-6*(i+1), h[1], 1, 0)
                            res.append(newstate)
                            #print("up newstate", i, newstate)
                        else:
                            break
                downmove = 6-row-h[1]
                if(downmove>0):
                    for i in range(downmove):
                        if state[endidx+6*(i+1):endidx+6*(i+1)+1] == ".":
                            newstate = movecar(state, endidx, endidx+6*(i+1), h[1], 1, 1)
                            res.append(newstate)      
                            #print("down newstate", i, newstate)
                        else:
                            break
                
    return res


def BFS(bsize, bstr):
    fringe = deque()
    visited = set()
    level = 0
    path = []
    path.append(bstr)

    fringe.append((level, bstr, path))
    visited.add(bstr)

    while len(fringe) > 0 :
        fringeEle = fringe.popleft()

        if testGoal(fringeEle[1]):
            return fringeEle
        children = get_children(fringeEle[1])

        for c in children:
            if c not in visited:
                newpath = []
                for item in fringeEle[2]: newpath.append(item)
                newpath.append(c)
                fringe.append((fringeEle[0]+1, c, newpath))
                visited.add(c)
    return None

def findHeads(curentline):
    for idx in range(len(currentline)):
        h = isHead(currentline, idx)
        if (len(h)==0):
            print("idx ", idx, "is not head")
        else:
            print("idx ", idx, "HEAD: ", h)
    return

size = 6
for idx, line in enumerate(line_list):
    currentline = line_list[idx]

    #currentline = "..A.....A...XXA...BBB..C.....C.....C"
    #currentline = "AA...BC..D.BCXXD.BC..D..E...FFE.GGG."
    print_puzzle(size, currentline)
    # result = get_children(currentline)
    # for r in result:
    #         print_puzzle(size, r)
    #         print()

    result = BFS(size, currentline)
    if result != None:
        for r in result[2]:
            print("solution len", len(result[2]), "-------", r)
            print_puzzle(size, r)
            print()
    else:
        print("NO SOLUTION")
    
end = perf_counter()
print('Total time:', end - start)