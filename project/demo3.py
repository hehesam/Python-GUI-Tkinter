import tkinter
import customtkinter
from PIL import Image, ImageTk
import os
import subprocess
import redis
import threading
import time
from tkinter import END


class sampleApp(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.title("main")
        self.geometry('1600x900')
        self.voice_state = False

        container = customtkinter.CTkFrame(master=self, width=900, height=700)

        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        switch_frame = customtkinter.CTkFrame(master=self, width=900, height=100)
        switch_frame.pack(side='bottom', fill='both', expand=True)
        self.switch_frame = switch_frame
        self.state = customtkinter.CTkEntry(self.switch_frame)
        self.state.pack(side='right', fill='both')

        voice_switch = customtkinter.CTkSwitch(master=switch_frame, text="Voice Control", width=72,
                                              height=30, corner_radius=20, fg_color="#F1521F",
                                              command=lambda : self.voice())
        # voice_switch.grid(row=4, column=4, columnspan=2, padx=20, pady=10, sticky="nsew")
        voice_switch.pack(side='left', fill='both')
        # voice_switch.grid_rowconfigure(0, weight=1)
        # voice_switch.grid_columnconfigure(0, weight=1)


        self.frames = {}

        for F in (mainPage, UnityGame, PoseEstimation):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            # frame.pack()

        self.show_frame("mainPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def voice(self):
        self.voice_thread = threading.Thread(target=self.read_voice)
        # self.voice_thread.join()

        if self.voice_state == False:
            # subprocess.run(["gnome-terminal", "--", "sh", "-c", "python3 pico_voice.py"], shell=True) # show the terminal "gnome-terminal", "--",
            self.voice_state = True
            self.voice_thread.start()
        else:
            self.voice_state = False

    def read_voice(self):
        r = redis.Redis(host='localhost', port=6379)
        r.set("start pico process", 1)
        while True:
            if not self.voice_state:
                self.state.insert(0, "stopped listening")
                r.set("end pico process", 1)
                break
            start_state = int(r.get("engine start"))
            stop_state = int(r.get("engine stop"))
            if stop_state or start_state:
                if stop_state :
                    self.state.delete(0,END)
                    self.state.insert(0, 'stop')

                if start_state :
                    self.state.delete(0,END)
                    self.state.insert(0, 'start')
                time.sleep(1)
                self.state.delete(0, END)


class mainPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        self.controller = controller

        image_size = 60

        mic_image = ImageTk.PhotoImage(Image.open("resource/mic2.png").resize((image_size, image_size), Image.ANTIALIAS))
        game_image = ImageTk.PhotoImage(Image.open("resource/game2.png").resize((image_size + 15, image_size), Image.ANTIALIAS))
        pose_image = ImageTk.PhotoImage(Image.open("resource/man.png").resize((image_size, image_size - 10), Image.ANTIALIAS))
        exit_image = ImageTk.PhotoImage(Image.open("resource/exit.png").resize((image_size, image_size - 10), Image.ANTIALIAS))


        frame_0 = customtkinter.CTkFrame(master=self, width=300, height=700,border_width=3 ,corner_radius=20, border_color="#F1521F" ,fg_color="#1A1A1A")
        frame_0.pack()

        label_1 = customtkinter.CTkLabel(frame_0, text="this is the main page",width=190, height=90,)
        label_1.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")



        game_button = customtkinter.CTkButton(master=frame_0, image=game_image, text="Unity Game          ", width=190,
                                              height=40, corner_radius=20,
                                              compound="right", fg_color="#F1521F", hover_color="#01D7DA",
                                              command=lambda : controller.show_frame("UnityGame"))

        game_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")



        pose_button = customtkinter.CTkButton(master=frame_0, image=pose_image, text="Pose Estimation   ", width=190,
                                              height=40, corner_radius=20,
                                              compound="right", fg_color="#F1521F", hover_color="#01D7DA",
                                              command=lambda : controller.show_frame("PoseEstimation"))
        pose_button.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")



        exit_button = customtkinter.CTkButton(master=frame_0, text="EXIT",width=210, height=90,corner_radius=20,
                                     compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#E30C2A", command=self.quit)
        exit_button.grid(row=5, column=0, padx=20, pady=20, sticky="nsew")


class UnityGame(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        self.controller = controller

        frame_1 = customtkinter.CTkFrame(master=self, width=700, height=600,border_width=3 ,corner_radius=20, border_color="#F1521F" ,fg_color="#1A1A1A")
        frame_1.pack()

        frame_0 = customtkinter.CTkFrame(master=self, width=300, height=700,border_width=3 ,corner_radius=20, border_color="#F1521F" ,fg_color="#1A1A1A")
        frame_0.pack()


        start_button = customtkinter.CTkButton(master=frame_0, text="Start Game", width=190,
                                              height=40, corner_radius=20,
                                              compound="right", fg_color="#F1521F", hover_color="#01D7DA",
                                              command=lambda : self.startGame())

        start_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")



        back_button = customtkinter.CTkButton(master=frame_0, text="Back   ", width=190,
                                              height=40, corner_radius=20,
                                              compound="right", fg_color="#F1521F", hover_color="#01D7DA",
                                              command=lambda : controller.show_frame("mainPage"))
        back_button.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")


    def startGame(self):
        # subprocess.call(["gnome-terminal", "--", "sh", "-c", "./unity_game2/rope.x86_64"])
        r = redis.Redis(host='localhost', port=6379)
        r.set("start unity process", 1)



class PoseEstimation(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        self.controller = controller

        label = customtkinter.CTkLabel(self, text="PoseEstimation")
        label.pack()

        button1 = customtkinter.CTkButton(self, text="go to main page",
                                          command=lambda: controller.show_frame("mainPage"))

        button1.pack()

app = sampleApp()
subprocess.run(   ["gnome-terminal", "--" , "sh", "-c", "python3 control_panel.py"])

app.mainloop()