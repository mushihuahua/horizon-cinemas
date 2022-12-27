import customtkinter as ctk

class AccountFrame():
    def __init__(self, container):

        self.frame = ctk.CTkFrame(master=container, corner_radius=20)

        self.test = ctk.CTkLabel(master=self.frame, text="Account")
        self.test.pack()