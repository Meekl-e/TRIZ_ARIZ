import pymorphy3
from  ObjectClass import *

morph = pymorphy3.MorphAnalyzer()

svoistva = []

listNouns = []
listVerbs = []

objects = []
verbs = []



question = input("В чем ваша задача? ").split()
for word in question:
    t = morph.tag(word)[0]

    if t.POS == "NOUN" :
        listNouns.append(morph.parse(word)[0])
    if t.POS == "VERB":
        listVerbs.append(morph.parse(word)[0])

for n in listNouns:
    role = int(input(f"Пожалуйста, выберите исполняющую роль {n.inflect({'gent'}).word} в нашей задаче из инструмент (1), неизменяемый объект (2), изменяемый объект (3) "))
    if role == 2:
        continue
    sv = input(f"Пожалуйста, назовите плохие свойства {n.inflect({'gent'}).word} в нашей задаче ").split()
    objects.append(Object(svoistva=sv, role=role, word=n))

for v in listVerbs:
    question = int(input(f"Скажите, понятие '{v.normal_form}' необходимо увеличить (1),оставить прежним (2), уменьшить (3). Введите цифру: "))
    if question == 1 or question==3:
        verbs.append(Verb(v, question))

for o in objects:
    for s in o.antiSvoistva():
        r = o.word.tag.gender
        answer = input(f"Если бы {o.word.normal_form} {morph.parse('быть')[0].inflect({r}).word} бы {morph.parse(s)[0].inflect({r}).word}. Задача бы решилась (да/нет): ")
        if answer.startswith("д"):
            if s[:2].lower() == "не":
                o.protivorechiya.append((s[2:], o.word))
            else:
                o.protivorechiya.append(("не" +s, o.word))


allP = []
for o in objects:
    for p in o.protivorechiya:
        for o2 in objects:
            if o == o2:
                continue
            for p2 in o2.protivorechiya:
                if (p2,p) not in allP:
                    allP.append((p,p2))


print("Технические противоречия: ")
for t in allP:
    print(f"{t[0][0]} {t[0][1].inflect({'gent'}).word} противоречит с {t[1][0]} {t[1][1].inflect({'gent'}).word} ")




