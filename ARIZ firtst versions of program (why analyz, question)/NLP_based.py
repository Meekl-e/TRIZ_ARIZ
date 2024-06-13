import requests
import time
import re
import numpy as np
import nltk
from pymorphy3 import MorphAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def compareData(text):
    global allwords
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('russian'))
    words = [word for word in tokens if word not in stop_words]
    words = [analyzer.parse(word)[0].normal_form for word in words]
    print(words)
    for word in words:
        if word.isalpha() or "-" in word:
            allwords= np.append(allwords, word+"\n")
    allwords = np.unique(allwords)

nltk.download("punkt")
nltk.download('stopwords')
nltk.download('omw-1.4')
analyzer = MorphAnalyzer(lang="ru")
#print(len('<div class="que clearfix"><p>'),len('</p></div></div>'))
#response = requests.get("https://www.trizland.ru/tasks/1241/")
#text = str(response.text).replace("\n","").replace(r"\r","")

with open("site.html","r",encoding="UTF-8") as file:
    text=file.read().replace(r"\r","").replace(r"\t","").replace(r"\n","").replace("&shy;","")

pattern = '<div class="que clearfix"><p>.*</p></div></div>'
patternComments = '<li id="comment\d*">.*?</li>'
patternInComments = '</div><p>.*?</p></div>'


answers = open("ID-answer.txt","r",encoding="UTF-8")
questions = open("ID-question.txt","r",encoding="UTF-8")
allWordsFile = open("words.txt","r",encoding="UTF-8")
allwords = np.array([])

ID = 0
for i in range(1241, 1875):#6240):
    time.sleep(1)
    try:
        response = requests.get(f"https://www.trizland.ru/tasks/{i}/")
    except TimeoutError:
        continue
    text = str(response.text).replace(r"\r","").replace(r"\t","").replace(r"\n","").replace("&shy;","").replace("&laquo;","")
    print("*****************")
    print(i)
    question = re.search(pattern, text)
    if question is None:
        print("NONE")
        continue
    question = question[0][29:-16]
    print(question)
    coms = re.findall(patternComments, text)
    if len(coms) == 0:
        continue
    compareData(question)
    for com in coms:
        comment = re.search(patternInComments, com)
        if comment is None:
            continue
        comment = comment[0][9:-10]
        compareData(comment)
        print(comment)
        print("==")
        answers.write(f"{ID}|{comment}\n")
    questions.write(f"{ID}|{question}\n")


    ID += 1

for i in range(5041, 6240):#6240):
    time.sleep(1)
    try:
        response = requests.get(f"https://www.trizland.ru/tasks/{i}/")
    except TimeoutError:
        continue
    text = str(response.text).replace(r"\r","").replace(r"\t","").replace(r"\n","").replace("&shy;","").replace("&laquo;","")
    print("*****************")
    print(i)
    question = re.search(pattern, text)
    if question is None:
        print("NONE")
        continue
    question = question[0][29:-16]
    print(question)
    coms = re.findall(patternComments, text)
    if len(coms) == 0:
        continue
    compareData(question)
    for com in coms:
        comment = re.search(patternInComments, com)
        if comment is None:
            continue
        comment = comment[0][9:-10]
        compareData(comment)
        print(comment)
        print("==")
        answers.write(f"{ID}|{comment}\n")
    questions.write(f"{ID}|{question}\n")


    ID += 1

allWordsFile.writelines(allwords)



