import re
import sys

myRegexLst = [
r"(?=.*a)(?=.*e)(?=.*i)(?=.*o)(?=.*u)",
r"[^aeiou]*[aeiou][^aeiou]*[aeiou][^aeiou]*[aeiou][^aeiou]*[aeiou][^aeiou]*[aeiou][^aeiou]*$",
r"^a[^a]*a$|^b[^b]*b$|^c[^c]*c$|^d[^d]*d$|^e[^e]*e$|^f[^f]*f$|^g[^g]*g$|^h[^h]*h$|^i[^i]*i$|^j[^j]*j$|^k[^k]*k$|^l[^l]*l$|^m[^m]*m$|^n[^n]*n$|^o[^o]*o$|^p[^p]*p$|^q[^q]*q$|^r[^r]*r$|^s[^s]*s$|^t[^t]*t$|^u[^u]*u$|^v[^v]*v$|^w[^w]*w$|^x[^x]*x$|^y[^y]*y$|^z[^z]*z$", #wrong
r"^(\w)(\w)(\w).*\3\2\1$|^(\w)\w\4$|^(\w)(\w)\6\5$|^(\w)(\w)\w\8\7$",
r"[^bt]*bt[^bt]*$|^[^bt]*tb[^bt]*$",
r".*(.)\1\1*.*",
r"^.*(\w)(.*\1){2}(.*\1)+.*$",
r"^(?:(\w)\1(?:(?!\1)\w\1)*)+$",
r"^[aeiou]*([^aeiou][aeiou]*){3}([^aeiou][aeiou]*)+$",
r"^([^a]*a[^a]*){3,}$|^([^b]*b[^b]*){3,}$|^([^c]*c[^c]*){3,}$|^([^d]*d[^d]*){3,}$|^([^e]*e[^e]*){3,}$|^([^f]*f[^f]*){3,}$|^([^g]*g[^g]*){3,}$|^([^h]*h[^h]*){3,}$|^([^i]*i[^i]*){3,}$|^([^j]*j[^j]*){3,}$|^([^k]*k[^k]*){3,}$|^([^l]*l[^l]*){3,}$|^([^m]*m[^m]*){3,}$|^([^n]*n[^n]*){3,}$|^([^o]*o[^o]*){3,}$|^([^p]*p[^p]*){3,}$|^([^q]*q[^q]*){3,}$|^([^r]*r[^r]*){3,}$|^([^s]*s[^s]*){3,}$|^([^t]*t[^t]*){3,}$|^([^u]*u[^u]*){3,}$|^([^v]*v[^v]*){3,}$|^([^w]*w[^w]*){3,}$|^([^x]*x[^x]*){3,}$|^([^y]*y[^y]*){3,}$|^([^z]*z[^z]*){3,}$"
]

minlen = 1000000
maxlen = 0

def word_match(wlist):
    global minlen, maxlen
   
    for i in range(10):
        print()
        print()
        minlen = 1000000
        maxlen = 0
        exp = re.compile(myRegexLst[i])
        count = 0
        matches = 0
        matchlist = []
        repeatlen = 0
        
        for word in wlist:
            word = word.lower()
            x = exp.match(word)

            if x:
                if (i < 5):
                    matches = matches + 1
                    matchlist.append(word)
                    if (minlen > len(word)):
                        minlen = len(word)
                    if (maxlen < len(word)):
                        maxlen = len(word)
                if i == 5:      #longest contiguous block of a single letter
                    exp1 = re.compile(r"(.)\1\1*")
                    tmp = 0
                    for result in exp1.finditer(word):
                        if (tmp<result.end() - result.start()):
                            tmp = result.end() - result.start()
                   #print("repeat", repeatlen, "tmp", tmp, word, result.start(), result.end())
                    if repeatlen == tmp:
                        matchlist.append(word)
                        matches = matches + 1
                    if repeatlen < tmp:
                        repeatlen = tmp
                        matchlist.clear()
                        matchlist.append(word)
                        matches = 1
                if i == 6:      #max appearance of same letter
                    exp1 = re.compile(r"([a-z])(.*\1){2}(.*\1)+")
                    tmp = 0
                    for result in exp1.finditer(word):
                        c = result[0][0]
                        s1 = word.replace(c,'')
                        if tmp < (len(word) - len(s1)):
                            tmp = len(word) - len(s1)
                    
                    if repeatlen == tmp:
                        matchlist.append(word)
                    if repeatlen < tmp:
                        repeatlen = tmp
                        matchlist.clear()
                        matchlist.append(word)   
                if i == 7:      #max appearance of pair
                    exp1 = re.compile(r"(?=(\w\w)\w*\1)")
                    tmp = 0
                    for result in exp1.finditer(word):
                        c = result[0][0:2]
                        s1 = word.replace(c,'')
                        if tmp < (len(word) - len(s1)):
                            tmp = len(word) - len(s1)
                    
                    if repeatlen == tmp:
                        matchlist.append(word)
                    if repeatlen < tmp:
                        repeatlen = tmp
                        matchlist.clear()
                        matchlist.append(word)
                if i == 8:      #max appearance consonants
                    s1 = word.replace('a','')
                    s1 = s1.replace('e','')
                    s1 = s1.replace('i','')
                    s1 = s1.replace('o','')
                    s1 = s1.replace('u','')
                    
                    if repeatlen == len(s1):
                        matchlist.append(word)
                    if repeatlen < len(s1):
                        repeatlen = len(s1)
                        matchlist.clear()
                        matchlist.append(word)
                #print (word)
            else: #for case 10
                if i == 9:      #max no repeat more than twice
                    matchlist.append(word)
                    if (minlen > len(word)):
                        minlen = len(word)
                    if (maxlen < len(word)):
                        maxlen = len(word)
            #     print("NO match", word)
        print("#"+str(i+1), myRegexLst[i])
        # print("min", minlen, "max", maxlen)

        if i < 3 or i==9:
            matchlist = process(matchlist, i+1)
        print(len(matchlist), "total matches")
        printcount = 0
        for word in matchlist:
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
    if n==2 or n==3 or n ==10:    #max len
        for word in wlist:
            if len(word) == maxlen:
                newlist.append(word)

    return newlist

filename = sys.argv[1]

with open(filename) as f:
    wlist = [line.strip() for line in f]

word_match(wlist)


