import re
import sys
from colorama import init, Back, Fore  

init()
s = "While inside they wined and dined, safe from the howling wind.\nAnd she whined, it seemed, for the 100th time, into the ear of her friend,\nWhy indeed should I wind the clocks up, if they all run down in the end?"
s1 = ''
options = ''

#print(s)//
arg = sys.argv[1]
print(arg)
starting = arg.find("/", 1)
print(starting)
if starting+1 < len(arg):
    options = arg[starting+1]
print(options)
arg = arg[1:starting]
print(arg)
exp = re.compile(arg)

if options == "i":
    exp = re.compile(arg, re.I)
if options == "m":
    exp = re.compile(arg, re.M)
if options == "s":
    exp = re.compile(arg, re.S)

if len(options) ==2 and options.index("i")>0 and options.index("m")>0:
    exp = re.compile(arg, re.I|re.M)
if len(options) ==2 and options.index("i")>0 and options.index("s")>0:
    exp = re.compile(arg, re.I|re.S)
if len(options) ==2 and options.index("s")>0 and options.index("m")>0:
    exp = re.compile(arg, re.S|re.M)
    
if options.index("i")>0 and options.index("m")>0 and options.index("s")>0:
    exp = re.compile(arg, re.I|re.M|re.S)

# exp = re.compile(arg)
    
prevend = 0
for result in exp.finditer(s):
    #print("preend", prevend, "start", result.start())
    if (prevend==result.start()):
        s1 = s1 + s[prevend:result.start()]+ Back.LIGHTCYAN_EX + result[0]+ Back.RESET
    else:
        s1 = s1 + s[prevend:result.start()]+ Back.LIGHTYELLOW_EX + result[0]+ Back.RESET
    prevend = result.end()
    #print("preend", prevend)
s1 = s1 + s[prevend:]
print (s1)
# exp3 = re.compile(r"..l", re.I | re.S | re.M)
