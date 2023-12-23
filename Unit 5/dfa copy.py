import sys
from collections import defaultdict

dfalist = []
###### DFA 1 ################################## aab
letters1 ="ab"
statenum1 = 4
final1 = [3]
dfa1 = {
    0: {
         "a": 1
        },
    1: {
        "a": 2
        },
    2: {
        "b": 3
        },
    3: {}
}

letterslist = ['','ab','','','','','','']
statenum = [0,4,0,0,0,0,0,0]
final=[[],[3],[],[],[],[],[],[]]
dfa = defaultdict(list)
mode = 1

arg1 = sys.argv[1]
n = 0
if len(arg1)==1 and arg1 in ("1","2","3","4","5","6","7"):
    mode = 2
    n = int(arg1) - 1 

dfafilename = arg1
stringfilename = sys.argv[2]

if mode == 1:
    with open(dfafilename) as f:
        dfadata = f.read()

with open(stringfilename) as f:
    line_list = [line.strip() for line in f]

def build_dfa(data):
    global letters, statenum, final
    sections = data.split("\n\n")

    lines = sections[0].split("\n")
    letters = lines[0]
    statenum = int(lines[1])
    final = lines[2].split(" ")
    final = [int(i) for i in final]

    print("letters", letters,"|")
    print("statenum", statenum)
    print("final", final)

    sections.pop(0)
    for sec in sections:
        lines = sec.split("\n")
        print(lines)
        dict = defaultdict(list)
        state = int(lines[0])
        lines.pop(0)
        for line in lines:
            pairs = line.split(" ")
            dict[pairs[0]] = int(pairs[1])
        dfa[state] = dict
    


    return

def print_dfa(dfa, final):
    print("*",  end ="  ")
    for l in letters:
        print(l, end="  ")
    print()

    for d in dfa:
        print(d, end ="  ")
        states = dfa[d]
        for l in letters:
            if l in states:
                print(states[l],end ="  ")
            else:
                print("_",end ="  ")
        print()
    print("Final nodes:", final)
    return

def process(str):
    match = False
    state = 0

    for c in str:
        moves = dfa[state]
        if c in moves:
            state = moves[c]
        else:
            return False

    if state in final:
        return True
    else:
        return False

if mode == 1:
    build_dfa(dfadata)

print_dfa(dfa, final)

for str in line_list:
    match = process(str)
    print(match, str)

