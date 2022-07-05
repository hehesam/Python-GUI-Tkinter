import tkinter

import customtkinter
from PIL import Image, ImageTk
import os
import subprocess
from pico_voice import pico

PATH = os.path.dirname(os.path.realpath(__file__))

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

# def enter_app():
#     login.quit()


def button_function():
    print("button pressed")


def start_voice(frame_1):
    blanket = customtkinter.CTkEntry(frame_1, width=190, height=40)
    blanket.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
    word = pico()
    blanket.insert(0, word)
    # subprocess.call(["gnome-terminal", "--", "sh", "-c", "python3 pico_voice.py"])

def start_game():
    subprocess.call(["gnome-terminal", "--", "sh", "-c", "./unity_game2/rope.x86_64"])


# login = customtkinter.CTk()
# login.geometry("600x260")
# login.title("Wellcome")
#
# login_button = customtkinter.CTkButton(master=login,text="login",command=enter_app)
# login_button.pack()
# login.mainloop()

app = customtkinter.CTk()
app.geometry("900x800")
app.title("METAFITT")


image_size = 60

back_image = ImageTk.PhotoImage(Image.open("resource/bg_gr3.jpg").resize((900, 800), Image.ANTIALIAS))
back_ground = tkinter.Label(master=app, image=back_image)
back_ground.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


mic_image = ImageTk.PhotoImage(Image.open("resource/mic2.png").resize((image_size, image_size), Image.ANTIALIAS))
game_image = ImageTk.PhotoImage(Image.open("resource/game2.png").resize((image_size+15, image_size), Image.ANTIALIAS))
pose_image = ImageTk.PhotoImage(Image.open("resource/man.png").resize((image_size, image_size-10), Image.ANTIALIAS))
exit_image = ImageTk.PhotoImage(Image.open("resource/exit.png").resize((image_size, image_size-10), Image.ANTIALIAS))

frame_0 = customtkinter.CTkFrame(master=app, width=300, height=700,border_width=3 ,corner_radius=20, border_color="#F1521F" ,fg_color="#1A1A1A")
frame_0.pack()

frame_1 = customtkinter.CTkFrame(master=frame_0, width=250, height=240, corner_radius=20)
frame_1.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

frame_2 = customtkinter.CTkFrame(master=frame_0, width=250, height=240, corner_radius=20)
frame_2.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
logo = ImageTk.PhotoImage(Image.open("resource/metafit2.jpg").resize((260, 240), Image.ANTIALIAS))
logo_set = tkinter.Label(master=frame_2, image=logo)
logo_set.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


mic_button = customtkinter.CTkButton(master=frame_1, image=mic_image, text="ٰVoice Control",width=190, height=40, corner_radius=20,
                                     compound="right", fg_color="#F1521F", hover_color="#01D7DA", command=lambda  : start_voice(frame_1))
mic_button.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

game_button = customtkinter.CTkButton(master=frame_1, image=game_image, text="Unity Game          ",width=190, height=40, corner_radius=20,
                                     compound="right", fg_color="#F1521F", hover_color="#01D7DA", command=start_game)
game_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

pose_button = customtkinter.CTkButton(master=frame_1, image=pose_image, text="Pose Estimation   ",width=190, height=40, corner_radius=20,
                                     compound="right", fg_color="#F1521F", hover_color="#01D7DA", command=start_game)
pose_button.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")


exit_button = customtkinter.CTkButton(master=frame_0, image=exit_image, text="EXIT",width=190, height=90,corner_radius=20,
                                     compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#E30C2A", command=app.quit)

exit_button.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")


app.mainloop()

