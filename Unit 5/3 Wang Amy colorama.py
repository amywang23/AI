import re
import sys
from colorama import init, Back, Fore  

init()
s = "While inside they wined and dined, safe from the howling wind.\nAnd she whined, it seemed, for the 100th time, into the ear of her friend,\nWhy indeed should I wind the clocks up, if they all run down in the end?"
s1 = ''
options = ''

#print(s)//
arg = sys.argv[1]
# print(arg)
starting = arg.find("/", 1)
# print(starting)
if starting+1 < len(arg):
    options = arg[starting+1:len(arg)-1]
# print(options)
arg = arg[1:starting]
# print(arg)
if options == "":
    exp = re.compile(arg)
elif options == "i":
    exp = re.compile(arg, re.I)
elif options == "m":
    exp = re.compile(arg, re.M)
elif options == "s":
    exp = re.compile(arg, re.S)
elif len(options) ==2 and options.find("i")>0 and options.find("m")>0:
    exp = re.compile(arg, re.I|re.M)
elif len(options) ==2 and options.find("i")>0 and options.find("s")>0:
    exp = re.compile(arg, re.I|re.S)
elif len(options) ==2 and options.find("s")>0 and options.find("m")>0:
    exp = re.compile(arg, re.S|re.M)
else:   
# elif options.find("i")>0 and options.find("m")>0 and options.find("s")>0:
    exp = re.compile(arg, re.I|re.M|re.S)

# exp = re.compile(arg)
    
prevend = 0 #colors different color even though they are separated ?
for result in exp.finditer(s):
    #print("preend", prevend, "start", result.start())
    if (prevend!=0 and prevend==result.start()):
        s1 = s1 + s[prevend:result.start()]+ Back.LIGHTCYAN_EX + result[0]+ Back.RESET
    else:
        s1 = s1 + s[prevend:result.start()]+ Back.LIGHTYELLOW_EX + result[0]+ Back.RESET
    prevend = result.end()
    #print("preend", prevend)
s1 = s1 + s[prevend:]
print (s1)
# exp3 = re.compile(r"..l", re.I | re.S | re.M)
