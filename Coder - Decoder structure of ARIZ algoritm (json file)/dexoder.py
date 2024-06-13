import json


def decoder():
    with open("task.json", "r", encoding="UTF-8") as f:
        task = json.loads(f.read())
    results = []
    results.append(f"Достигнуть цели выше '{task['goal']}'. Задайте себе вопрос: зачем надо '{task['goal']}'? И с ответом перезаупустите программу")
    for i in range(len(task['scenarios'])):
        results.append(f"Достигнуть цели '{task['goal']}' любым другим путем, кроме {task['scenarios'][i]['scenario']}")
    for i in range(len(task["scenarios"])):
        for j in range(len(task['scenarios'][i]['roles'])):
            results.append(f"Взять любой другой предмет, который подходит на роль {task['scenarios'][i]['roles'][j]['role']}")
            if len(task['scenarios'][i]['roles'][j]['problem']) > 0:
                results.append(f"Изменить свойства {task['scenarios'][i]['roles'][j]['actor']} так, чтобы убрать свойство(а) {', '.join(task['scenarios'][i]['roles'][j]['problem'])}")
    for i in range(len(task['problem-object'])):
        results.append(f"Попробовать изменить свойство {task['problem-object'][i]} объекта {task['object']} в пространстве, во времени, в структуре, в отношениях")
    return results
