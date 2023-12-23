import re
import sys

myRegexLst = [r"^[a-z]*?([a-z])[a-z]*?\1[a-z]*?\1[a-z]*?\1[a-z]*?$",]

def word_match(wlist):
    for i in range(1):
        exp = re.compile(myRegexLst[i])
        count = 0
        matches = 0
        matchlist = []
        for word in wlist:
            if count < 5:
                count = count +1
            else:
                break
            x = exp.match(word)

            if x:
                matches = matches + 1
                matchlist.append(word)
            else:
                print("NO match", word)
        print("#"+str(i+1), myRegexLst[i])
        print(matches, "total matches")
        printcount = 0
        for word in matchlist:
            print(word)
            if printcount > 3:
                break
            printcount = printcount+1
    return
    

filename = sys.argv[1]

with open(filename) as f:
    wlist = [line.strip() for line in f]

word_match(wlist)


