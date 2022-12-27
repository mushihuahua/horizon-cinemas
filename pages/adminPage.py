import customtkinter as ctk

class AdminFrame():
    def __init__(self, container):

        self.frame = ctk.CTkFrame(master=container, corner_radius=20)

        self.test = ctk.CTkLabel(master=self.frame, text="Admin")
        self.test.pack()