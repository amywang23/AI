import re
import sys

myRegexLst = [
r"(?=.*a)(?=.*e)(?=.*i)(?=.*o)(?=.*u)",
r"^[^aeiou]*[aeiou][^aeiou]*[aeiou][^aeiou]*[aeiou][^aeiou]*[aeiou][^aeiou]*[aeiou][^aeiou]*$",
r"^([a-z])\1*?\1$",
r"^([a-z])([a-z])([a-z]).*\3\2\1$|^([a-z])[a-z]\4$|^([a-z])([a-z])\6\5$|^([a-z])([a-z])[a-z]\8\7$",
r"^[^bt]*bt[^bt]*$|^[^bt]*tb[^bt]*$"
#r"^[a-z]*?([a-z])[a-z]*?\1[a-z]*?\1[a-z]*?\1[a-z]*?$",
]

minlen = 1000000
maxlen = 0

def word_match(wlist):
    global minlen, maxlen
   
    for i in range(5):
        print()
        print()
        minlen = 1000000
        maxlen = 0
        exp = re.compile(myRegexLst[i])
        count = 0
        matches = 0
        matchlist = []
        for word in wlist:
            if count < 500000:
                count = count +1
            else:
                break
            x = exp.match(word.lower())

            if x:
                matches = matches + 1
                matchlist.append(word)
                if (minlen > len(word)):
                    minlen = len(word)
                if (maxlen < len(word)):
                    maxlen = len(word)
                #print (word)
            # else:
            #     print("NO match", word)
        print("#"+str(i+1), myRegexLst[i])
        print(matches, "total matches")
        print("min", minlen, "max", maxlen)

        if i < 3:
            processedlist = process(matchlist, i+1)
        else:
            processedlist = matchlist
        printcount = 0
        for word in processedlist:
            if printcount > 4:
                break
            print(word)
            printcount = printcount+1
    return
    
def process(wlist, n):
    newlist = []
    if (n == 1):    #min len
        for word in wlist:
            if len(word) == minlen:
                newlist.append(word)
    if n==2 or n==3:    #max len
        for word in wlist:
            if len(word) == maxlen:
                newlist.append(word)

    return newlist

filename = sys.argv[1]

with open(filename) as f:
    wlist = [line.strip() for line in f]

word_match(wlist)


