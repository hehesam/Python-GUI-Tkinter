from tkinter import *

root = Tk()

e = Entry(root, width=50)
e.pack()
e.insert(0, "Enter your name :")

def     myClick():
    hello = "Hello " + e.get()
    myLabel = Label(root, text=hello)
    myLabel.pack()


myButton = Button(root, text="click me ", command=myClick, font="Helvetica", fg="red", bg="green")
myButton.pack()

root.mainloop()
