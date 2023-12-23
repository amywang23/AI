import sys

if sys.argv[1] == 'A':
    print(int(sys.argv[2]) + int(sys.argv[3]) + int(sys.argv[4]))

if sys.argv[1] == 'B':
    sum = 0
    for index, value in enumerate(sys.argv[2:]):
        sum += int(value)
    print(sum)

if sys.argv[1] == 'C':
    for index, value in enumerate(sys.argv[2:]):
        if int(value) % 3 == 0:
            print(int(value))

if sys.argv[1] == 'D':
    a = 0
    b = 1
    n = int(sys.argv[2])
    if n == 1:
        print(a)
    else:
        print(a)
        print(b)
    for i in range(2, int(n)):
        c = a + b
        a = b
        b = c
        print(a+b)

if sys.argv[1] == 'E':
    for i in range(int(sys.argv[2]), int(sys.argv[3])+1):
        print(int(i*i - 3*i + 2))

if sys.argv[1] == 'F':
    a = float(sys.argv[2])
    b = float(sys.argv[3])
    c = float(sys.argv[4])
    s = (a + b + c)/2.0
    if a+b >= c and b+c >= a and c+a >= b:
        print((s*(s-a)*(s-b)*(s-c))**0.5)
    else:
        print("Not a valid triangle!")

if sys.argv[1] == 'G':
    s = sys.argv[2]
    countA = s.count('A')
    countA += s.count('a')
    countE = s.count('E')
    countE += s.count('e')
    countI = s.count('I')
    countI += s.count('i')
    countO = s.count('O')
    countO += s.count('o')
    countU = s.count('U')
    countU += s.count('u')
    print('A', end = " ")
    print(countA)
    print('E', end = ' ')
    print(countE)
    print('I', end = ' ')
    print(countI)
    print('O', end = ' ')
    print(countO)
    print('U', end = ' ')
    print(countU)
    # print({x: sys.argv[2].lower().count(x) for x in "aeiou"})
