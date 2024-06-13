from tkinter import *
import pymorphy3


morph = pymorphy3.MorphAnalyzer()

def createSistem():
    win = Tk()
    win.geometry("200x700")
    win.configure(background="white")
    win.resizable(width=False, height=False)
    sistem = StringVar(value=listNouns[0])
    for n in listNouns:
        n = n[0]
        btn = Radiobutton(win, cursor="hand2", text=n, value=n, variable=sistem, background="white", )
        btn.pack(fill=X)
    button1.configure(background="azure")
    win.mainloop()




listNouns = []
listVerbs = []


root = Tk()
root.geometry("500x500")
root.resizable(width=False, height=False)



canvas =Canvas(root, height=500, width=500,background="grey")
photo = PhotoImage(file="image.png")
image = canvas.create_image(0, 0, anchor='nw',image=photo)
canvas.pack()


# Create the buttons with text fields above them
button1 = Button(root, text="Система", font=("Georgia", 15,), cursor="hand2", background="blue",foreground="white", command=createSistem )
button1.place(x=40, y=60)


button2 = Button(root, text="Свойство", font=("Georgia", 15,), cursor="hand2",background="blue",foreground="white", command=createInstruments)
button2.place(x=380, y=70)


button3 = Button(root, text="Изменение", font=("Georgia", 15,), cursor="hand2",background="blue",foreground="white")
button3.place(x=380, y=250)


button4 = Button(root, text="Сценарий", font=("Georgia", 15,), cursor="hand2",background="blue",foreground="white")
button4.place(x=260, y=400)


button5 = Button(root, text="Роль", font=("Georgia", 15,), cursor="hand2",background="blue",foreground="white")
button5.place(x=50, y=260)



# Run the main loop
root.mainloop()