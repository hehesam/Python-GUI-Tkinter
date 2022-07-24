import time
import os
import redis
# import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import cv2
import numpy as np

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

def video_stream():
    r = redis.Redis(host='localhost', port=6379)
    data = r.get('pose_frame')
    nparr = np.fromstring(data, np.uint8)
    newFrame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # cv2.imshow("s", newFrame)
    cv2image = cv2.cvtColor(newFrame, cv2.COLOR_BGR2RGBA)

    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, video_stream)

title = Button(root, text="Hi", command=video_stream)
title.pack()
root.mainloop()

# while True:
#     r = redis.Redis(host='localhost', port=6379)
#     data = r.get('pose_frame')
#     nparr = np.fromstring(data, np.uint8)
#     newFrame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#     cv2.imshow("s", newFrame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break




