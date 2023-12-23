from math import log
from collections import defaultdict
import matplotlib.pyplot as plt
import random
import sys

question_number = 0
questions = []
caselist = []
casedict = defaultdict(list)
final_decisions = []
question_answers_set_list=[]
traindata = []
testdata = []
accuracylist = []
statslist = []
classificationlist = []

size_test = 50
size_train_min = 5
size_train_max = 300
size_step = 1

def build_data(line_list):
    global caselist, questions, question_number, final_decisions

    for idx, line in enumerate(line_list):
        currentline = line_list[idx].split(",")
        if (idx == 0):
            questions = currentline
            question_number = len(questions)
            for i in range(question_number):
                question_answers_set_list.append(set())
                statslist.append(defaultdict())
            # print("question #", question_number, questions)
        else:
            if not '?' in line_list[idx]:
                cl = currentline.copy()
                cl.pop()
                classificationlist.append(",".join(cl))
                #print(classificationlist)
            dict = defaultdict()
            for i in range(question_number):    #discard first element
                dict[questions[i]] = currentline[i]
                question_answers_set_list[i].add(currentline[i])
                if i != question_number-1 and currentline[i] != "?":
                    key = currentline[-1]+"-"+currentline[i]
                    if key in statslist[i]:
                        statslist[i][key] += 1
                    else:
                        statslist[i][key] = 1
            
            caselist.append(dict)
    final_decisions = list(sorted(question_answers_set_list[question_number-1]))       

    # print(questions)
    # print(final_decisions)
    # print(len(caselist))
    #print(statslist)
    return caselist

def clean_data(datalist):
    cleaned = []
    for d in datalist:
        vals = d.values()
        if not "?" in vals:
            cleaned.append(d)
    return cleaned

def create_train_data(datalist):

    random.shuffle(datalist)
    return datalist[:len(datalist)-size_test], datalist[len(datalist)-size_test:]

def guess_data(datalist):

    count = 0
    dupcount = 0
    for d in datalist:
        count += 1
        vals = d.values()
        if "?" in vals:
            l = []
            for i in range(question_number-1):
                if d[questions[i]] == "?":
                    statd = statslist[i]
                    maxa = 0
                    maxkey = ""
                    for key in statd:
                        vector_answer = d[questions[question_number-1]]
                        if vector_answer in key:   #check this vector's final answer
                            if (maxa < statd[key]):
                                maxa = statd[key]
                                maxkey = key
                    #print("row", count, "i", i, "vector answer", vector_answer, "maxa", maxa, "key", maxkey)
                    # print(statslist[i])
                    replace_answer = maxkey[maxkey.index("-")+1:]
                    #print(replace_answer)
                    d[questions[i]] = replace_answer
                    l.append(replace_answer)
                else:
                    l.append(d[questions[i]])
            #print(l)

            #check if it's a dup
            if ','.join(l) in classificationlist:
                #print("this is dup", d)
                d[questions[question_number-1]] = "dup"   #mark this as a dup
                dupcount += 1
    #remove all dups
    newlist =  [ elem for i,elem in enumerate(datalist) if elem[questions[question_number-1]] != "dup" ]

    # print("input len", len(datalist), "after removed dup", len(newlist), "total dups", dupcount)
    return newlist

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

def entropy(datalist): 
    result = 0

    if len(datalist) == 0:
        return 0

    totalnum = len(datalist)
    answernums = [0] * len(final_decisions) #number of outcome of result 
    q = questions[question_number-1]
    for i in range(len(datalist)):
        for j in range(len(final_decisions)):
            if (datalist[i][q] == final_decisions[j]):
                answernums[j] += 1
    #print("totalnum", totalnum, "answers", answernums)
    if totalnum in answernums:  # all of them has the same outcome
        return 0
    sum = 0.0
    for i in range(len(final_decisions)):
        #print("i", i, "answeri", answernums[i])
        if (answernums[i] != 0 ):
            sum += (answernums[i]/totalnum)*log(answernums[i]/totalnum, 2)
    sum = sum * (-1.0)
    
    return sum

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


def generate_tree(datalist, parent, depth):
    #print("depth", depth, "----------------------------------------------------")

    #first process parent and add values
    parent["depth"] = depth
    parent["type"] = "answer"
    original = entropy(datalist)
    if (depth == 0):
        parent["description"] = "Starting Entropy: " + str(original)
        parent["value"] = ""
        if original == 0:   # initial list has just one outcome
            parent["description"] += " --> " + datalist[0][questions[question_number-1]]
            parent["value"] = datalist[0][questions[question_number-1]]
            # ***print("\n\n!!!!!!!!!!!!!!!!!!!!IMPORTANT: INITIAL SET HAS JUST ONE OUTCOME")
            return
    else:
        if original == 0:   #only one outcome so it's a leaf
            parent["description"] += " --> " + datalist[0][questions[question_number-1]]
            return
        else:
            parent["description"] += " (with current entropy " + str(original) + ")"

    #find a question with max gain
    maxset = find_max_gain(datalist, original)
    maxquestion = maxset[0]
    maxgain = maxset[1]
  
    #print("depth", depth, "maxquestion is", questions[maxquestion])
    subdatalist = split_dataset(datalist, maxquestion)
    #print(len(subdatalist), len(subdatalist[0]), len(subdatalist[1]), len(subdatalist[2]))
   
    #create a node for the question
    node = defaultdict(list)
    node["description"] = questions[maxquestion] + "? (information gain: " + str(maxgain) + ")"
    node["value"] = questions[maxquestion]
    node["depth"] = depth+1
    node["type"] = "question"
    parent["children"].append(node)

    #create nodes for answers
    for sub in subdatalist:
        if len(sub) == 0:
            continue
        child = defaultdict(list)
        child["description"] = sub[0][questions[maxquestion]]
        child["value"] = sub[0][questions[maxquestion]]
        child["depth"] = depth+2
        child["type"] = "answer"
        node["children"].append(child)
        generate_tree(sub, child, depth+2)

    return

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

def print_tree(node):
    spaces = " " * (2*node["depth"])
    print(spaces,"*", node["description"])

    for child in node["children"]:
        print_tree(child)

    return

def print_data(datalist):

    print(" ".join(questions))
    for d in datalist:
        for q in questions:
            print(" "+d[q], end =" ")
        print()

    return

def build_learning_curve(datalist):
    
    for SIZE in range(size_train_min, size_train_max+1, size_step):
        TRAIN = random.sample(datalist, SIZE)   #deal with duplicate vector
        root = defaultdict(list)
        generate_tree(TRAIN, root, 0)
        # ***print("\nSIZE", SIZE, "-------------------------")
        # ***print_tree(root)
        #print_data(TRAIN)

        correctnum = 0
        for i in range(len(testdata)):
            #print(testdata[i])
            result = traverse_tree(root, testdata[i])
            #print(result, testdata[i][questions[question_number-1]])
            if result == testdata[i][questions[question_number-1]]:
                correctnum += 1
        accuracylist.append((SIZE, correctnum/len(testdata)))

    #print(accuracylist)

    return accuracylist

def traverse_tree(root, vector):

    count = 0
    result = ""
    current = root
    while True:
        count += 1
        # if count > 20:
        #     break
        #print(count, current["description"])
        if not "children" in current or len(current["children"]) == 0:
            description = current["description"]
            idx = description.index("--> ")
            if idx > 0:
                result = description[idx+4:]
                break
        else:
            children = current["children"]
            if len(children) == 1 and children[0]["type"] == "question":
                question = children[0]["value"]
                answer = vector[question]
                grandchildren = children[0]["children"]
                #print("only one child question", question, "answer", answer, "# grand", len(grandchildren))
                current = grandchildren[0]
                for c in grandchildren:
                    if answer == c["value"]:
                        current = c
                        break

    return result

def plot(accuracy):

    xlist = []
    ylist = []
    for a in accuracy:
        xlist.append(a[0])
        ylist.append(a[1])

    # print(xlist)
    # print(ylist)
    
    plt.scatter(xlist, ylist)
    plt.show()
    return

#python training.py nursery.csv 500 500 12000 500
#python training.py connect-four.csv 7000 5000 60000 5000
filename = sys.argv[1]
size_test = int(sys.argv[2])
size_train_min = int(sys.argv[3])
size_train_max = int(sys.argv[4])
size_step = int(sys.argv[5])


with open(filename) as f:
    line_list = [line.strip() for line in f]

build_data(line_list)
#print(len(caselist))

#make a guess
#caselist = guess_data(caselist)
#print(caselist)
# print("data size before processing", len(caselist))

#remove all rows with ?
#caselist = clean_data(caselist)
#print(len(caselist))

#remove last 50 rows
dlist = create_train_data(caselist)
traindata = dlist[0]
testdata = dlist[1]
# print("train data size", len(traindata))

accuracylist = build_learning_curve(traindata)
# print(accuracylist)
plot(accuracylist)


