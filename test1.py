from tkinter import *
# import Tkinter as tk

root = Tk()

myLable1 = Label(root, text="Hello world")
myLable2 = Label(root, text="by world")

# myLable.pack()
myLable1.grid(row=0,column=0)
myLable2.grid(row=1, column=1)
root.mainloop()
