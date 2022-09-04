# import cv2
# from cv2 import VideoWriter
# from cv2 import VideoWriter_fourcc
# import pyautogui as pg
# import numpy as np
#
# while True :
#     screenshot = cv2.cvtColor(np.array(pg.screenshot()), cv2.COLOR_RGB2BGR)
#     cv2.imshow('Screenshot', screenshot)
#     # cv2.waitKey()
#     if cv2.waitKey(1) & 0xFF == 27 : break
# cv2.destroyAllWindows()
#
import tkinter
from tkinter import *
from PIL import ImageTk, Image
import cv2


root = Tk()
# Create a frame
root.geometry('700x600')
app = Frame(root, bg="black")
app.pack()


# Create a label in the frame
fmain = Frame(app, width=700, height=600, )
fmain.pack()
lmain = Label(fmain, bg='blue')
lmain.pack()

# Capture from camera
cap = cv2.VideoCapture(0)

# function for video streaming

def video_stream():
    print(1)
    _, frame = cap.read()
    print("frame: ",type(frame),frame)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    print("cvimage: ",type(cv2image),cv2image)
    img = Image.fromarray(cv2image)
    print("image: ",type(img),img)

    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    return
    lmain.after(1, video_stream)
    print(2)

# video_stream()
title = tkinter.Button(root, text="Hi", command=video_stream)
title.pack()
root.mainloop()
