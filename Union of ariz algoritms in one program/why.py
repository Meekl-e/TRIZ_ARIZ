




def whyAnalyz(analyzer, task):
    answer = input("Зачем "+ task+"? . для завершения")
    line = []
    sposobs = []
    if answer == ".":
        return []
    while True:
        line.append(answer)
        answer = input(f"Зачем {analyzer.parse(answer.split()[-1])[0].normal_form}?")
        if answer ==".":
            sposobs.append("=>".join(reversed(line)))
            return sposobs
        spopyQ = input(f"{analyzer.parse(answer.split()[-1])[0].normal_form} можно добиться другими способами? да/нет")
        if spopyQ.startswith("да"):
            sposob = input(f"Скажите, что нужно сделать, чтобы добиться {analyzer.parse(answer.split()[-1])[0].normal_form}? ")
            sp = [analyzer.parse(answer.split()[-1])[0].normal_form]
            while sposob != ".":
                sp.append(sposob)
                sposob = f"Как можно {sposob}?"
            sposobs.append(list(reversed(sp)))