import customtkinter
from PIL import Image, ImageTk
import os

PATH = os.path.dirname(os.path.realpath(__file__))

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

# def enter_app():
#     login.quit()


def button_function():
    print("button pressed")

# login = customtkinter.CTk()
# login.geometry("600x260")
# login.title("Wellcome")
#
# login_button = customtkinter.CTkButton(master=login,text="login",command=enter_app)
# login_button.pack()
# login.mainloop()

app = customtkinter.CTk()
app.geometry("460x260")
app.title("METAFITT")


image_size = 60

# mic_image = ImageTk.PhotoImage(Image.open(PATH + "/bell.png").resize(image_size, image_size), Image.ANTIALIAS)
mic_image = ImageTk.PhotoImage(Image.open("mic2.png").resize((image_size, image_size), Image.ANTIALIAS))
game_image = ImageTk.PhotoImage(Image.open("game2.png").resize((image_size+15, image_size), Image.ANTIALIAS))

frame_1 = customtkinter.CTkFrame(master=app, width=250, height=240, corner_radius=20)
frame_1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# frame_2 = customtkinter.CTkFrame(master=app, width=250, height=240, corner_radius=40)
# frame_2.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")

# frame_1.grid_columnconfigure(0, weight=1)
# frame_1.grid_columnconfigure(1, weight=1)
# frame_1.grid_rowconfigure(0, minsize=10)

mic_button = customtkinter.CTkButton(master=frame_1, image=mic_image, text="voice recognition",width=190, height=40,corner_radius=20,
                                     compound="right", fg_color="#F1521F", hover_color="#D512C3", command=button_function)
mic_button.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

game_button = customtkinter.CTkButton(master=frame_1, image=game_image, text="unity game          ",width=190, height=40,corner_radius=20,
                                     compound="right", fg_color="#F1521F", hover_color="#D512C3", command=button_function)
game_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

app.mainloop()

