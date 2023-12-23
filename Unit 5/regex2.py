import sys
import re

args = sys.argv[1:]

idx = int(args[0])-40

myRegexLst = [
r"^[ox\.]{64}$",
#r"^\.[ox]{7}$|^[ox]{1}\.[ox]{6}$|^[ox]{2}\.[ox]{5}$|^[ox]{3}\.[ox]{4}$|^[ox]{4}\.[ox]{3}$|^[ox]{5}\.[ox]{2}$|^[ox]{6}\.[ox]{1}$|^[ox]{7}\.$",
#r"^(?=\S{8}(?!\S))[ox]*\.[ox]*$",  #this works
r"^(?=[ox.]{8}$)[ox]*\.[ox]*$",

# position is followed by exactly 10 non-whitespace characters
#r"^(?=\S{8}(?!\S))x*\.[ox]*$|^(?=\S{8}(?!\S))[ox]*\.x*$",    #this works  
# #need work
r"^(?=[ox.]{8}$)x*\.[ox]*$|^(?=[ox.]{8}$)[ox]*\.x*$",
r"^.(..)*$",
r"^0([01]{2})*$|^1[01]([01]{2})*$",
#r"^.*(([aeiou])\2?(?!\2)).*$", 
r"^(?!.*(aa|ee|ii|oo|uu).*).*[aeiou]{2}.*$", #need work
r"^((?!110)[01])*$",
r"^[bc]*a[bc]*$|^[bc]*a$",
r"^[bc]*(a[bc]*a[bc]*)*$",
r"^[02]*(1[02]*1[02]*)*$" 
]

if idx < len(myRegexLst):
    print(myRegexLst[idx])

orthello = "xxoo.xox.....oox......oxo..ooxooo..oox.ox.xxx..oxoox...o.....xox"
edge1 = "xxoox.xx"
edge2 = "xxxx.oxx"
txt44 = "1110011010"
txt45 = "jdkfsfafeimmsdfds"
txt46 = "01010110100101"
txt48 = "bbbcabacca"
txt49 = "120120121112110"

txt = edge1
x = re.search(myRegexLst[idx], txt)

if x:
  print("YES! We have a match!")
else:
  print("No match")

