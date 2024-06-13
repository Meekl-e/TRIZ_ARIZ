import json
import re
from copy import copy


questions= open("ID-question.txt","r",encoding="UTF-8").readlines()
answers= open("ID-answer.txt","r",encoding="UTF-8").readlines()


dataQuestions = {}
data = {}

for q in questions:

    id, q = q.split("|")
    q = q.split()
    q = " ".join(q)
    dataQuestions[int(id)] = q
    data[q] = []




for line in answers:
    idAnswer, answer = line.split("|")
    answer = answer.split()
    if len(answer) == 0:
        continue
    answer = " ".join(answer)
    idAnswer = int(idAnswer)
    q = dataQuestions.get(idAnswer)
    if q == None:
        continue
    if answer not in data[q]:
        data[q].append(answer)

for q in copy(list(data.keys())):
    if len(data[q]) == 0:
        data.pop(q)

with open("data.json", "w", encoding="UTF-8") as f:
    json.dump(data, f, indent=1, ensure_ascii=False)




