import json
import re
from pymorphy3 import MorphAnalyzer
from collections import Counter
import numpy as np



def replaceAll(string):
    string = re.sub(pattern=r"[—\nt,»«()'=+_$№#%0-9()&a-z<>“„�A-Z]", repl="", string=string).replace("[", "").replace("]","")
    string = re.sub(pattern=r"[^\w\s]", repl="", string=string)
    string = re.sub(pattern=r"\s{2,}", repl=" ", string=string).lower()
    return string


with open('dictionary.json', "r") as f:
    file_content = f.read()
    data = json.loads(file_content)


analyzer = MorphAnalyzer()

while True:
    string = replaceAll(input())

    question = [analyzer.normal_forms(i)[0] for i in string.split()]
    chancesNumbers = []
    questions = []

    for q in data.keys():
        chanceThis = 0
        for word in data[q]:
            if word == "answers":
                continue
            if word in question:
                chanceThis+= data[q][word]
        chancesNumbers.append(chanceThis)
        questions.append(q)
    q = questions[np.argmax(chancesNumbers)]
    print(q)
    for a in data[q]["answers"]:
        print(a)




