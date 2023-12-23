import sys
import random
from math import log
from collections import defaultdict
from random import randrange

dict = defaultdict(list)
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
mapping = 'XRPHIWGSONFQDZEYVJKMATUCLB'
POPULATION_SIZE = 5

def en_decode(word, method):
    nword = ''
    
    #print("en_decode", mapping)
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

def build_dict(wlist):

    for line in wlist:
        strs = line.split(' ')
        dict[strs[0]] = int(strs[1])
    return

def fitness_score(word, n):
    score = 0
    
    for i in range(len(word)-n+1):
        s = word[i:i+n]
        s = ''.join([i for i in s if i.isalpha()])
        if (len(s) == n):
            if s in dict:
                score += log(dict[s],2)
    return score

def random_alphbet():
    result = ''
    alp = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    for i in range(3):
        random.shuffle(alp)
        result = ''.join(alp)
    return result

def hill_climbing(word, n):
    global mapping
    usedmappings = set()
    mapping = random_alphbet()
    print("hill clibming mapping initial", mapping)
    nword = en_decode(word, 2)
    print("hill climbing decoded initial", nword)

    prevscore = fitness_score(nword, n)
    print ("hill climbing score inital", prevscore)
    print()

    count = 0
    changecount = 0
    while True:
        count += 1
        prevmapping = mapping
        i1 = randrange(26)
        i2 = randrange(26)
        print("hill clibming count", count)
        if (i1 == i2):
            continue
        if (i1 > i2):
            tmp = i2
            i2 = i1
            i1 = tmp

        c1 = mapping[i1]
        c2 = mapping[i2]
        mapping = mapping[0:i1] + c2 + mapping[i1+1:i2] + c1 + mapping[i2+1:]
        print("hill clibming mapping count", count, "exchanged", i1, i2, mapping)
        if mapping in usedmappings:
            print("mapping used before")
            continue
        else:
            usedmappings.add(mapping)

        nword = en_decode(word, 2)
        print("hill climbing decoded=", nword)

        score = fitness_score(nword, n)
        print ("hill climbing score", score, "prev", prevscore)
        
        scorediff = abs(prevscore-score)
        if (score < prevscore):
            mapping = prevmapping
            print("mapping rolled back")
        else:
            prevscore = score
            changecount += 1

        print()

        if changecount > 5 and scorediff<10:
        #if nword[0:2] == "CS": #or scorediff<10:
            break
        
    return


#python ngrams.py 3 'SIQQE, KMAHIZMK!' 'XRPHIWGSONFQDZEYVJKMATUCLB'
shortstr = "XMTP CGPQR BWEKNJB GQ OTGRB EL BEQX BWEKNJB, G RFGLI. GR GQ BEQX ABSETQB RFGQ QBLRBLSB TQBQ EJJ RBL KMQR SMKKML VMPYQ GL BLDJGQF: 'G FEUB RM AB E DMMY QRTYBLR GL RFER SJEQQ GL RFB PMMK MC RFER RBESFBP."
#

longstr = """PF HACYHTTRQ VF N PBYYRPGVBA BS SERR YRNEAVAT NPGVIVGVRF GUNG
GRNPU PBZCHGRE FPVRAPR GUEBHTU RATNTVAT TNZRF NAQ CHMMYRF GUNG
HFR PNEQF, FGEVAT, PENLBAF NAQ YBGF BS EHAAVAT NEBHAQ. JR
BEVTVANYYL QRIRYBCRQ GUVF FB GUNG LBHAT FGHQRAGF PBHYQ QVIR URNQSVEFG VAGB PBZCHGRE FPVRAPR, RKCREVRAPVAT GUR XVAQF BS DHRFGVBAF
NAQ PUNYYRATRF GUNG PBZCHGRE FPVRAGVFGF RKCREVRAPR, OHG JVGUBHG
UNIVAT GB YRNEA CEBTENZZVAT SVEFG. GUR PBYYRPGVBA JNF BEVTVANYYL
VAGRAQRQ NF N ERFBHEPR SBE BHGERNPU NAQ RKGRAFVBA, OHG JVGU GUR
NQBCGVBA BS PBZCHGVAT NAQ PBZCHGNGVBANY GUVAXVAT VAGB ZNAL
PYNFFEBBZF NEBHAQ GUR JBEYQ, VG VF ABJ JVQRYL HFRQ SBE GRNPUVAT.
GUR ZNGREVNY UNF ORRA HFRQ VA ZNAL PBAGRKGF BHGFVQR GUR PYNFFEBBZ
NF JRYY, VAPYHQVAT FPVRAPR FUBJF, GNYXF SBE FRAVBE PVGVMRAF, NAQ
FCRPVNY RIRAGF. GUNAXF GB TRAREBHF FCBAFBEFUVCF JR UNIR ORRA
NOYR GB PERNGR NFFBPVNGRQ ERFBHEPRF FHPU NF GUR IVQRBF, JUVPU NER
VAGRAQRQ GB URYC GRNPUREF FRR UBJ GUR NPGVIVGVRF JBEX (CYRNFR
QBA’G FUBJ GURZ GB LBHE PYNFFRF – YRG GURZ RKCREVRAPR GUR
NPGVIVGVRF GURZFRYIRF!). NYY BS GUR NPGVIVGVRF GUNG JR CEBIVQR
NER BCRA FBHEPR – GURL NER ERYRNFRQ HAQRE N PERNGVIR PBZZBAF
NGGEVOHGVBA-FUNERNYVXR YVPRAPR, FB LBH PNA PBCL, FUNER NAQ ZBQVSL
GUR ZNGREVNY. SBE NA RKCYNANGVBA BA GUR PBAARPGVBAF ORGJRRA PF
HACYHTTRQ NAQ PBZCHGNGVBANY GUVAXVAT FXVYYF, FRR BHE
PBZCHGNGVBANY GUVAXVAT NAQ PF HACYHTTRQ CNTR. GB IVRJ GUR GRNZ
BS PBAGEVOHGBEF JUB JBEX BA GUVF CEBWRPG, FRR BHE CRBCYR CNTR.
SBE QRGNVYF BA UBJ GB PBAGNPG HF, FRR BHE PBAGNPG HF CNTR. SBE
ZBER VASBEZNGVBA NOBHG GUR CEVAPVCYRF ORUVAQ PF HACYHTTRQ, FRR
BHE CEVAPVCYRF CNTR."""

n = int(sys.argv[1])     #n gram
word = sys.argv[2]
mapping = sys.argv[3]

#nword = en_decode(word, method)
#print(nword)

word = longstr
filename = "ngrams.txt"

with open(filename) as f:
    wlist = [line.strip() for line in f]

build_dict(wlist)
# nword = en_decode(word, 2)
# print("fitness decoded=", nword)
score = fitness_score(word, n)
print("fitness", score)

word = longstr
hill_climbing(word, n)
