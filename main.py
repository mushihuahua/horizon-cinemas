from pymongo import MongoClient
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

cluster = "mongodb+srv://mushihuahua:TfOPb5fwlgyFMNHE@horizoncinemas.ldas1hn.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster)

class Staff:
    def __init__(self, employeeID, passwordHash, cinema, firstName, lastName):
        self.ID = employeeID
        self.passwordHash = passwordHash
        self.cinema = cinema
        self.firstName = firstName
        self.lastName = lastName
        self.fullName = self.firstName +' '+ self.lastName
        
    def getPasswordHash(self):
        return self.passwordHash

    def setPasswordHash(self, passwordHash):
        self.passwordHash = passwordHash
    
    def changePassword(self, newPass):
        self.passwordHash = newPass

class BookingStaff(Staff): 
    def __init__(self, employeeID, passwordHash, cinema, firstName, lastName):
        super().__init__(employeeID, passwordHash, cinema, firstName, lastName)

class Manager(BookingStaff): 
    def __init__(self, employeeID, passwordHash, cinema, firstName, lastName):
        super().__init__(employeeID, passwordHash, cinema, firstName, lastName)
    
class Admin(Manager): 
    def __init__(self, employeeID, passwordHash, cinema, firstName, lastName, report):
        super().__init__(employeeID, passwordHash, cinema, firstName, lastName)
        self.__report = report 
    
    def generateReport(self):
        pass

class Report: 
    def __init__(self, numberOfListingBookings, totalMonthlyRevenue, topFilm, staffBookings):
        self.__numberOfListingBookings = numberOfListingBookings
        self.__totalMonthlyRevenue = totalMonthlyRevenue
        self.__topFilm = topFilm
        self.__staffBookings = staffBookings

    def displayReport(self):
        pass


class App(ctk.CTk):

    width = 1024
    height = 768

    def __init__(self):
        super().__init__()
        self.title("Horizon Cinemas")
        self.geometry(f"{self.width}x{self.height}")

class MainFrame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)

        self.error = None

        self.loginFrame = ctk.CTkFrame(master=container)
        self.loginFrame.pack(pady=20, padx=60, fill="both", expand=True)

        self.loginLabel = ctk.CTkLabel(master=self.loginFrame, text="Employee Login", font=("Roboto", 48))
        self.loginLabel.pack(pady=container.width/12, padx=60)

        self.idEntry = ctk.CTkEntry(master=self.loginFrame, width=500, height=52, placeholder_text="Employee ID", font=("Roboto", 14))
        self.idEntry.pack(pady=20)

        self.pwdEntry = ctk.CTkEntry(master=self.loginFrame, width=500, height=52, placeholder_text="Password", show="*", font=("Roboto", 14))
        self.pwdEntry.pack(pady=20)

        self.loginButton = ctk.CTkButton(master=self.loginFrame, text="Login", width=250, height=52, command=self.login)
        self.loginButton.pack(pady=20)

    def login(self):
        employeeID = self.idEntry.get()
        password = self.pwdEntry.get()
        try:
            employeeID = int(employeeID)
            if(self.error != None):
                self.error.pack_forget()
        except:
            if(self.error != None):
                self.error.pack_forget()
            self.error = ctk.CTkLabel(master=self.loginFrame, text="Employee ID should be a number", text_color="red")
            self.error.pack()
        print(f"ID:{employeeID}\nPWD:{password}")



if(__name__ == "__main__"):
    print(client.list_database_names())
    app = App()
    frame = MainFrame(app)
    app.mainloop()
