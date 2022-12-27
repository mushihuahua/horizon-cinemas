from pymongo import MongoClient
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from werkzeug.security import generate_password_hash, check_password_hash
import os
from tkcalendar import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

cluster = "mongodb+srv://mushihuahua:TfOPb5fwlgyFMNHE@horizoncinemas.ldas1hn.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster)

db = client.horizonCinemasDB
loggedInUser = None

ERROR_COLOUR="#e23636"

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
        else:
            pass

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
                    loggedInUser = result
                    # If login is successful show the view menu and the main page
                    menu.menuFrame.pack(fill="both")
                    menu.bookingStaffButton.configure(border_color="#e5d1fe", border_width=4, fg_color="#9f54fb")
                    loginView.loginFrame.pack_forget()
                    self.container.switchFrame(mainView.frame, menu.bookingStaffButton)

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

# Booking View
class MainFrame():
    def __init__(self, container):

        from datetime import datetime
        date = datetime.today().strftime('%Y-%m-%d')
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:])

        self.frame = ctk.CTkFrame(master=container, corner_radius=10)

        self.viewTitle = ctk.CTkLabel(master=self.frame, text="Bookings", font=("Roboto", 48))
    
        self.calendarLabel = ctk.CTkLabel(master=self.frame, text="Select Date:", font=("Roboto", 15))
        self.calendar = Calendar(master=self.frame, 
                        selectmode='day', 
                        year=year, 
                        month=month, 
                        day=day)
    
        self.selectFilmLabel = ctk.CTkLabel(master=self.frame, text="Select Film:", font=("Roboto", 15))
        self.selectFilm = ctk.CTkOptionMenu(master=self.frame, 
                            values=["Film 1", "Film 2", "Etc."],
                            width=200,
                            height=30,
                            font=("", 16, "bold"),
                            corner_radius=4)
        self.selectShowingLabel = ctk.CTkLabel(master=self.frame, text="Select Showing:", font=("Roboto", 15))    
        self.selectShowing = ctk.CTkOptionMenu(master=self.frame, 
                            values=["Showing 1", "Showing 2", "Etc."],
                            width=200,
                            height=30,
                            font=("", 16, "bold"),
                            corner_radius=4)  
        self.maxSeatsLabel = ctk.CTkLabel(master=self.frame, text="Max Seats:", font=("Roboto", 15)) 
        self.maxSeats = ctk.CTkLabel(master=self.frame, text="0", font=("Roboto", 15)) 
        self.selectTicketsLabel = ctk.CTkLabel(master=self.frame, text="Select Tickets", font=("Roboto", 18)) 
        self.lowTicketsLabel = ctk.CTkLabel(master=self.frame, text="Lower Hall Tickets:", font=("Roboto", 15)) 
        self.lowHallTickets = ctk.CTkOptionMenu(master=self.frame, 
                            values=["1", "2", "Etc."],
                            width=200,
                            height=30,
                            font=("", 16, "bold"),
                            corner_radius=4)    
        self.upperTicketsLabel = ctk.CTkLabel(master=self.frame, text="Upper Hall Tickets:", font=("Roboto", 15)) 
        self.upperHallTickets = ctk.CTkOptionMenu(master=self.frame, 
                            values=["1", "2", "Etc."],
                            width=200,
                            height=30,
                            font=("", 16, "bold"),
                            corner_radius=4) 
        self.vipTicketsLabel = ctk.CTkLabel(master=self.frame, text="VIP Tickets:", font=("Roboto", 15)) 
        self.vipHallTickets = ctk.CTkOptionMenu(master=self.frame, 
                            values=["1", "2", "Etc."],
                            width=200,
                            height=30,
                            font=("", 16, "bold"),
                            corner_radius=4)                                     
        self.totalPriceLabel = ctk.CTkLabel(master=self.frame, text="Total Price:", font=("Roboto", 15)) 
        self.totalPrice = ctk.CTkLabel(master=self.frame, text="£0", font=("Roboto", 18)) 
        self.makeBookingButton = ctk.CTkButton(master=self.frame, 
                                    text="Make Booking",
                                    width=200,
                                    height=40,
                                    font=("", 16, "bold"),
                                    corner_radius=7)

        self.viewBookingsButton = ctk.CTkButton(master=self.frame, 
                                    text="View Bookings",
                                    width=200,
                                    height=40,
                                    font=("", 16, "bold"),
                                    corner_radius=7,
                                    fg_color="#bb86fc",
                                    hover_color="#9f54fb")

        self.col0 = ctk.CTkLabel(master=self.frame, text=" ", width=300, height=40) 
        self.row2 = ctk.CTkLabel(master=self.frame, text=" ", width=300, height=90) 
    
        self.calendarLabel.grid(row=1, column=1)
        self.calendar.place(relx=.48, rely=.29, anchor="center")

        self.viewTitle.grid(row=0, column=2, pady=30, padx=60)
        self.viewBookingsButton.grid(row=1, column=3, pady=10, padx=10)

        self.selectFilmLabel.grid(row=3, column=1)
        self.selectFilm.grid(row=3, column=2, pady=10, padx=10)
        self.selectShowingLabel.grid(row=4, column=1)
        self.selectShowing.grid(row=4, column=2, pady=10, padx=10)
        self.selectTicketsLabel.grid(row=6, column=2, pady=10, padx=10)
        self.lowTicketsLabel.grid(row=7, column=1)
        self.lowHallTickets.grid(row=8, column=1, pady=10, padx=10)
        self.upperTicketsLabel.grid(row=7, column=2)
        self.upperHallTickets.grid(row=8, column=2, pady=10, padx=10)
        self.vipTicketsLabel.grid(row=7, column=3)
        self.vipHallTickets.grid(row=8, column=3, pady=10, padx=10)
        self.totalPriceLabel.grid(row=9, column=1, pady=10, padx=10)
        self.totalPrice.grid(row=9, column=2, pady=10, padx=10)
        self.makeBookingButton.grid(row=10, column=2, pady=10, padx=10)
        
        self.col0.grid(row=0, column=0)
        self.row2.grid(row=2, column=0)
        

class AdminFrame():
    def __init__(self, container):

        self.frame = ctk.CTkFrame(master=container, corner_radius=20)

        self.test = ctk.CTkLabel(master=self.frame, text="Admin")
        self.test.pack()

class ManagerFrame():
    def __init__(self, container):

        self.frame = ctk.CTkFrame(master=container, corner_radius=20)

        self.test = ctk.CTkLabel(master=self.frame, text="Manager")
        self.test.pack()

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

        self.menuFrame.grid_rowconfigure(0, weight=1)
        self.menuFrame.grid_columnconfigure(0, weight=1)

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
        ''' (app.width/6.5) '''
        self.bookingStaffButton.grid(row=0, column=0, padx=(buttonPaddingX, buttonPaddingX), pady=(37, 37))
        self.adminButton.grid(row=0, column=1, padx=(buttonPaddingX, buttonPaddingX), pady=(37, 37))
        self.managerButton.grid(row=0, column=2, padx=(buttonPaddingX, buttonPaddingX), pady=(37, 37))
        self.accountButton.grid(row=0, column=3, padx=(buttonPaddingX, 0), pady=(37, 37))
        self.logoutButton.grid(row=0, column=4, padx=(275, 50), pady=(37, 37))
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

        loggedInUser = None


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
    menu.menuFrame.pack(fill="both")
    menu.bookingStaffButton.configure(border_color="#e5d1fe", border_width=4, fg_color="#9f54fb")
    loginView.loginFrame.pack_forget()
    mainView.frame.pack(pady=20, padx=60, fill="both", expand=True)

    app.mainloop()


# 123456
# randompass