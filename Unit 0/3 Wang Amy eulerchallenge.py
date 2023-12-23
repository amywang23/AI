from operator import is_
import sys
from heapq import heappush, heappop, heapify, nsmallest, nlargest
from time import perf_counter

def is_prime(x):
    squareroot = x**(0.5)
    if x < 2:
        return "not anything"
    for elem in range(2,int(squareroot)+1):
        if(x % elem == 0):
            return False
    return True

start = perf_counter()

#1 print the sum of all the ints from 0 to 1000 that is divisible by 3 or 5
print(sum(i for i in range(0, 1000) if i % 3 == 0 or i % 5 == 0))

#2 print the sum of all even numbers up to 4000000
total = 0
current = 1
temp = 1
while current <= 4000000:
    if current % 2 == 0:
        total += current
    current, temp = temp, current + temp
print (total)

#3 loop until greatest common factor is found
factor = 2
greatest = 0
flag = False
number = 600851475143
while(flag == False):
    if(number % factor != 0):
        factor += 1
    else:
        greatest = number
        number = number / factor
        if(number == 1):
            print(greatest)
            flag = True

#4 checking for palindromes that exist between 100 and 999
result = 0
for elem in range(999, 100, -1):
    for element in range(999, 100, -1):
        product = elem* element
        if str(elem*element) == str(elem*element)[::-1]:
            if elem*element > result:
                result = elem*element
print(result)

#5 finding least common multiple
def gcd(a, b):
    while b != 0:
        t = b
        b = a % b
        a = t
    return a
lcm = 1
for elem in range(2, 20):
    lcm = elem*lcm/gcd(elem, lcm)
print(lcm)

#6 finding sum of all numbers 0-100 squared minus sum of all numbers squared between 0-100
print((sum((i for i in range(0, 101))))**2 - sum(i**2 for i in range(0, 101)))

#7 how many primes are there before 10000
number = 0
prime = 1
while number < 10001:
    prime += 1
    if is_prime(prime):
        number += 1
print(prime)

#8 largest product of 13 digits in a row in the string
num_string = "731671765313306249192251196744265747423553491949349698352031277450632623957831801698480186947885184385" +\
"861560789112949495459501737958331952853208805511125406987471585238630507156932909632952274430435576689" +\
"664895044524452316173185640309871112172238311362229893423380308135336276614282806444486645238749303589" +\
"072962904915604407723907138105158593079608667017242712188399879790879227492190169972088809377665727333" +\
"001053367881220235421809751254540594752243525849077116705560136048395864467063244157221553975369781797" +\
"784617406495514929086256932197846862248283972241375657056057490261407972968652414535100474821663704844" +\
"031998900088952434506585412275886668811642717147992444292823086346567481391912316282458617866458359124" +\
"566529476545682848912883142607690042242190226710556263211111093705442175069416589604080719840385096245" +\
"544436298123098787992724428490918884580156166097919133875499200524063689912560717606058861164671094050" +\
"7754100225698315520005593572972571636269561882670428252483600823257530420752963450"
temp=[]
finallist=[]
for i in num_string:
    temp.append(int(i))
for i in range(len(temp)-12):
    a=(temp[i])*(temp[i+1])*(temp[i+2])*(temp[i+3])*(temp[i+4])*(temp[i+5])*(temp[i+6])*(temp[i+7])*(temp[i+8])*(temp[i+9])*(temp[i+10])*(temp[i+11])*(temp[i+12])
    finallist.append(a)
print(max(finallist))

#9 find product of pythagorean triplet that sums up to 1000
total = 1000
for elem in range(1, int(total/3)):
    for element in range(elem+1, int(total/2)):
        side = total - elem - element
        if elem**2 + element**2 == side**2:
            print(elem*element*side)

#11 greatest product of 4 numbers
data = [[ 8,  2, 22, 97, 38, 15,  0, 40,  0, 75,  4,  5,  7, 78, 52, 12, 50, 77, 91,  8],
       [49, 49, 99, 40, 17, 81, 18, 57, 60, 87, 17, 40, 98, 43, 69, 48,  4, 56, 62,  0],
       [81, 49, 31, 73, 55, 79, 14, 29, 93, 71, 40, 67, 53, 88, 30,  3, 49, 13, 36, 65],
       [52, 70, 95, 23,  4, 60, 11, 42, 69, 24, 68, 56,  1, 32, 56, 71, 37,  2, 36, 91],
       [22, 31, 16, 71, 51, 67, 63, 89, 41, 92, 36, 54, 22, 40, 40, 28, 66, 33, 13, 80],
       [24, 47, 32, 60, 99,  3, 45,  2, 44, 75, 33, 53, 78, 36, 84, 20, 35, 17, 12, 50],
       [32, 98, 81, 28, 64, 23, 67, 10, 26, 38, 40, 67, 59, 54, 70, 66, 18, 38, 64, 70],
       [67, 26, 20, 68,  2, 62, 12, 20, 95, 63, 94, 39, 63,  8, 40, 91, 66, 49, 94, 21],
       [24, 55, 58,  5, 66, 73, 99, 26, 97, 17, 78, 78, 96, 83, 14, 88, 34, 89, 63, 72],
       [21, 36, 23,  9, 75,  0, 76, 44, 20, 45, 35, 14,  0, 61, 33, 97, 34, 31, 33, 95],
       [78, 17, 53, 28, 22, 75, 31, 67, 15, 94,  3, 80,  4, 62, 16, 14,  9, 53, 56, 92],
       [16, 39,  5, 42, 96, 35, 31, 47, 55, 58, 88, 24,  0, 17, 54, 24, 36, 29, 85, 57],
       [86, 56,  0, 48, 35, 71, 89,  7,  5, 44, 44, 37, 44, 60, 21, 58, 51, 54, 17, 58],
       [19, 80, 81, 68,  5, 94, 47, 69, 28, 73, 92, 13, 86, 52, 17, 77,  4, 89, 55, 40],
       [ 4, 52,  8, 83, 97, 35, 99, 16,  7, 97, 57, 32, 16, 26, 26, 79, 33, 27, 98, 66],
       [88, 36, 68, 87, 57, 62, 20, 72,  3, 46, 33, 67, 46, 55, 12, 32, 63, 93, 53, 69],
       [ 4, 42, 16, 73, 38, 25, 39, 11, 24, 94, 72, 18,  8, 46, 29, 32, 40, 62, 76, 36],
       [20, 69, 36, 41, 72, 30, 23, 88, 34, 62, 99, 69, 82, 67, 59, 85, 74,  4, 36, 16],
       [20, 73, 35, 29, 78, 31, 90,  1, 74, 31, 49, 71, 48, 86, 81, 16, 23, 57,  5, 54],
       [ 1, 70, 54, 71, 83, 51, 54, 69, 16, 92, 33, 48, 61, 43, 52,  1, 89, 19, 67, 48]]

final = [0, 0, 0, 0]
for elem in range(0,20):
    for temp in range(0,17):
        h = data[elem][temp]*data[elem][temp + 1]*data[elem][temp + 2]*data[elem][temp + 3]
        if h > final[0]:
            final[0] = h
        v = data[temp][elem]*data[temp + 1][elem]*data[temp + 2][elem]*data[temp + 3][elem]
        if v > final[1]:
            final[1] = v
for element in range(0,17):
    for temp1 in range (0,17):
        r = data[temp1][element]*data[temp1 + 1][element + 1]*data[temp1 + 2][element + 2]*data[temp1 + 3][element + 3]
        if r > final[2]:
            final[2] = r
        l = data[temp1][element + 3]*data[temp1 + 1][element + 2]*data[temp1 + 2][element + 1]*data[temp1 + 3][element]
        if l > final[3]:
            final[3] = l
print(max(final))

#18 find max 
data = [[75],

       [95, 64],

       [17, 47, 82],

       [18, 35, 87, 10],

       [20,  4, 82, 47, 65],

       [19,  1, 23, 75,  3, 34],

       [88,  2, 77, 73,  7, 63, 67],

       [99, 65,  4, 28,  6, 16, 70, 92],

       [41, 41, 26, 56, 83, 40, 80, 70, 33],

       [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],

       [53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14],

       [70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57],

       [91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48],

       [63, 66,  4, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31],

       [ 4, 62, 98, 27, 23,  9, 70, 98, 73, 93, 38, 53, 60,  4, 23]]

def maxRecur(data, x, y, row, col):
    if(y >= col):
         return 0
    elif(x >= row-1 ):
         return data[x][y]
    temp = max(maxRecur(data, x + 1, y, row, col), maxRecur(data, x + 1, y + 1, row, col))
    return data[x][y] + temp

print(maxRecur(data, 0, 0, 15, 15))

#24
def factorial(x):
    number = 1
    if x <= 1:
        return 1
    else:
        for elem in range(1, x+1):
            number = number*elem
    return(number)

counter = 0
result = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for i in range(factorial(10)):   
    counter += 1
    if counter == 1000000:
        print(''.join([str(x) for x in result]))
        break
    temp=len(result)-1
    while (temp > 0) and (result[temp-1] > result[temp]):        
        temp=temp-1
    result[temp:] = reversed(result[temp:]) 
    if temp > 0: 
        temp1 = temp 
        while result[temp-1] > result[temp1]:   
            temp1=temp1+1
    result[temp-1],result[temp1]=result[temp1],result[temp-1]

#28
sum = 1
temp = 1

for elem in range(2, 1001, 2):
    for element in range(4):   
        temp += elem
        sum += temp
print (sum)

#29
#length of list turned set of nested for loop a is first loop, b is second loop do a**b everytime
print(len({*[a**b for a in range(2, 101) for b in range(2, 101)]}))

end = perf_counter()
print("Total time:", end - start)