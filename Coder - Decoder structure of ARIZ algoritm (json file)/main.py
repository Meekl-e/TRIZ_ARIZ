import json
import codir
import dexoder


with open("task.json", "w", encoding="UTF-8") as f:
    f.write(json.dumps(codir.target(input("Введите вашу задачу"))))
for r in dexoder.decoder():
    print(r)

