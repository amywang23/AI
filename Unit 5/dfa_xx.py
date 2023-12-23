import sys
from collections import defaultdict

dfalist = []

###### DFA 1 ################################## aab
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

###### DFA 2 ################################## end with 1
dfa2 = {
    0: {
        "0": 0,
        "1": 1,
        "2": 0
        },
    1: {
        "0": 0,
        "1": 1,
        "2": 0
        }
}

###### DFA 3 ################################## b somewhere
dfa3 = {
    0: {
        "a": 0,
        "b": 1,
        "c": 0
        },
    1: {
        "a": 1,
        "b": 1,
        "c": 1
        }
}

###### DFA 4 ##################################  even number of "0"s (including none
####at all) and any number of "1"s (including none at all)
dfa4 = {
    0: {
        "0": 1,
        "1": 0
        },
    1: {
        "0": 0,
        "1": 1
        }
}

###### DFA 5 ################################## even 0 and even 1
#error: when given a 2, it automatically goes to a trash node -> cannot get out of it -> will return false even with even 0's and 1's
dfa5 = {
   0: {
        "0": 1,
        "1": 2
        },
    1: {
        "0": 0,
        "1": 2
        },
    2: {
        "0":1,
        "1": 0
    }
}

###### DFA 6 ################################## no abc
#error: aabca matches but it shldn't
dfa6 = {
    0: {
        "a": 1,
        "b": 0,
        "c": 0
        },
    1: {
        "a": 0,
        "b": 2,
        "c": 0
        },
    2: {
        "a": 0,
        "b": 0
        }
}

###### DFA 7 ################################## 10 then 11
dfa7 = {
    0: {
        "0": 0,
        "1": 1,
        },
    1: {
        "0": 2,
        "1": 1,
        },
    2: {
        "0": 2,
        "1": 3, 
    },
    3: {
        "0": 2,
        "1": 4, 
    },
    4: {
        "0": 4,
        "1": 4, 
    }

}

letterslist = ['','ab','012','abc','01','01','abc','01']
statenumlist = [0,4,2,2,2,3,3,5]
finallist = [[],[3],[1],[1],[0],[0],[0,1,2],[4]]

mode = 1
arg1 = sys.argv[1]
n = 0
if len(arg1)==1 and arg1 in ("1","2","3","4","5","6","7"):
    mode = 2
    n = int(arg1)

dfafilename = arg1
stringfilename = sys.argv[2]
print("***************mode", mode)
if mode == 1:
    with open(dfafilename) as f:
        dfadata = f.read()

with open(stringfilename) as f:
    line_list = [line.strip() for line in f]

def build_dfa(data):
    global letterslist, statenumlist, finallist
    dfa0 = defaultdict(list)
    sections = data.split("\n\n")

    lines = sections[0].split("\n")
    letterslist[0] = lines[0]
    statenumlist[0] = int(lines[1])
    finallist[0] = lines[2].split(" ")
    finallist[0] = [int(i) for i in finallist[0]]

    print("letters", letterslist[0])
    print("statenum", statenumlist[0])
    print("final", finallist[0])

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
        dfa0[state] = dict
    
    return dfa0

def print_dfa(dfa, final, n):
    print("*",  end ="  ")
    for l in letterslist[n]:
        print(l, end="  ")
    print()

    for d in dfa:
        print(d, end ="  ")
        states = dfa[d]
        for l in letterslist[n]:
            if l in states:
                print(states[l],end ="  ")
            else:
                print("_",end ="  ")
        print()
    print("Final nodes:", final)
    return

def process(str, n):
    match = False
    state = 0

    for c in str:
        moves = dfa[state]
        if c in moves:
            state = moves[c]
        else:
            return False

    if state in finallist[n]:
        return True
    else:
        return False

dfa = defaultdict(list)
if mode == 1:
    dfalist.append(build_dfa(dfadata))
    dfa = dfalist[0]
else:
    dfalist.append({})
    dfalist.append(dfa1)
    dfalist.append(dfa2)
    dfalist.append(dfa3)
    dfalist.append(dfa4)
    dfalist.append(dfa5)
    dfalist.append(dfa6)
    dfalist.append(dfa7)
    
    dfa = dfalist[n]


print_dfa(dfa, finallist[n], n)

for str in line_list:
    match = process(str, n)
    print(match, str)

