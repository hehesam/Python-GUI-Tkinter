from tkinter import *
# import Tkinter as tk

root = Tk()

myLable1 = Label(root, text="Hello world").grid(row=0,column=0)
myLable2 = Label(root, text="by world")

# myLable.pack()
myLable2.grid(row=1, column=1)
root.mainloop()
