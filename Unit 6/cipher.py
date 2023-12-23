import sys
from math import log

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
mapping = 'XRPHIWGSONFQDZEYVJKMATUCLB'


def en_decode(word, method):
    nword = ''
    
    if method == '1':
        fromlist = alphabet
        tolist = mapping
    else:
        tolist = alphabet
        fromlist = mapping

    word = word.upper()
    for i in range(len(word)):
        c = word[i]
        if (fromlist.find(c) != -1):
            index = fromlist.index(c)
            nword += tolist[index]
        else:
            nword += c

    return nword


#python cipher.py 1 hello
method = sys.argv[1]
word = sys.argv[2]

nword = en_decode(word, method)
print(nword)