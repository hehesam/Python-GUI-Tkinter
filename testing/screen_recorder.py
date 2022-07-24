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
app = Frame(root, bg="white")
app.pack()
title = tkinter.Button(root, text="Hi")
title.pack()

# Create a label in the frame
lmain = Label(app)
lmain.grid()

# Capture from camera
cap = cv2.VideoCapture(0)

# function for video streaming
def video_stream():
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, video_stream)

video_stream()
root.mainloop()
