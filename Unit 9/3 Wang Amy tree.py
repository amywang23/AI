from math import log
from collections import defaultdict
import sys

question_number = 0
questions = []
caselist = []
casedict = defaultdict(list)
final_decisions = []
question_answers_set_list=[]

filename = sys.argv[1]
with open(filename) as f:
    line_list = [line.strip() for line in f]
    
outputfile = open('treeout.txt', 'w')

def build_data(line_list):
    global caselist, questions, question_number, final_decisions

    for idx, line in enumerate(line_list):
        currentline = line_list[idx].split(",")
        if (idx == 0):
            questions = currentline
            question_number = len(questions)
            for i in range(question_number):
                question_answers_set_list.append(set())
        else:
            dict = defaultdict()
            for i in range(question_number):
                dict[questions[i]]=currentline[i]
                question_answers_set_list[i].add(currentline[i])
            
            caselist.append(dict)
    final_decisions = list(sorted(question_answers_set_list[question_number-1]))       

    return caselist

def extended_entropy(datalist, question):
    if len(datalist) == 0:
        return 0

    qidx = questions.index(question)
    subdatalist = split_dataset(datalist, qidx)

    sum = 0.0
    for i in range(len(question_answers_set_list[qidx])):
        #print("extended_entropy", i, len(subdatalist[i]), entropy(subdatalist[i]))
        sum += len(subdatalist[i])/len(datalist)*entropy(subdatalist[i])

    return sum

#the spread
def entropy(datalist):
    result = 0

    if len(datalist) == 0:
        return 0

    totalnum = len(datalist)
    r0 = 0      #number of outcome of result 
    q = questions[question_number-1]
    for i in range(len(datalist)):
        if (datalist[i][q] == final_decisions[0]):
            r0 += 1
    
    if r0 == 0 or r0 == totalnum:
        return 0
    result = (-1.0) * ((r0/totalnum)*log(r0/totalnum, 2) + (((totalnum-r0)/totalnum)*log((totalnum-r0)/totalnum, 2)))

    return result

#split dataset into smaller sets
def split_dataset(datalist, qnum):

    question = questions[qnum]
    n = len(question_answers_set_list[qnum])
    answerlist = list(sorted(question_answers_set_list[qnum]))
    #print("answerlist", answerlist)
    
    subdatalist = []
    for i in range(n):
        subdatalist.append([])
    for i in range(len(datalist)):
        for j in range(n):
            if datalist[i][question] == answerlist[j]:
                subdatalist[j].append(datalist[i])
                #print("i", i, "j", j, len(subdatalist[j]))

    return subdatalist

#create the tree while in consideration of 
def generate_tree(datalist, parent, depth):
    #print("depth", depth, "----------------------------------------------------")
    #first process parent and add values
    parent["depth"] = depth
    parent["type"] = "answer"
    original = entropy(datalist)
    if (depth == 0):
        parent["value"] = "Starting Entropy: " + str(original)
    else:
        if original == 0:   #only one outcome so it's a leaf
            parent["value"] += " --> " + datalist[0][questions[question_number-1]]
            return
        else:
            parent["value"] += " (with current entropy " + str(original) + ")"

    #find a question with max gain
    maxset = find_max_gain(datalist, original)
    maxquestion = maxset[0]
    maxgain = maxset[1]
  
    #print("depth", depth, "maxquestion is", questions[maxquestion])
    subdatalist = split_dataset(datalist, maxquestion)
    #print(len(subdatalist), len(subdatalist[0]), len(subdatalist[1]), len(subdatalist[2]))
   
    #create a node for the question
    node = defaultdict(list)
    node["value"] = questions[maxquestion] + "? (information gain: " + str(maxgain) + ")"
    node["depth"] = depth+1
    node["type"] = "question"
    parent["children"].append(node)

    #create nodes for answers
    for sub in subdatalist:
        if len(sub) == 0:
            continue
        child = defaultdict(list)
        child["value"] = sub[0][questions[maxquestion]]
        child["depth"] = depth+2
        child["type"] = "answer"
        node["children"].append(child)
        generate_tree(sub, child, depth+2)

    return

#find the max amount of gain
def find_max_gain(datalist, original):

    maxgain = 0
    maxquestion = -1
    for i in range(question_number-1):
        gain = original - extended_entropy(datalist, questions[i])
        #print("find_max_gaini", i, questions[i], gain)
        if gain > maxgain:
            maxgain = gain
            maxquestion = i
    
    #print("find maxgain", maxgain, questions[maxquestion])

    return(maxquestion, maxgain)

#print the tree pretty
def print_tree(node):
    spaces = " " * (2*node["depth"])
    print(spaces,"*", node["value"], file=outputfile)

    for child in node["children"]:
        print_tree(child)

    return

build_data(line_list)
#print(caselist)
# print(final_decisions)
# print("original", entropy(caselist))
# print("extended with outlook", extended_entropy(caselist, "Outlook"))
# original = entropy(caselist)
# print(original-extended_entropy(caselist, "Outlook"))
# print(original-extended_entropy(caselist, "Temp"))
# print(original-extended_entropy(caselist, "Humidity"))
# print(original-extended_entropy(caselist, "Wind"))

root = defaultdict(list)
generate_tree(caselist, root, 0)
print_tree(root)