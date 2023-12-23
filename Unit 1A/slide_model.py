import sys

f = sys.argv[1]

with open(f) as f:
    line_list = [line.strip() for line in f]
    
def print_puzzle(dimen, line):
    rows = [line[col: col+dimen] for col in range(0, len(line), dimen)]
    for i in rows:
        print(" "+ i)
    
def find_goal(line):
    goal = sorted(line)
    for i in goal:
        goal += " " + i
    goal = goal.replace(".", "")
    goal = goal + "."
    return goal

def get_children(dimen, line):
    temp = line.index(".")
    result = []
    if temp%dimen > 0:
        result.append(switch(line, temp - 1, temp))
    if temp%dimen < dimen - 1:
        result.append(switch(line, temp, temp + 1))
    if temp//dimen > 0:
        result.append(switch(line, temp - dimen, temp))
    if temp//dimen < dimen - 1:
        result.append(switch(line, temp, temp + dimen))
    return result

def switch(line, i1, i2):
    temp = line[:i1]
    temp1 = line[i1 + 1:i2]
    temp2 = line[i2 + 1:]
    result = temp + line[i1] + temp1 + line[i2] + temp2
    return result
    
for index, elem in enumerate(line_list):
    elemlist = elem.split(" ")
    print("Line", index, "start state:")
    print_puzzle(int(elemlist[0]), elemlist[1])
    print("Line", index, "goal state:", find_goal(elemlist[1]))
    print("Line", index, "children:", get_children(int(elemlist[0]), elemlist[1]))