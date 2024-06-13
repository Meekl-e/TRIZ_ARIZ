import pymorphy3

from classConnectors import Connector

morph = pymorphy3.MorphAnalyzer()



def setQuestion(connector):
    wordMain = connector.mainWord
    verb = connector.verbConnect
    word = connector.word
    m = ""
    v = ""
    w = ""
    n = ""

    if wordMain != None:
        m = wordMain.normal_form
    elif word != None:
        m = word.normal_form
    if verb != None:
        if wordMain != None:
            try:
                v = verb.inflect({wordMain.tag.number, wordMain.tag.person}).word
            except ValueError:
                v = verb.inflect({wordMain.tag.number}).word
        elif word !=None and word.tag.number != None:
                v = verb.inflect({word.tag.number}).word
        else:
            v = verb.inflect({"plur", "2per"}).word
    if word != None:
        if connector.typeO.startswith("n"):
            w = word.inflect({"gent"}).word
        else:
            w = word.normal_form

    if connector.typeO=="no" and( m !="" or v!="" or w !=""):
        n = "не"
    elif connector.typeO =="not" and( m !="" or v!="" or w !=""):
        n = "нет"
    return f"Почему {n} {v} {w}? ".replace("  "," ")



def setQuestionToAnswer(connector):
    verb = connector.verbConnect
    word = connector.word
    if verb != None:
        v = verb.inflect({"INFN"}).word
    else:
        v = "получить"
    if word != None:
        w = word.inflect({"accs"}).word
    else:
        return None
    return f"{v} {w}"



listConnectors = []
listAnswers = {}

verb = None
wordMain = None
w = None

question = input("В чем ваша задача? ").split()
for word in question:
    p = morph.parse(word)[0]
    t = p.tag
    if (t.POS == "NOUN" and t.case == "nomn") or t.POS=="NPRO" :
        wordMain = p
    if (t.POS == "NOUN" and t.case in ["acc2","accs"]) or t.POS == "INFN" :
        w = p
    elif t.POS == "VERB":
        verb = p


listConnectors.append(Connector(typeObject="yes", word=w, verb=verb, mainWord=wordMain))


questions = True
while questions:
    question = input(setQuestion(listConnectors[-1])).split()
    wordTo = None
    wordMain = None
    verb = None
    typeW = "yes"
    for word in question:
        if word == "х":
            questions = False
            break
        p = morph.parse(word)[0]
        if p.normal_form == "не":
            typeW = "no"
        elif p.normal_form == "нет":
            typeW = "not"
        t = p.tag
        if t.POS == "NOUN" and t.case == "nomn":
            wordMain = p
        if (t.POS == "NOUN" and t.case in ["acc2", "accs", "gent"]) or t.POS == "INFN":
            wordTo = p
        elif t.POS == "VERB":
            verb = p
    if questions:
        listConnectors.append(Connector(typeObject=typeW, word=wordTo, verb=verb, mainWord=wordMain))


for i in range(1, len(listConnectors) ):
    a = setQuestionToAnswer(listConnectors[i])
    if a == None:
        continue
    question = input("Есть ли другое рабочее решения вместо: '"+a+"'").lower()
    if question=="нет" or question=="х":
        continue

    listAnswers[a+"|"+str(i)] = [question]
    questions = True
    while questions:

        question = input("Что нужно, чтобы "+listAnswers[a+"|"+str(i)][-1]+"? ").lower()
        if question == "х":
            break
        listAnswers[a+"|"+str(i)].append(question)





print("\nВозможные решения:")
for a in listAnswers.keys():
    for s in list(reversed(listAnswers[a])):
        print(s, end="=>")
    indexSep = a.index("|")

    index = int(a[indexSep+1:])
    for i in range(index-1,0,-1):
        print(setQuestionToAnswer(listConnectors[i]),end="=>")
    print()


