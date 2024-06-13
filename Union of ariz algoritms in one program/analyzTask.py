from pymorphy3 import MorphAnalyzer

from problem import problem
from  target import target
analyzer = MorphAnalyzer()


taskText = input("Опишите вашу цель или проблему (кратко): ")
isProblem = int(input("Это является проблемой? 1 - это проблема, 0-это цель"))

if isProblem == "1":
    problem(analyzer, taskText)
else:
    target(analyzer, taskText)




