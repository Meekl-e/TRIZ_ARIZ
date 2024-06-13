from flask import *
from pymorphy3 import MorphAnalyzer

from app.ObjectClass import Object

app = Flask(__name__)

users = {}
analyzer = MorphAnalyzer()


def target(msg: str):
    global analyzer
    user = users[request.remote_addr]

    user["count"] = round( user["count"], 2)
    print(user["count"])
    if user["count"] == 1:
        obj, sistem = map(lambda x: analyzer.parse(x)[0], msg.split())

        user["messages"].append(f"{sistem.normal_form} может {analyzer.parse('сам')[0].inflect({sistem.tag.gender})[0]} {obj.normal_form+'ся'}? да/нет ")
        user["sistem"] = sistem
        user["elements"]["obj"] =obj
        user["count"]+=1
    elif user["count"] == 2:
        if msg.lower().startswith("да"):
            user["resheniya"].append("Подождать")
        user["messages"].append(f"{user['sistem'].inflect({'accs'})[0]} можно чем-то {user['elements']['obj'].normal_form}? да/нет")
        user["count"]+=1
    elif user["count"] == 3:
        if msg.lower().startswith("нет"):
            user["count"] = 5
            return
        user["messages"].append(
            f"Назовите инструмент, с помощью которого можно {user['elements']['obj'].normal_form} {user['sistem'].inflect({'accs'})[0]}.\nНапишите . когда инструменты закончатся.\n")
        user["count"]+=0.1
    elif user["count"] > 3 and user["count"] < 4 and str(user["count"])[-1]!="5":
        if msg == ".":
            user["resheniya"] += user["elements"]["insGreatList"]
            user["resheniya"] += list(
                map(lambda x: "Взять (если такое возможно) " + " ".join(x.antiSvoistva()) + " " + x.word.normal_form,
                    user["elements"]["instList"]))
            user["messages"].append(
                f"Можно не {user['elements']['obj'].normal_form} {user['sistem'].inflect({'accs'})[0]}? да/нет")
            user["count"] = 5
            return
        user["elements"]["instrPars"] = analyzer.parse(msg)[0]
        user["messages"].append(
            f"Что-то мешает {user['elements']['obj'].normal_form} {user['sistem'].inflect({'accs'})[0]} {user['elements']['instrPars'].inflect({'ablt'})[0]}? Да-напишите отрицательные свойства через пробел, нет - напишите нет ")
        user["count"]+=0.05
    elif  user["count"] > 3 and user["count"] < 4 and user["count"]!=3.5 and str(user["count"])[-1]=="5":
        if msg.lower().startswith("нет"):
            user["elements"]["insGreatList"].append("Использовать "+ user["elements"]["instrPars"].normal_form)
            user["roles"].append((user["elements"]["instrPars"].normal_form, []))
        else:
            svList = msg.lower().split()
            user["elements"]["instList"].append(Object(user["elements"]["instrPars"], svList))
            user["roles"].append((user["elements"]["instrPars"].normal_form, svList))
        user["messages"].append("Напишите следующий инструмент")
        user["count"] += 0.05
    elif user["count"] == 5:
        if msg.lower().startswith("да"):
            user["resheniya"].append(f"Не {user['elements']['obj'].normal_form} {user['sistem'].inflect({'accs'})[0]}")
        user["messages"].append(
            f"К чему приведет {user['elements']['obj'].normal_form} {user['sistem'].inflect({'accs'})[0]}? Например, разбить вазу приведет к уничтожению. Напишите 1 слово ")
        user["count"]+=1
    elif user["count"] == 6:
        user["change"] = msg.capitalize()
        user["messages"].append(
                f"Как можно {user['elements']['obj'].normal_form} {user['sistem'].inflect({'accs'})[0]}? Напишите 1 слово ")
        user["count"]+=1
    elif user["count"] == 7:
        user["scenario"] = msg.capitalize()
        user["messages"].append(f"Какими плохими свойствами обладает {user['sistem'].inflect({'gent'})[0]} в нашей задаче? Напишите свойства через пробел или . если свойств нет")
        user["count"]+=1
    elif user["count"] == 8:
        if msg == ".":
            lstSv = []
        else:

            lstSv = msg.lower().split()
        user["svoistva"] = lstSv
        sistem = Object(user['sistem'], lstSv, role="sistem")

        for i in user["elements"]["instList"]:
            analyzTask1 = f"{sistem.word.normal_form} ---------> {user['change']} ---------> {user['scenario']} ---------> {i.word.normal_form}"
            user["resheniya"].append(analyzTask1)
            for j in range(3):
                user["resheniya"].append("|" + " " * (len(analyzTask1) - 2) + "|")
            for svI in i.svoistva:
                for sv in sistem.svoistva:
                    user["resheniya"].append(f"{sv}  <" + "-" * (len(analyzTask1) - len(sv) - len(svI)) + f"> {svI}")
        user["messages"].append("; ".join(user["resheniya"]))
        user["count"]+=1








@app.route('/', methods=['post', 'get'])
def index():


    if users.get(request.remote_addr) is None:
        users[request.remote_addr] = {"sistem": analyzer.parse("")[0], "change": "", "scenario": "", "msg": "",
                                      "svoistva":[],"resheniya":[], "roles":[], "count":1, "elements": {"insGreatList":[], "instList":[]},
                                      "messages": ["Опишите вашу цель (в двух словах)"]}

    param = users[request.remote_addr]

    if request.method == 'POST':

        for p in param.keys():
            if p == "sistem" and not request.form.get(p) is None:
                param[p] = analyzer.parse(request.form.get(p))[0]
            elif param[p] != "" and param[p]!=None and p!="msg": continue
            else:
                param[p] = request.form.get(p)
        if not param.get("msg")  is None and param.get("msg").replace(" ", "") != "":

            param["messages"].append(param.get("msg"))
            target(param["messages"][-1])
            param["messages"] = param["messages"][-7:]
    print(users[request.remote_addr])
    return render_template('index.html', sistem=param["sistem"].normal_form, change=param["change"],
                           scenario=param["scenario"], messages=reversed(param["messages"][-7:]), svoistva=param["svoistva"],
                           roles=param["roles"])

@app.route('/sistem', methods=['post'])
def sistem():
    users[request.remote_addr]["sistem"] =analyzer.parse("")[0]
    return redirect(url_for("index"))

@app.route('/change', methods=['post'])
def change():
    users[request.remote_addr]["change"] = ""
    return redirect(url_for("index"))

@app.route('/scenario', methods=['post'])
def scenario():
    users[request.remote_addr]["scenario"] = ""
    return redirect(url_for("index"))
@app.route('/reset', methods=['post'])
def reset():
    users[request.remote_addr] = {"sistem": analyzer.parse("")[0], "change": "", "scenario": "", "msg": "",
                                      "svoistva":[],"resheniya":[], "roles":[], "count":1, "elements": {"insGreatList":[], "instList":[]},
                                      "messages": ["Опишите вашу цель (в двух словах)"]}
    print("EWf")
    return redirect(url_for("index"))

@app.route("/tasks", methods=["get"])
def tasks():
    return render_template("tasks.html")


if __name__ == "__main__":
    app.run()
