# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
from tkinter import *
from tkinter.ttk import *
# from deepSpeech_voice import start_voice
import subprocess
import tkinter

# creates a Tk() object
master = Tk()

# sets the geometry of main
# root window
master.geometry("40 0x400")
master.title("METAFIT")


def thing(my_label):
    my_label.config(text="You clicked the button...")
    # subprocess.call(["gnome-terminal", "--", "sh", "-c", "python3 deepSpeech_voice.py"])
    subprocess.call(["gnome-terminal", "--", "sh", "-c", "./rope.x86_64"])


    # start_voice()

def openNewWindow():
    newWindow = Toplevel(master)
    newWindow.title("Voice")
    newWindow.geometry("512x640")

    # A Label widget to show in toplevel

    listing_btn = PhotoImage(file='mic3.png')
    # Label(newWindow,image=listing_btn).pack()
    exit_button = Button(newWindow, text='exit', command=newWindow.quit)

    my_label = Label(newWindow, text='')
    my_label.pack()
    mic_button = tkinter.Button(newWindow, image=listing_btn, command=lambda : thing(my_label), borderwidth=0 )
    mic_button.pack()
    exit_button.pack()
    newWindow.mainloop()

def pose_tab():
    pos_window = Toplevel(master)
    pos_window.title("pose estimation")

label = Label(master,
              text="This is the main window")

label.pack(pady=10)

# a button widget which will open a
# new window on button click
btnv = tkinter.Button(master,
             text="open voice recognition",
             command=openNewWindow)
btnp = Button(master, text="Pose estimation",
              command=pose_tab)
btnv.pack()
btnp.pack()
listing_btn = PhotoImage(file='mic3.png')
# Label( image=listing_btn, text="why").pack()
# mainloop, runs infinitely
mainloop()
