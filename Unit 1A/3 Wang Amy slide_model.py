import sys

f = sys.argv[1]

with open(f) as f:
    line_list = [line.strip() for line in f]
    
def print_puzzle(dimen, line):
    #take line (string) : two for loops looping through dimen, print by line _  _  _ 3 ABCDEFG.H
    rows = [line[col: col+dimen] for col in range(0, len(line), dimen)]
    for val in rows:
        print(' '.join(val))
    
def find_goal(line):
    goal = sorted(line)
    goal = ''.join(goal)
    goal = goal.replace('.', '')
    return(goal + ".")

def get_children(dimen, line):
    dot = line.index('.')
    final = []
    #move left
    if dot%dimen > 0:
        final.append(switch(line, dot - 1, dot))
    #move right
    if dot%dimen < dimen - 1:
        final.append(switch(line, dot, dot + 1))
    #move up
    if dot//dimen > 0:
        final.append(switch(line, dot - dimen, dot))
    #move down
    if dot//dimen < dimen - 1:
        final.append(switch(line, dot, dot + dimen))
    return final

#i1 < i2
def switch(line, i1, i2):
    s1 = line[:i1]
    s2 = line[i1 + 1: i2]
    s3 = line[i2 + 1:]
    final = s1 + line[i2] + s2 + line[i1] + s3
    return (final)

# for loop, separate size of puzzle and the actual puzzle, input into the function
# print(switch("abcdefg.h", 4, 7))
for index, elem in enumerate(line_list):
    elemlist = elem.split(" ")
    print("Line", index, "start state:")
    print_puzzle(int(elemlist[0]), elemlist[1])
    print("Line", index, "goal state:", find_goal(elemlist[1]))
    print("Line", index, "children:", get_children(int(elemlist[0]), elemlist[1]))