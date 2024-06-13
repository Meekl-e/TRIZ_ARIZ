from pymorphy3 import MorphAnalyzer
from pochemychka import pochemy
from ObjectClass import Object
from why import whyAnalyz


def getInstruments(analyzer, obj, sistem):
    instrument = input(f"Назовите инструмент, с помощью которого можно {obj.normal_form} {sistem.inflect({'accs'})[0]}.\nНапишите . когда инструменты закончатся.\n").lower()
    insGreatList = []
    instList = []
    while instrument != ".":
        instrPars = analyzer.parse(instrument)[0]
        ispathFree = input(f"Что-то мешает {obj.normal_form} {sistem.inflect({'accs'})[0]} {instrPars.inflect({'ablt'})[0]}? Да-напишите отрицательные свойства через пробел, нет - напишите нет ").lower()
        if ispathFree.startswith("нет"):
            insGreatList.append("Использовать "+ instrument)
        else:
            svList = ispathFree.split()
            instList.append(Object(instrPars, svList))
        instrument = input("Следующий инструмент - ")
    return insGreatList, instList


def anotherSposoby(analyzer, goal):
    listSposobs = []
    sposob =  input(f"Какой есть еще способ достичь {goal}? . для завершения").lower()
    while sposob != ".":
        whatProblem = input(f"В чем проблема {sposob}? Если есть - напишите, нет - напишите нет " ).lower()
        if whatProblem == "нет":
            listSposobs.append(f"Достичь высшей цели {goal}, тем что {sposob}")
        else:
            listSposobs += pochemy(analyzer, whatProblem)
        sposob = input(f"Какой есть еще способ достичь {goal}? . для завершения").lower()
    return listSposobs
def target(analyzer, task):
    resheniya = []
    analyzer  = MorphAnalyzer()
    obj, sistem =map(lambda x:analyzer.parse(x)[0],task.split())
    instGl, insL = [], []
    #obj = analyzer.parse("разбить")[0]
    #sistem = analyzer.parse("вазу")[0]
    questionWait = input(f"{sistem.normal_form} может {analyzer.parse('сам')[0].inflect({sistem.tag.gender})[0]} {obj.normal_form+'ся'}? да/нет ").lower()
    if questionWait.startswith("да"):
        resheniya.append("Подождать")
    questionInstr = input(f"{sistem.inflect({'accs'})[0]} можно чем-то {obj.normal_form}? да/нет").lower()

    if questionInstr.startswith("да"):
        instGl, insL = getInstruments(analyzer, obj, sistem)
        resheniya+=instGl
        resheniya+= list(map(lambda x:"Взять (если такое возможно) "+" ".join(x.antiSvoistva())+" "+x.word.normal_form,insL))

    questionWhy = input(f"Зачем надо {obj.normal_form} {sistem.inflect({'accs'})[0]}?").lower().split()[-1]
    resheniya += whyAnalyz(analyzer, questionWhy)

    questionNo = input(f"Можно не {obj.normal_form} {sistem.inflect({'accs'})[0]}? да/нет").lower()
    if questionNo.startswith("да"):
        resheniya.append(f"Не {obj.normal_form} {sistem.inflect({'accs'})[0]}")

    questionNoDo = input(f"Можно не {obj.normal_form} {sistem.inflect({'accs'})[0]}, а достичь {questionWhy} другим путем? да/нет").lower()
    if questionNoDo.startswith("да"):
        resheniya+=anotherSposoby(analyzer, questionWhy)

    questionTo = input(f"К чему приведет {obj.normal_form} {sistem.inflect({'accs'})[0]}? Например, разбить вазу приведет к уничтожению. Напишите 1 слово ").lower()
    if analyzer.parse(questionTo.split()[-1])[0].normal_form ==  analyzer.parse(questionWhy.split()[-1])[0].normal_form:
        izmenenie = obj.normal_form
        scenario = analyzer.parse(input(f"Как можно {obj.normal_form} {sistem.inflect({'accs'})[0]}? Напишите 1 слово ").lower())[0].normal_form
    else:
        izmenenie = analyzer.parse(questionTo.split()[-1])[0].normal_form
        scenario = analyzer.parse(questionWhy.split()[-1])[0].normal_form
    questionAboutSistem =  input(f"Какими плохими свойствами обладает {sistem.inflect({'gent'})[0]} в нашей задаче? Напишите свойства через пробел или . если свойств нет").lower().split()
    if questionAboutSistem[0] != ".":
        sistem = Object(sistem, questionAboutSistem, role="sistem")

        for i in insL:
            analyzTask1 = f"{sistem.word.normal_form} ---------> {izmenenie} ---------> {scenario} ---------> {i.word.normal_form}"
            resheniya.append(analyzTask1)
            for j in range(3):
                resheniya.append("|" + " "*(len(analyzTask1) - 2)+"|")
            for svI in i.svoistva:
                for sv in sistem.svoistva:
                    questionAboutSv = input(
                        f"Скажите, '{sv}' является антонимом (противоположное значение, противоречит) '{svI}'. да/нет ").lower()
                    if questionAboutSv.startswith("да"):
                        resheniya.append(f"{sv}  <"+"-"*(len(analyzTask1)-len(sv)-len(svI))+f"> {svI}")




    return resheniya




