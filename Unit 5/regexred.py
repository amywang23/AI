import sys; args = sys.argv[1:]
idx = int(args[0])-50

myRegexLst = [
  r"/\b\w*(\w)\w*\1\w*/i",
  r"/\b\w*(\w)(\w*\1){3}\w*/i",
  r"/^(0|1)([01]*\1)*$/",
  r"/\b(?=\w*cat)\w{6}\b/i", 
  r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i",
  r"/\b((?!cat)\w){6}\b/i",
  r"/\b(?!\w*(\w)\w*\1)\w+/i", 
  r"/^(?!.*10011)[01]*$/",
  r"/\b\w*([aeiou])(?!\1)[aeiou]\w*\b/i",
  r"/^(?!.*101)(?!.*111)[01]*$/"
  ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])

#Amy Wang 2023 Period 3