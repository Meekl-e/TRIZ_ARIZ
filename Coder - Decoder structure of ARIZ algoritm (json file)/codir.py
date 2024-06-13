

def target(task):
    result = {}
    inst = ""
    if input(f"Скажите, {task} является сценарием или целью? Цель - уничтожение вазы, разбить вазу - сценарий. Напишите СЦЕНАРИЙ или ЦЕЛЬ: ").lower().startswith("ц"):
        result["goal"] = task
        scenario = input(f"Скажите, каким способом (сценарием) вы хотите достичь {task}? ")
        result["scenarios"] = [{"scenario":scenario, "roles":[]}]
    else:
        goal = input("Скажите, какая цель у данной задачи? ")
        result["goal"] = goal
        result["scenarios"] = [{"scenario":task, "roles":[]}]
        scenario = task
    result["object"] = input(f"Назовите объект, который является главным в нашей задаче. Он может обладать свойствами. Обычно он фигурирует в '{result['goal']}': ").lower()
    result["problem-object"] = input(f"Назовите свойства объекта '{result['object']}' через пробел, которые мешают выполнению '{result['goal']}': ").lower().split()


    inst = input(
        f"С помощью чего можно {scenario}? Назвите объект, с помощью которого выполняется данное действие. . для завершения: ")
    while inst != ".":
        role = input(
            f"Скажите, какую роль играет {inst} в нашей задаче? Например, молоток в скценарии разбить вазу играет роль уничтожитель: ")
        problem = input(f"А в чем проблема объекта {inst}? Назовите его плохие свойства через пробел: ").lower()
        result["scenarios"][-1]["roles"].append({"role": role, "actor": inst, "problem": problem.split()})
        inst = input(
            f"С помощью чего можно {task}? Назвите объект, с помощью которого выполняется данное действие. . для завершения: ")

    if input(f"Скажите, есть ли еще способы (сценарии) достижения {result['goal']}? да/нет ").lower().startswith("д"):
        scenario = input("Скажите название способа (. для завершения): ")
        while scenario !=".":
            result["scenarios"].append({"scenario":scenario, "roles":[]})
            inst = input(
                f"С помощью чего можно {scenario}? Назвите объект, с помощью которого выполняется данное действие. . для завершения: ")
            while inst != ".":
                role = input(f"Скажите, какую роль играет {inst} в нашей задаче? Например, молоток в скценарии разбить вазу играет роль уничтожитель: ")
                problem = input(f"А в чем проблема объекта {inst}? Назовите его плохие свойства через пробел (. если свойств нет): ").lower()
                if problem == ".":
                    result["scenarios"][-1]["roles"].append({"role":role, "actor":inst, "problem":[]})
                else:
                    result["scenarios"][-1]["roles"].append({"role": role, "actor": inst, "problem": problem.split()})
                inst = input(f"С помощью чего можно {task}? Назвите объект, с помощью которого выполняется данное действие. . для завершения: ")
            scenario = input("Скажите название способа (. для завершения): ")


    return result