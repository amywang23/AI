import sys
import re

args = sys.argv[1:]

idx = int(args[0])-50

myRegexLst = [
r"^[a-z]*?([a-z])[a-z]*?\1[a-z]*?$",  
              #r"^\w*?(\w{1})\w*?\1\w*?$", #50
r"^[a-z]*?([a-z])[a-z]*?\1[a-z]*?\1[a-z]*?\1[a-z]*?$",
r"^0[01]*0$|^1[01]*1$",
r"^cat[a-z]{3}$|^[a-z]cat[a-z]{2}$|[a-z]{2}^cat[a-z]{1}$|^[a-z]{3}cat$",
r"^bring$|^(?=[a-z]{5,9}$)[a-z]*bri[a-z]*ing[a-z]*$|^(?=[a-z]{5,9}$)[a-z]*ing[a-z]*bri[a-z]*$",
r"^(?=[a-z]{6}$)(?!.*cat).*$",
r"^(?:([a-z])(?!.*\1))*$",   #^(?!.*(.).*\1)[a-z]+$
r"^(?!.*10011)[01]*$", #r"^(?=[01]*$)(?!.*10011).*$",
r"",
r"^(?!.*101)(?!.*111)[01]*$"
]



if idx < len(myRegexLst):
    print(myRegexLst[idx])

txt50 = "beanbeb"
txt51 = "abcaabea" #"beanbeabab"
txt52 = '01010110110100101010'
txt53 = 'acatho'
txt54 = "bring"
txt55 = "abcatd"
txt56 = "abcdefga"
txt57 = "00011110011000"
txt58 = "bbbcabacca"
txt59 = "000110011000"


txt = txt51
x = re.search(myRegexLst[idx], txt)

if x:
  print("YES! We have a match!")
else:
  print("No match")

exp = re.compile(myRegexLst[idx])
#print("result", exp.finditer(txt))
count = 0
for result in exp.finditer(txt):
  print("count", count, result[0])
  count = count +1

