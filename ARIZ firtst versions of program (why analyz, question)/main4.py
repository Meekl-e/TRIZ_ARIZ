import pymorphy3
from  ObjectClass import *
from tkinter import *
morph = pymorphy3.MorphAnalyzer()




listNouns = []
listVerbs = []

objects = []
instrumnets = []
metods = []
goals = []
allProtiv = []

sistem = ""

question = input("Сформулируйте кратко вашу задачу: ").split()
for wordIndex in range(len(question)):
    word = question[wordIndex]
    t = morph.tag(word)[0]

    if t.POS == "NOUN" :
        listNouns.append(morph.parse(word)[0])
    if t.POS == "VERB" or t.POS == "INFN":
        listVerbs.append(morph.parse(word)[0])



for n in listNouns:
    sv = None
    role = int(input(f"Пожалуйста, выберите исполняющую роль {n.inflect({'gent'}).word} в нашей задаче из исполнитель (1), цель(2), неизменяемый объект (3), изменяемый объект (4) "))
    if role == 3:
        continue
    if role ==4:
        sv = input(f"Пожалуйста, назовите плохие свойства {n.inflect({'gent'}).word} в нашей задаче ").split()
        objects.append(Object(svoistva=sv, role=role, word=n))
    elif role==1:
        sv = input(f"Пожалуйста, назовите плохие свойства {n.inflect({'gent'}).word} в нашей задаче ").split()
        instrumnets.append(Object(svoistva=sv, role=role, word=n))
    else:
        goals.append(n)

if len(goals)==0:
    o = input("У нашей задачи нет цели! Пожалуйста, напишите цель. Она должна выражаться одним существительным. Например, уничтожение - цель, а разбить - метод ее достижения ").split()[0]
    goals.append(morph.parse(o)[0])



if any(map(lambda x:x.role==2, objects)) == False:
    o = input(
        "У нашей задачи нет исполнителя! Пожалуйста, напишите его. Это одно существительное - объект, который должен предположительно взаимодействовать с другим для получения желаемого результата ")

    object = morph.parse(o)[0]
    sv = input(f"Пожалуйста, назовите плохие свойства {object.inflect({'gent'}).word} в нашей задаче ").split()
    instrumnets.append(Object(svoistva=sv, role=1, word=object))



for v in listVerbs:
    question = input(f"Скажите, понятие '{v.normal_form}' относится к способу достижения поставленной цели? да/нет ").lower()
    if question.startswith("д"):
        metods.append(v)

if len(metods)==0:
    o = input("У нашей задачи нет споба ее достижения! Пожалуйста, напишите глагол с помощью которого можно ее достичь ").split()[0]
    goals.append(morph.parse(o)[0])

for o in objects:
    for s in o.antiSvoistva():
        r = o.word.tag.gender
        answer = input(f"Если бы {o.word.normal_form} {morph.parse('быть')[0].inflect({r}).word} бы {morph.parse(s)[0].inflect({r}).word}. Задача бы решилась (да/нет): ").lower()
        if answer.startswith("д"):
            o.protivorechiya.append((s, o.word))


# Граф построен!!!


root = Tk()
root.geometry("500x500")
root.resizable(width=False, height=False)



canvas =Canvas(root, height=500, width=500,background="grey")
photo = PhotoImage(file="image.png")
image = canvas.create_image(0, 0, anchor='nw',image=photo)
canvas.pack()


# Create the buttons with text fields above them
button1 = Button(root, text=objects[0].word.normal_form, font=("Georgia", 15,), cursor="hand2", background="blue",foreground="white" )
button1.place(x=40, y=60)


button2 = Button(root, text=objects[0].svoistva[0], font=("Georgia", 15,), cursor="hand2",background="blue",foreground="white")
button2.place(x=380, y=70)


button3 = Button(root, text=metods[0].normal_form, font=("Georgia", 15,), cursor="hand2",background="blue",foreground="white")
button3.place(x=380, y=250)


button4 = Button(root, text=goals[0].normal_form, font=("Georgia", 15,), cursor="hand2",background="blue",foreground="white")
button4.place(x=260, y=400)


button5 = Button(root, text=instrumnets[0].word.normal_form, font=("Georgia", 15,), cursor="hand2",background="blue",foreground="white")
button5.place(x=50, y=260)

root.mainloop()


for o in objects+instrumnets:
    if len(o.protivorechiya) == 0:
        continue
    s = "".join([i[0]+', ' for i in o.protivorechiya])
    s = s.removesuffix(", ")
    print(f"Скажите, существует ли в мире другой объект, которым можно заменить {o.word.inflect({'accs'}).word} и обладающий свойством '{s}' ")
    answer = input(f"Можно с помощью такого предмета можно решить нашу задачу? да/нет ").lower()
    if answer.startswith("д"):
        print("Ура, задача решена! Возможно, есть еще другие варианты...")


for o in objects:
    if len(o.protivorechiya) == 0:
        continue
    s = "".join([i[0]+', ' for i in o.protivorechiya])
    s = s.removesuffix(", ")
    print(f"Скажите, зачем нам {metods[-1].word} {o.word.inflect({'accs'}).word}?")
    answer = input(f"Может быть существуют другие рабочие способы достичь {goals[-1].inflect({'gent'}).word}? да/нет ").lower()
    if answer.startswith("д"):
        print("Ура, задача решена! Возможно, есть еще другие варианты...")


for g in goals:
    g = g.word
    answer = input(f"Может быть, нам не имеет смысла достигать цель '{g}', чтобы получить желаемый результат? ").lower()
    if answer[0] == "д":
        print("Ура, задача решена! Возможно, есть еще другие варианты...")
    else:
        answer = input(f"Скажите, можно ли произвести другие действия, но не полностью достичь или достичь с избытком цели '{g}'? ").lower()
        if answer[0] == "д":
            print("Ура, задача решена! Возможно, есть еще другие варианты...")
        else:
            answer = input(f"Может ли цель '{g}' выполниться сама со временем? ").lower()
            if answer[0] == "д":
                print("Ура, задача решена! Возможно, есть еще другие варианты...")
            else:
                answer = input(f"Может ли цель '{g}' выполниться сама без нашего участия? ").lower()
                if answer[0] == "д":
                    print("Ура, задача решена! Возможно, есть еще другие варианты...")











