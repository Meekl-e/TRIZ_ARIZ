import json
import re
from pymorphy3 import MorphAnalyzer
from collections import Counter
import math


def replaceAll(string):
    string = re.sub(pattern=r"[—\nt,»«()'=+_$№#%0-9()&a-z<>“„�A-Z]", repl="", string=string).replace("[", "").replace("]","")
    string = re.sub(pattern=r"[^\w\s]", repl="", string=string)
    string = re.sub(pattern=r"\s{2,}", repl=" ", string=string).lower()
    return string

analyzer = MorphAnalyzer()

with open('data.json', "r", encoding="UTF-8") as f:
    file_content = f.read()
    data = json.loads(file_content)

normalizedData = {}

for string in data.keys():
    normalizedData[replaceAll(" ".join([analyzer.normal_forms(i)[0] for i in string.split()]))] = data[string]




classes = normalizedData.keys()
countWords = len(classes)


allWords = set([a for b in [i.split() for i in normalizedData.keys()] for a in b])
print(allWords)

allKeyWords = {}

for w in allWords:
    allKeyWords[w] = sum([1 for i in normalizedData.keys() if w in i.split()])


dataChances = {}
for question in classes:
    dataThisChances = {}
    c = question.split()
    countClass = len(c)
    words = Counter(c)
    for w in c:
        TF_IDF = (words.get(w)/countClass) *math.log(countWords/allKeyWords[w],10)
        dataThisChances[w] = TF_IDF
        print(TF_IDF)
    dataThisChances["answers"] = normalizedData[question]
    dataChances[question] = dataThisChances




with open("dictionary.json", "w", encoding="UTF-8") as f:
    json.dump(dataChances, f)

