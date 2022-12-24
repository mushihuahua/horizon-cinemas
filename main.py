from pymongo import MongoClient
from bson.objectid import ObjectId
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from werkzeug.security import generate_password_hash, check_password_hash
import os
import weakref
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

cluster = "mongodb+srv://mushihuahua:TfOPb5fwlgyFMNHE@horizoncinemas.ldas1hn.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster)

db = client.horizonCinemasDB
ERROR_COLOUR="#e23636"
SUCCESS_COLOUR="#66bb6a"

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
    
    def __str__(self):
        return f"{self.fullName} {self.passwordHash}"

class BookingStaff(Staff): 
    def __init__(self, employeeID, passwordHash, cinema, firstName, lastName):
        super().__init__(employeeID, passwordHash, cinema, firstName, lastName)

class Admin(BookingStaff): 
    def __init__(self, employeeID, passwordHash, cinema, firstName, lastName):
        super().__init__(employeeID, passwordHash, cinema, firstName, lastName)
        
    def generateReport(self):
        # Place holder
        self.__report = None
    
class Manager(Admin): 
    def __init__(self, employeeID, passwordHash, cinema, firstName, lastName):
        super().__init__(employeeID, passwordHash, cinema, firstName, lastName)

    def createNewEmployee(self, newFirstName, newLastName, newEmployeeID, newPasswordHash, newType):
        newEmployee = {
            "_id": newEmployeeID,
            "password_hash": newPasswordHash,
            "first_name": newFirstName,
            "last_name": newLastName,
            "type": newType,
            "cinema": ObjectId("63a22d895cbf5a11ca1f710e") # Change later
        }

        return db.staff.insert_one(newEmployee).acknowledged

class Report:
    def __init__(self, numberOfListingBookings=0, totalMonthlyRevenue=0, topFilm=0, staffBookings=0):
        self.__numberOfListingBookings = numberOfListingBookings
        self.__totalMonthlyRevenue = totalMonthlyRevenue
        self.__topFilm = topFilm
        self.__staffBookings = staffBookings

    def displayReport(self):
        pass


staffTypes = {
    "Booking Staff": BookingStaff,
    "Admin": Admin,
    "Manager": Manager
}

loggedInUser = Staff(0, "", 0, "", "")


'''
test = Staff(1, "hi", "Steve Bannon", "test", "Steve", "Bannon")
print(test)
newPassword = "hello"
test.changePassword("hello")
print(test)
'''

class App(ctk.CTk):

    width = 1920
    height = 1080
    x_pos = 0
    y_pos = 0

    def __init__(self):
        super().__init__()

        self.frames = []
        self.buttons = []

        self.title("Horizon Cinemas")
        if "nt" == os.name:
            self.iconbitmap(bitmap = "icon.ico")

        self.geometry(f"{self.width}x{self.height}+{self.x_pos}+{self.y_pos}")

    def switchFrame(self, frame, button):

        # Unpack all the view frames
        for i in self.frames:
            i.frame.pack_forget()
        
        # Pack the view frame switched to
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Return all buttons to normal
        for i in self.buttons:
            i.configure(border_width=0, fg_color="#bb86fc")

        # Change the button pressed to be highlighted
        button.configure(border_color="#e5d1fe", border_width=4, fg_color="#9f54fb")

class LoginFrame():
    def __init__(self, container):
        
        self.error = None
        self.container = container

        self.loginFrame = ctk.CTkFrame(master=container, corner_radius=20)

        self.loginLabel = ctk.CTkLabel(master=self.loginFrame, text="Employee Login", font=("Roboto", 48))
        self.loginLabel.pack(pady=85, padx=60)

        logo = ctk.CTkImage(Image.open('icon.png'), size=(250,200))
        self.logo = ctk.CTkLabel(master=self.loginFrame, text="", image=logo)
        self.logo.pack(pady=0)

        self.idEntry = ctk.CTkEntry(master=self.loginFrame, 
                        width=500, 
                        height=52, 
                        placeholder_text="Employee ID", 
                        font=("Roboto", 14))
        self.idEntry.pack(pady=20)
        self.idEntry.bind('<Return>', self.__login)

        self.pwdEntry = ctk.CTkEntry(master=self.loginFrame, 
                        width=500, 
                        height=52, 
                        placeholder_text="Password", 
                        show="*", 
                        font=("Roboto", 14))
        self.pwdEntry.pack(pady=20)
        self.pwdEntry.bind('<Return>', self.__login)

        self.loginButton = ctk.CTkButton(master=self.loginFrame, 
                        text="Login", 
                        width=250, 
                        height=52, 
                        font=("Roboto", 20),
                        fg_color="#bb86fc",
                        hover_color="#9f54fb",
                        command=self.__login)
        self.loginButton.pack(pady=20)

    def __login(self, event=None):

        # Get input from the entry widgets
        employeeID = self.idEntry.get()
        password = self.pwdEntry.get()

        # Make sure the employee id inputted is a number
        try:
            employeeID = int(employeeID)
            if(self.error != None):
                self.error.pack_forget()

            # Make sure that employee id is 6 digits
            if(len(str(employeeID)) != 6):
                self.error = ctk.CTkLabel(master=self.loginFrame, text="Employee ID should be a 6 digit number", text_color=ERROR_COLOUR, font=("Roboto", 18))
                self.error.pack()
                return

            # Try to find an entry in db with employeeID and check if it exists
            result = db.staff.find_one({"_id": employeeID})
            if(result != None):

                # Get the password hash related to that employee ID if it exists and check if the password entered is correct
                hash = result.get("password_hash")
                if(check_password_hash(hash, password)):
                    print(f"Login Successful")
                    global loggedInUser

                    staffType = result.get("type")

                    loggedInUser = staffTypes[staffType](result.get("_id"), result.get("password_hash"), result.get("cinema"), result.get("first_name"), result.get("last_name"))

                    # If login is successful show the view menu and the main page
                    menu.menuFrame.pack(fill="both")
                    menu.bookingStaffButton.configure(border_color="#e5d1fe", border_width=4, fg_color="#9f54fb")
                    loginView.loginFrame.pack_forget()
                    self.container.switchFrame(mainView.frame, menu.bookingStaffButton)

                    # Go through all instances of InfoFrame and change the employeeLabel text to the logged in user's information
                    for info in InfoFrame.infoList:
                        info.employeeLabel.configure(text=f"{loggedInUser.fullName} - {loggedInUser.__class__.__name__}")

                else:
                    # Clear the password entry field
                    self.pwdEntry.delete(0, "end")

                    # More error checking
                    if(len(str(password)) < 8 or len(str(password)) > 16):
                        self.error = ctk.CTkLabel(master=self.loginFrame, text="The password should be 8 to 16 characters long", text_color=ERROR_COLOUR, font=("Roboto", 18))
                        self.error.pack()
                        return
                    self.error = ctk.CTkLabel(master=self.loginFrame, text="The password you entered is incorrect, try again", text_color=ERROR_COLOUR, font=("Roboto", 18))
                    self.error.pack()
                    return
            else:
                self.error = ctk.CTkLabel(master=self.loginFrame, text="Employee ID does not exist", text_color=ERROR_COLOUR, font=("Roboto", 18))
                self.error.pack()
                return

        except ValueError:
            if(self.error != None):
                self.error.pack_forget()
            self.error = ctk.CTkLabel(master=self.loginFrame, text="Employee ID should be a number", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()

class MainFrame():
    def __init__(self, container):

        self.frame = ctk.CTkFrame(master=container, corner_radius=20)

        self.test = ctk.CTkLabel(master=self.frame, text="Main")
        self.test.pack()

class AdminFrame():
    def __init__(self, container):

        self.frame = ctk.CTkFrame(master=container, corner_radius=20)

        self.test = ctk.CTkLabel(master=self.frame, text="Admin")
        self.test.pack()

class InfoFrame():
    infoList = []
    def __init__(self, container):
        self.__class__.infoList.append(weakref.proxy(self))
        self.employeeLabel = ctk.CTkLabel(master=container,
                                    font=("Roboto", 16))

        self.cinemaLabel = ctk.CTkLabel(master=container, 
                            text="Bristol, Cabot Circus",
                            font=("Roboto", 16))
class ManagerFrame():
    def __init__(self, container):

        self.frames = []
        self.error = None
        self.successMessage = None

        self.frame = ctk.CTkFrame(master=container, corner_radius=20)

        self.inFrame = ctk.CTkFrame(master=self.frame, corner_radius=20)
        self.createAccountFrame = ctk.CTkFrame(master=self.frame, corner_radius=20)

        self.frames.append(self.inFrame)
        self.frames.append(self.createAccountFrame)

        self.buttonsFrame = ctk.CTkFrame(master=self.frame, corner_radius=20)

        self.info = InfoFrame(self.inFrame)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)

        self.text = ctk.CTkLabel(master=self.inFrame, 
                            text="Manager View",
                            font=("Roboto", 48))

        self.addCityButton = ctk.CTkButton(master=self.buttonsFrame, 
                                    text="Add City", 
                                    width=250,
                                    height=75,
                                    font=("", 18, "bold"), 
                                    corner_radius=7,
                                    fg_color="#9f54fb",
                                    hover_color="#a722fa")

        self.addCinemaButton = ctk.CTkButton(master=self.buttonsFrame, 
                                    text="Add Cinema", 
                                    width=250,
                                    height=75,
                                    font=("", 18, "bold"), 
                                    corner_radius=7,
                                    fg_color="#9f54fb",
                                    hover_color="#a722fa")

        self.viewEmployeesButton = ctk.CTkButton(master=self.buttonsFrame, 
                                    text="View Staff Members", 
                                    width=400,
                                    height=75,
                                    font=("", 18, "bold"), 
                                    corner_radius=7,
                                    fg_color="#9f54fb",
                                    hover_color="#a722fa")

        self.createEmployeeAccount = ctk.CTkButton(master=self.buttonsFrame, 
                                    text="Create Staff Member Account", 
                                    width=400,
                                    height=75,
                                    font=("", 18, "bold"), 
                                    corner_radius=7,
                                    fg_color="#9f54fb",
                                    hover_color="#a722fa",
                                    command=lambda: self.switchFrames(self.createAccountFrame))

        self.createLabel = ctk.CTkLabel(master=self.createAccountFrame, text="Create Staff Member Account", font=("Roboto", 32))
        self.createLabel.pack(pady=40, padx=30)

        self.firstNameEntry = ctk.CTkEntry(master=self.createAccountFrame, 
                        width=500, 
                        height=52, 
                        placeholder_text="First Name", 
                        font=("Roboto", 14))
        self.firstNameEntry.pack(pady=20)
        self.firstNameEntry.bind('<Return>', self.__createAccount)

        self.lastNameEntry = ctk.CTkEntry(master=self.createAccountFrame, 
                        width=500, 
                        height=52, 
                        placeholder_text="Last Name", 
                        font=("Roboto", 14))
        self.lastNameEntry.pack(pady=20)
        self.lastNameEntry.bind('<Return>', self.__createAccount)

        self.typeValue = ctk.StringVar(master=self.createAccountFrame)
        self.typeValue.set("Select Staff Type")
        types = ["Booking Staff", "Admin", "Manager"]

        self.staffType = ctk.CTkOptionMenu(master=self.createAccountFrame,
                                    fg_color="#bb86fc",
                                    button_color="#9f54fb",
                                    button_hover_color="#a722fa", 
                                    variable=self.typeValue, 
                                    values=types,
                                    width=500, 
                                    height=52)

        self.staffType.pack(pady=20)

        self.idEntry = ctk.CTkEntry(master=self.createAccountFrame, 
                        width=500, 
                        height=52, 
                        placeholder_text="Employee ID", 
                        font=("Roboto", 14))
        self.idEntry.pack(pady=20)
        self.idEntry.bind('<Return>', self.__createAccount)


        self.pwdEntry = ctk.CTkEntry(master=self.createAccountFrame, 
                        width=500, 
                        height=52, 
                        placeholder_text="Password",
                        show="*",
                        font=("Roboto", 14))
        self.pwdEntry.pack(pady=20)
        self.pwdEntry.bind('<Return>', self.__createAccount)

        self.createButton = ctk.CTkButton(master=self.createAccountFrame, 
                        text="Create Account", 
                        width=250, 
                        height=52, 
                        font=("Roboto", 20),
                        fg_color="#bb86fc",
                        hover_color="#9f54fb",
                        command=self.__createAccount)

        self.createButton.pack(pady=20)        

        self.inFrame.pack(pady=20, padx=20, fill="both", expand=True)
        self.text.place(relx=.5, rely=.2, anchor="center")
        self.info.employeeLabel.place(relx=.5, rely=.3, anchor="center")
        self.info.cinemaLabel.place(relx=.5, rely=.35, anchor="center")

        self.buttonsFrame.pack(fill="both", padx=20)
        self.addCityButton.grid(row=1, column=0, sticky="news", padx=(160, 25), pady=25)
        self.addCinemaButton.grid(row=1, column=1, sticky="news", padx=(25, 25), pady=25)
        self.viewEmployeesButton.grid(row=1, column=2, sticky="news", padx=(25, 25), pady=25)
        self.createEmployeeAccount.grid(row=1, column=3, sticky="news", padx=(25, 160), pady=25)

    def __createAccount(self, event=None):

        firstName = self.firstNameEntry.get()
        lastName = self.lastNameEntry.get()
        id = self.idEntry.get()
        pwd = self.pwdEntry.get()
        empType = self.typeValue.get()

        if(self.error != None):
            self.error.pack_forget()
        
        if(self.successMessage != None):
            self.successMessage.pack_forget()

        if(len(firstName) <= 1):
            self.error = ctk.CTkLabel(master=self.createAccountFrame, text="Invalid first name", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return   
        
        if(len(lastName) <= 1):
            self.error = ctk.CTkLabel(master=self.createAccountFrame, text="Invalid last name", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return   

        try:
            id = int(id)

            if(empType == "Select Staff Type"):
                self.error = ctk.CTkLabel(master=self.createAccountFrame, text="Select a Staff Type", text_color=ERROR_COLOUR, font=("Roboto", 18))
                self.error.pack()
                return

            if(len(str(id)) != 6):
                self.error = ctk.CTkLabel(master=self.createAccountFrame, text="Employee ID should be a 6 digit number", text_color=ERROR_COLOUR, font=("Roboto", 18))
                self.error.pack()
                return

            if(db.staff.find_one({"_id": id}) != None):
                self.error = ctk.CTkLabel(master=self.createAccountFrame, text="Employee ID already exists", text_color=ERROR_COLOUR, font=("Roboto", 18))
                self.error.pack()
                return

            if(len(str(pwd)) < 8 or len(str(pwd)) > 16):
                self.error = ctk.CTkLabel(master=self.createAccountFrame, text="The password should be 8 to 16 characters long", text_color=ERROR_COLOUR, font=("Roboto", 18))
                self.error.pack()
                return

            success = False
            if(type(loggedInUser) is Manager):
                success = loggedInUser.createNewEmployee(firstName, lastName, id, generate_password_hash(pwd), empType)

            if(success):
                self.successMessage = ctk.CTkLabel(master=self.createAccountFrame, text="Employee account created successfully", text_color=SUCCESS_COLOUR, font=("Roboto", 18))
                self.successMessage.pack()

                self.firstNameEntry.delete(0, "end")
                self.lastNameEntry.delete(0, "end")
                self.idEntry.delete(0, "end")
                self.pwdEntry.delete(0, "end")
                self.typeValue.set("Select Staff Type")


            else:
                self.error = ctk.CTkLabel(master=self.createAccountFrame, text="Error occured, account could not be created", text_color=ERROR_COLOUR, font=("Roboto", 18))
                self.error.pack()


        except ValueError:
            if(self.error != None):
                self.error.pack_forget()
            self.error = ctk.CTkLabel(master=self.createAccountFrame, text="Employee ID should be a number", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()


    def switchFrames(self, frame):

        self.buttonsFrame.pack_forget()

        # Unpack all the view frames
        for i in self.frames:
            i.pack_forget()
        
        # Pack the view frame switched to
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.buttonsFrame.pack(fill="both", padx=20)



class AccountFrame():
    def __init__(self, container):

        self.frame = ctk.CTkFrame(master=container, corner_radius=20)

        self.test = ctk.CTkLabel(master=self.frame, text="Account")
        self.test.pack()


class MenuFrame():
    def __init__(self, container):

        self.container = container

        self.menuFrame = ctk.CTkFrame(master=container, 
                                width=app.width, 
                                border_width=1, 
                                border_color="black")

        buttonPaddingX = 25

        # Create the buttons to allow for view switching
        self.bookingStaffButton = ctk.CTkButton(master=self.menuFrame, 
                                    text="Booking", 
                                    width=250,
                                    height=75,
                                    font=("", 16, "bold"), 
                                    corner_radius=7,
                                    fg_color="#bb86fc",
                                    hover_color="#9f54fb",
                                    command=lambda: container.switchFrame(mainView.frame, self.bookingStaffButton))

        self.adminButton = ctk.CTkButton(master=self.menuFrame, 
                                    text="Admin View",
                                    width=250,
                                    height=75,
                                    font=("", 16, "bold"),
                                    corner_radius=7,
                                    fg_color="#bb86fc",
                                    hover_color="#9f54fb",
                                    command=lambda: container.switchFrame(adminView.frame, self.adminButton))

        self.managerButton = ctk.CTkButton(master=self.menuFrame, 
                                    text="Manager View",
                                    width=250,
                                    height=75,
                                    font=("", 16, "bold"),
                                    corner_radius=7,
                                    fg_color="#bb86fc",
                                    hover_color="#9f54fb",
                                    command=lambda: container.switchFrame(managerView.frame, self.managerButton))

        self.accountButton = ctk.CTkButton(master=self.menuFrame, 
                                    text="Account",
                                    width=250,
                                    height=75,
                                    font=("", 16, "bold"),
                                    corner_radius=7,
                                    fg_color="#bb86fc",
                                    hover_color="#9f54fb",
                                    command=lambda: container.switchFrame(accountView.frame, self.accountButton))
        
        self.logoutButton = ctk.CTkButton(master=self.menuFrame, 
                            text="Logout",
                            width=150,
                            height=75,
                            font=("", 16, "bold"),
                            corner_radius=7,
                            fg_color="#ff0266",
                            hover_color="#e8005c",
                            border_color="#ff1c75",
                            border_width=1,
                            command=self.__logout)

        # Put them on the GUI Grid inline and append them to a buttons array
        self.bookingStaffButton.place(relx=.1, rely=.5, anchor="center")
        self.adminButton.place(relx=.25, rely=.5, anchor="center")
        self.managerButton.place(relx=.4, rely=.5, anchor="center")
        self.accountButton.place(relx=.55, rely=.5, anchor="center")
        self.logoutButton.place(relx=.95, rely=.5, anchor="center")
        container.buttons.append(self.bookingStaffButton)
        container.buttons.append(self.adminButton)
        container.buttons.append(self.managerButton)
        container.buttons.append(self.accountButton)

    def __logout(self):
        menu.menuFrame.pack_forget()
        
        for frame in self.container.frames:
            frame.frame.pack_forget()
        
        loginView.loginFrame.pack(pady=20, padx=60, fill="both", expand=True)
        loginView.pwdEntry.delete(0, "end")
        loginView.idEntry.delete(0, "end")

        loggedInUser = Staff(0, "", 0, "", "")


if(__name__ == "__main__"):
    # print(client.list_database_names())
    app = App()

    menu = MenuFrame(app)
    loginView = LoginFrame(app)
    mainView = MainFrame(app)
    adminView = AdminFrame(app)
    managerView = ManagerFrame(app)
    accountView = AccountFrame(app)

    
    # app.frames.append(loginView)
    app.frames.append(mainView)
    app.frames.append(managerView)
    app.frames.append(adminView)
    app.frames.append(accountView)
    
    loginView.loginFrame.pack(pady=20, padx=60, fill="both", expand=True)
    # menu.menuFrame.pack(fill="both")
    # menu.bookingStaffButton.configure(border_color="#e5d1fe", border_width=4, fg_color="#9f54fb")
    # loginView.loginFrame.pack_forget()
    # mainView.frame.pack(pady=20, padx=60, fill="both", expand=True)

    app.mainloop()
