import json
import re
from pymorphy3 import MorphAnalyzer
from collections import Counter

def replaceAll(string):
    string = re.sub(pattern=r"[—\nt,»«()'=+_$№#%&a-z<>“„�A-Z]", repl="", string=string).replace("[", "").replace("]","")
    string = re.sub(pattern=r"[^\w\s]", repl="", string=string)
    string = re.sub(pattern=r"\s{2,}", repl=" ", string=string).lower()
    return string


def countNgramm(listWords, n):
    cntGramm = Counter([tuple(listWords[i:n]) for i in range(listWords-n+1)])
    return cntGramm


analyzer = MorphAnalyzer()

questions= open("ID-question.txt","r",encoding="UTF-8").readlines()
answers= open("ID-answer.txt","r",encoding="UTF-8").readlines()

dataList = []

dataQuestions = {}

for q in questions:
    id, q = q.split("|")
    q = replaceAll(q).split()
    q = [analyzer.normal_forms(i)[0] for i in q]
    dataQuestions[int(id)] = q


for line in answers:
    idAnswer, answer = line.split("|")
    answer = replaceAll(answer).split()
    answer = [analyzer.normal_forms(i)[0] for i in answer]
    if len(answer) == 0:
        continue
    idAnswer = int(idAnswer)
    q = dataQuestions[idAnswer]
    dataList.append(q+answer+["[end]"])
  #  print(dataList[-1])





# createGramms



three_grams={}

numGramms = 3

for line in dataList:
    for i in range(len(line)-numGramms):
        grammLast = " ".join(line[i:i+numGramms])

        grammNew = line[i+numGramms]
        if three_grams.get(grammLast) == None:
            three_grams[grammLast] = [grammNew]
        else:
            if grammNew not in three_grams[grammLast]:
                three_grams[grammLast].append(grammNew)







with open("grammars.json", "w", encoding="UTF-8") as f:
    json.dump(three_grams, f)

print(three_grams)




