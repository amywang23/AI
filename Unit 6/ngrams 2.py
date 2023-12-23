import sys
import random
from math import log
from collections import defaultdict
from random import randrange
from time import perf_counter



dict = defaultdict(list)
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

n =  3    #n gram
POPULATION_SIZE = 500
NUM_CLONES = 1
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = .75
CROSSOVER_LOCATIONS = 5
MUTATION_RATE = .8

population = set()
next_generation = set()
population_score = defaultdict(list)
all_score = defaultdict(list)

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
    for i in range(1):
        random.shuffle(alp)
        result = ''.join(alp)
    return result

def generate_first_population():
    global population

    population = set()
    while True:
        alp = random_alphbet()
        population.add(alp)
        if len(population) >= POPULATION_SIZE:
            break

    return population

def generate_population_score(word):
    global population, population_score, mapping, all_score

    population_score = defaultdict(list)
    for alp in population:
        if alp in all_score:
            population_score[alp] = all_score[alp]
        else:
            mapping = alp
            nword = en_decode(word, 2)
            score = fitness_score(nword, 3)
            population_score[alp] = score
            all_score[alp] = score

    return population_score

def selection(sorted_score):
    global population, next_generation,population_score
    
    selected = random.sample(sorted_score, TOURNAMENT_SIZE*2)
    #print(selected) 

    tlist = []
    tlist.append(sorted(selected[:TOURNAMENT_SIZE], key=lambda x:x[1], reverse=True))
    tlist.append(sorted(selected[TOURNAMENT_SIZE:], key=lambda x:x[1], reverse=True))
    #print(tlist[0])
    #print("----------------------------------------")
    #print(tlist[1])
    #print()

    parent = ['','']
    for i in range(2):
      for j in range(TOURNAMENT_SIZE):
        if random.random() < TOURNAMENT_WIN_PROBABILITY: 
            parent[i] = tlist[i][j][0]
            #print(i, j)
            break
    return parent

def breeding(p1, p2):
    idx = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    child =  "." * 26

    selected = random.sample(idx, CROSSOVER_LOCATIONS)
    #print("selected", selected)
    for i in range (CROSSOVER_LOCATIONS):
        j = selected[i]
        child = child[:j] + p1[j] + child[j+1:]
    #print(p1, p2)
    #print("child", child)


    for i in range (26):
        if not p2[i] in child:
            j = child.index(".")
            child = child[:j] + p2[i] + child[j+1:]
            #print(i, p2[i], child)

    return child

def mutation(child):
   
    idx = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    pair = sorted(random.sample(idx, 2))
    mutated = child[:pair[0]] + child[pair[1]] + child[pair[0]+1:pair[1]] + child[pair[0]] + child[pair[1]+1:]

    #print ("mute", mutated)
    return mutated

def runit(word):
    global population, population_score, mapping
 
    nword = ''
    maxscore = 0
    maxmapping =''
    
    sorted_score = []
    population = generate_first_population()
    for j in range(500):
        population_score = generate_population_score(word)
        #print(population_score)
        sorted_score = sorted(population_score.items(), key=lambda x:x[1], reverse=True)
        #print(sorted_score)

        if (maxscore < sorted_score[0][1]):
            maxscore = sorted_score[0][1]
            maxmapping = sorted_score[0][0]
            print("updated maxscore to", maxscore, maxmapping)
            
        next_generation = set()
        for i in range(NUM_CLONES):
            next_generation.add(sorted_score[i][0])
            #print(sorted_score[i][0], population_score[sorted_score[i][0]])

        while True:
            p = selection(sorted_score)     #pair of parents
            child = breeding(p[0], p[1])
            child = mutation(child)
            next_generation.add(child)
            if len(next_generation) >= POPULATION_SIZE:
                break

        #next generation score
        #print(next_generation)
        #print("next generation size:", len(next_generation))
        population = next_generation
        
        print("#",j,"-----------------------------------------\n")

    print(maxscore, maxmapping)
    mapping = maxmapping
    nword = en_decode(word, 2)
    print(nword)
    return nword

shortstr = "XMTP CGPQR BWEKNJB GQ OTGRB EL BEQX BWEKNJB, G RFGLI. GR GQ BEQX ABSETQB RFGQ QBLRBLSB TQBQ EJJ RBL KMQR SMKKML VMPYQ GL BLDJGQF: 'G FEUB RM AB E DMMY QRTYBLR GL RFER SJEQQ GL RFB PMMK MC RFER RBESFBP."
longstr = """PF HACYHTTRQ VF N PBYYRPGVBA BS SERR YRNEAVAT NPGVIVGVRF GUNG GRNPU PBZCHGRE FPVRAPR GUEBHTU RATNTVAT
TNZRF NAQ CHMMYRF GUNG HFR PNEQF, FGEVAT, PENLBAF NAQ YBGF BS EHAAVAT NEBHAQ. JR BEVTVANYYL QRIRYBCRQ
GUVF FB GUNG LBHAT FGHQRAGF PBHYQ QVIR URNQ-SVEFG VAGB PBZCHGRE FPVRAPR, RKCREVRAPVAT GUR XVAQF BS
DHRFGVBAF NAQ PUNYYRATRF GUNG PBZCHGRE FPVRAGVFGF RKCREVRAPR, OHG JVGUBHG UNIVAT GB YRNEA CEBTENZZVAT
SVEFG. GUR PBYYRPGVBA JNF BEVTVANYYL VAGRAQRQ NF N ERFBHEPR SBE BHGERNPU NAQ RKGRAFVBA, OHG JVGU GUR
NQBCGVBA BS PBZCHGVAT NAQ PBZCHGNGVBANY GUVAXVAT VAGB ZNAL PYNFFEBBZF NEBHAQ GUR JBEYQ, VG VF ABJ JVQRYL
HFRQ SBE GRNPUVAT. GUR ZNGREVNY UNF ORRA HFRQ VA ZNAL PBAGRKGF BHGFVQR GUR PYNFFEBBZ NF JRYY, VAPYHQVAT
FPVRAPR FUBJF, GNYXF SBE FRAVBE PVGVMRAF, NAQ FCRPVNY RIRAGF. GUNAXF GB TRAREBHF FCBAFBEFUVCF JR UNIR
ORRA NOYR GB PERNGR NFFBPVNGRQ ERFBHEPRF FHPU NF GUR IVQRBF, JUVPU NER VAGRAQRQ GB URYC GRNPUREF FRR UBJ
GUR NPGVIVGVRF JBEX (CYRNFR QBA'G FUBJ GURZ GB LBHE PYNFFRF – YRG GURZ RKCREVRAPR GUR NPGVIVGVRF
GURZFRYIRF!). NYY BS GUR NPGVIVGVRF GUNG JR CEBIVQR NER BCRA FBHEPR – GURL NER ERYRNFRQ HAQRE N PERNGVIR
PBZZBAF NGGEVOHGVBA-FUNERNYVXR YVPRAPR, FB LBH PNA PBCL, FUNER NAQ ZBQVSL GUR ZNGREVNY. SBE NA
RKCYNANGVBA BA GUR PBAARPGVBAF ORGJRRA PF HACYHTTRQ NAQ PBZCHGNGVBANY GUVAXVAT FXVYYF, FRR BHE
PBZCHGNGVBANY GUVAXVAT NAQ PF HACYHTTRQ CNTR. GB IVRJ GUR GRNZ BS PBAGEVOHGBEF JUB JBEX BA GUVF
CEBWRPG, FRR BHE CRBCYR CNTR. SBE QRGNVYF BA UBJ GB PBAGNPG HF, FRR BHE PBAGNPG HF CNTR. SBE ZBER
VASBEZNGVBA NOBHG GUR CEVAPVCYRF ORUVAQ PF HACYHTTRQ, FRR BHE CEVAPVCYRF CNTR."""


word = sys.argv[1]
filename = "ngrams.txt"

with open(filename) as f:
    wlist = [line.strip() for line in f]

start = perf_counter()
word = shortstr
build_dict(wlist)
runit(word)

end = perf_counter()
print( "run time", end-start)
