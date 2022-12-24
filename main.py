from pymongo import MongoClient
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from werkzeug.security import generate_password_hash, check_password_hash
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

cluster = "mongodb+srv://mushihuahua:TfOPb5fwlgyFMNHE@horizoncinemas.ldas1hn.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster)

db = client.horizonCinemasDB

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

    width = 1024
    height = 768
    x_pos = 0
    y_pos = 0

    def __init__(self):
        super().__init__()
        self.title("Horizon Cinemas")
        if "nt" == os.name:
            self.wm_iconbitmap(bitmap = "icon.ico")
        else:
            pass
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

    def login(self, event=None):

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
                self.error = ctk.CTkLabel(master=self.loginFrame, text="Employee ID should be a 6 digit number", text_color="red", font=("Roboto", 18))
                self.error.pack()
                return

            # Try to find an entry in db with employeeID and check if it exists
            result = db.staff.find_one({"_id": employeeID})
            if(result != None):

                # Get the password hash related to that employee ID if it exists and check if the password entered is correct
                hash = result.get("password_hash")
                if(check_password_hash(hash, password)):
                    print(f"Login Successful")
                else:
                    # Clear the password entry field
                    self.pwdEntry.delete(0, "end")

                    # More error checking
                    if(len(str(password)) < 8 or len(str(password)) > 16):
                        self.error = ctk.CTkLabel(master=self.loginFrame, text="The password should be 8 to 16 characters long", text_color="red", font=("Roboto", 18))
                        self.error.pack()
                        return
                    self.error = ctk.CTkLabel(master=self.loginFrame, text="The password you entered is incorrect, try again", text_color="red", font=("Roboto", 18))
                    self.error.pack()
                    return
            else:
                self.error = ctk.CTkLabel(master=self.loginFrame, text="Employee ID does not exist", text_color="red", font=("Roboto", 18))
                self.error.pack()
                return

        except:
            if(self.error != None):
                self.error.pack_forget()
            self.error = ctk.CTkLabel(master=self.loginFrame, text="Employee ID should be a number", text_color="red", font=("Roboto", 18))
            self.error.pack()


class cinema:
    def __init__(self, city, location, screens, listings, booking, staffMembers):
        self.__city = city
        self.__location = location
        self.__screens = screens
        self.__listings = listings
        self.__booking = booking
        self.__staffMembers = staffMembers
        
    def getListings(self):
        return listing
    
    def makeBooking(self, makeBooking, booking):
        makeBooking = booking
    
    def cancelBooking(self, bookingReference):
        pass

    def addListing(self, listings): 
        pass

    def removeListing(self, Listing):
        pass

    def hireStaffMember(self, newStaff):
        pass

    def removeStaffMember(self):
        pass

    def addScreen(self):
        pass

    def removeScreen(self):
        pass

    def getCity():
        pass
    
class cityContainer: 
    def __init__(self, city):
        self.__city = city

    def addCity(self):
        pass

class city:
    def __init__(self, name, morningPrice, afternoonPrice, eveningPrice, cinema):
        self.__name = name
        self.__morningPrice = morningPrice
        self.__afternoonPrice = afternoonPrice
        self.__eveningPrice = eveningPrice
        self.__cinema = cinema

    def getTicketPrice():
        pass

class listing: 
    def __init__(self,filmName, filmDate, filmDescription, actorDetails,filmGenre,filmAge, filmRating, shows):
        self.__filmName = filmName
        self.__filmDate = filmDate
        self.__filmDescription = filmDescription
        self.__actorDetails = actorDetails
        self.__filmGenre = filmGenre
        self.__filmAge = filmAge
        self.__filmRating = filmRating
        self.__shows = shows

    def getListingInformation(self):
        pass

    def changeListingInformation(self):
        pass
    
    def getShows(self):
        pass

    def getFilmName(self):
        pass

    def getFilmDate(self):
        pass

    def addShow(self):
        pass

    def removeShow(self):
        pass

if(__name__ == "__main__"):
    # print(client.list_database_names())
    app = App()
    frame = MainFrame(app)
    app.mainloop()
