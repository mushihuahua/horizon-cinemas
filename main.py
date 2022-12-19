from pymongo import MongoClient
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

cluster = "mongodb+srv://mushihuahua:TfOPb5fwlgyFMNHE@horizoncinemas.ldas1hn.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster)







class Staff:
    def __init__(self, employeeID, passwordHash, fullName, cinema, firstName, lastName):
        def __init__(self, employeeID, passwordHash, cinema, firstName, lastName):
            self.ID = employeeID
            self.passwordHash = passwordHash
            self.cinema = cinema
            self.firstName = firstName
            self.lastName = lastName
            fullName = self.firstName +' '+ self.lastName
            self.fullName = fullName
            self.fullName = self.firstName +' '+ self.lastName
        
    def get_passwordHash(self):
        def getPasswordHash(self):
            return self.passwordHash

    def set_passwordHash(self, passwordHash):
        def setPasswordHash(self, passwordHash):
            self.passwordHash = passwordHash
    
    def changePassword(self, newPass):
        self.passwordHash = newPass
    
    def __str__(self):
        return f"{self.fullName} {self.passwordHash}"

class BookingStaff: 
    def __init__(self, employeeID, passwordHash, fullName, cinema, firstName, lastName):
        super().__init__(employeeID, passwordHash, fullName, cinema, firstName, lastName)
        self.ID = employeeID
        self.passwordHash = passwordHash
        self.cinema = cinema
        self.firstName = firstName
        self.lastName = lastName
        fullName = self.firstName +' '+ self.lastName
        self.fullName = fullName
class BookingStaff(Staff): 
    def __init__(self, employeeID, passwordHash, cinema, firstName, lastName):
        super().__init__(employeeID, passwordHash, cinema, firstName, lastName)

class Manager: 
    def __init__(self, employeeID, passwordHash, fullName, cinema, firstName, lastName):
        super().__init__(employeeID, passwordHash, fullName, cinema, firstName, lastName)
        self.ID = employeeID
        self.passwordHash = passwordHash
        self.cinema = cinema
        self.firstName = firstName
        self.lastName = lastName
        fullName = self.firstName +' '+ self.lastName
        self.fullName = fullName
class Manager(BookingStaff): 
    def __init__(self, employeeID, passwordHash, cinema, firstName, lastName):
        super().__init__(employeeID, passwordHash, cinema, firstName, lastName)
    
class Admin: 
    def __init__(self, employeeID, passwordHash, fullName, cinema, firstName, lastName, report):
        super().__init__(employeeID, passwordHash, fullName, cinema, firstName, lastName)
        self.ID = employeeID
        self.passwordHash = passwordHash
        self.cinema = cinema
        self.firstName = firstName
        self.lastName = lastName
        fullName = self.firstName + ' ' + self.lastName
        self.fullName = fullName
class Admin(Manager): 
    def __init__(self, employeeID, passwordHash, cinema, firstName, lastName, report):
        super().__init__(employeeID, passwordHash, cinema, firstName, lastName)
        self.__report = report 
    
    def generateReport():
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


'''
test = Staff(1, "hi", "Steve Bannon", "test", "Steve", "Bannon")
print(test)
newPassword = "hello"
test.changePassword("hello")
print(test)
'''







class App(ctk.CTk):

    width = 1024
    height = 768
    x_pos = 0
    y_pos = 0

    def __init__(self):
        super().__init__()
        self.title("Horizon Cinemas")
        self.iconbitmap('icon.ico')
        self.geometry(f"{self.width}x{self.height}+{self.x_pos}+{self.y_pos}")


class MainFrame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)

        self.error = None

        self.loginFrame = ctk.CTkFrame(master=container, corner_radius=20)
        self.loginFrame.pack(pady=20, padx=60, fill="both", expand=True)

        self.loginLabel = ctk.CTkLabel(master=self.loginFrame, text="Employee Login", font=("Roboto", 48))
        self.loginLabel.pack(pady=container.width/12, padx=60)

        logo = ctk.CTkImage(Image.open('icon.png'), size=(250,200))
        self.logo = ctk.CTkLabel(master=self.loginFrame, text="", image=logo)
        self.logo.pack(pady=0)

        self.idEntry = ctk.CTkEntry(master=self.loginFrame, 
                        width=500, 
                        height=52, 
                        placeholder_text="Employee ID", 
                        font=("Roboto", 14))
        self.idEntry.pack(pady=20)
        self.idEntry.bind('<Return>', self.login)

        self.pwdEntry = ctk.CTkEntry(master=self.loginFrame, 
                        width=500, 
                        height=52, 
                        placeholder_text="Password", 
                        show="*", 
                        font=("Roboto", 14))
        self.pwdEntry.pack(pady=20)
        self.pwdEntry.bind('<Return>', self.login)

        self.loginButton = ctk.CTkButton(master=self.loginFrame, 
                        text="Login", 
                        width=250, 
                        height=52, 
                        font=("Roboto", 20),
                        command=self.login)
        self.loginButton.pack(pady=20)

    def login(self, event):
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
    #print(client.list_database_names())
    app = App()
    frame = MainFrame(app)
    app.mainloop()
