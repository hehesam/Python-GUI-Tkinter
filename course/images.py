from tkinter import *

root = Tk()
root.title("Hi")
# root.iconbitmap('~/programs/python/python-GUI-tkinter/icon.ico')

botton_quit = Button(root, text="Exit program", command=root.quit)
botton_quit.pack()
root.mainloop()