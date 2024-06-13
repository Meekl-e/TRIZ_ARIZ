import json
from pymorphy3 import MorphAnalyzer
from collections import Counter
from copy import copy
from itertools import combinations_with_replacement

def predict(lastWords):
    global dictionary
    lastWords = lastWords.lower()
    if dictionary.get(lastWords) == None:
        return ["[EOS]"]
    results = dictionary[lastWords]
   # print(results)
    return results


def createCombinations():
    return [list(s) for s in combinations_with_replacement([analyzer.normal_forms(i)[0] for i in input().split()], numGrams)]


analyzer = MorphAnalyzer()


with open('grammars.json') as f:
    file_content = f.read()
    dictionary = json.loads(file_content)


#print(sentenc, end="")

numGrams = 3

gen = True

sentenc = createCombinations()


while gen:
    copyL =copy(sentenc)
    for s in copyL:

        if max(Counter(s).values()) > 3 or len(s) > 500:
            sentenc.remove(s)
            continue
        nextWords = predict(" ".join(s[-numGrams:]))
        for w in nextWords:
            if s[-1] == ".":
                if w[-1] == ".":
                    w = "[end]"
                w = w.capitalize()
            if w == "[end]" or w =="[EOS]":
                print(" ".join(s))
            else:
                newSent = copy(s)
                newSent.append(w)
                sentenc.append(newSent)
        sentenc.remove(s)
    if len(sentenc) == 0:
        gen = False
   # print(sentenc)
    #time.sleep(5)






