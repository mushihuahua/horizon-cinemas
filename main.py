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
ctk.set_default_color_theme("blue")

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

class Report:
    def __init__(self, numberOfListingBookings=0, totalMonthlyRevenue=0, topFilm=0, staffBookings=0):
        self.__numberOfListingBookings = numberOfListingBookings
        self.__totalMonthlyRevenue = totalMonthlyRevenue
        self.__topFilm = topFilm
        self.__staffBookings = staffBookings

    def displayReport(self):
        pass
    
class Cinema:
    def __init__(self, id, city, location):
        self.__id = id
        self.__city = city
        self.__location = location
        self.__screens = []
        self.__listings = []
        self.__bookings = []
        self.__staffMembers = []

    def getID(self):
        return self.__id
        
    def getListings(self):
        pass
    
    def makeBooking(self, newBooking):
        pass
    
    def cancelBooking(self, bookingReference):
        pass

    def addListing(self, listing): 
        pass

    def removeListing(self, listing):
        pass

    def createNewEmployee(self, newFirstName, newLastName, newEmployeeID, newPasswordHash, newType):
        newEmployee = {
            "_id": newEmployeeID,
            "password_hash": newPasswordHash,
            "first_name": newFirstName,
            "last_name": newLastName,
            "type": newType,
            "cinema": currentCinema.getID()
        }

        return db.staff.insert_one(newEmployee).acknowledged

    def removeStaffMember(self, staffMember):
        pass

    def addScreen(self, screen):
        pass

    def removeScreen(self, screen):
        pass

    def getCity(self):
        return self.__city

    def getLocation(self):
        return self.__location
    
class CityContainer: 
    def __init__(self):
        self.__cities = []
        for city in db.cities.find():
            self.__cities.append(City(city.get("name"), city.get("morning_price"), city.get("afternoon_price"), city.get("evening_price")))

    def addCity(self, cityName, morningPrice, afternoonPrice, eveningPrice):
        newCity = {
            "name" : cityName, 
            "morning_price" : morningPrice,
            "afternoon_price" : afternoonPrice,
            "evening_price" : eveningPrice
        }
        return db.cities.insert_one(newCity).acknowledged

    def removeCity(self, city):
        pass

    def getCities(self):
        return self.__cities

class City:
    def __init__(self, name, morningPrice, afternoonPrice, eveningPrice):
        self.__name = name
        self.__morningPrice = morningPrice
        self.__afternoonPrice = afternoonPrice
        self.__eveningPrice = eveningPrice
        self.__cinemas = []

    def getName(self):
        return self.__name

    def getTicketPrice(self, time):
        pass

    def addCinema(self, cinema):
        pass

    def removeCinema(self, cinema):
        pass

    def setMorningTicketPrice(self, newPrice):
        pass

    def setAfternoonTicketPrice(self, newPrice):
        pass

    def setEveningTicketPrice(self, newPrice):
        pass

    def makeBookingAtDifferentCinema(self, cinema, city):
        pass

class Listing: 
    def __init__(self,filmName, filmDate, filmDescription, actorDetails,filmGenre,filmAge, filmRating):
        self.__filmName = filmName
        self.__filmDate = filmDate
        self.__filmDescription = filmDescription
        self.__actorDetails = actorDetails
        self.__filmGenre = filmGenre
        self.__filmAge = filmAge
        self.__filmRating = filmRating
 
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

    def addShow(self, show):
        pass

    def removeShow(self, show):
        pass


class Show:
    def __init__(self, listing, date, time, screen):
        self.__listing = listing
        self.__date = date
        self.__time = time
        self.__screen = screen
        
    def getScreen(self):
        pass

    def getListing(self):
        pass

    def getDate(self):
        pass

    def getTime(self):
        pass

class Seat:
    def __init__(self, seatNumber, available=True):
        self.__seatNumber = seatNumber
        self.__available = available

    def changeAvailability(self):
        if(self.__available):
            self.__available = False
        else:
            self.__available = True
        
    def getAvailability(self):
        return self.__available

    def getSeatNumber(self):
        return self.__seatNumber

class LowerHallSeat(Seat): 
    def __init__(self, seatNumber, available=True):
        super().__init__(seatNumber, available)

class UpperGallerySeat(Seat): 
    def __init__(self, seatNumber, available=True):
        super().__init__(seatNumber, available)

class VIPSeat(UpperGallerySeat):
    def __init__(self, seatNumber, available=True):
        super().__init__(seatNumber, available)

class Ticket:
    def __init__(self, seatNo):
        self.__seatNo = seatNo
    
    def getPricePercentage(self):
        pass

class LowerHallTicket(Ticket): 
    def getPricePercentage(self):
        return 1

class UpperGalleryTicket(Ticket): 
    def getPricePercentage(self):
        return 1.2 

class VIPTicket(UpperGalleryTicket):
    def getPricePercentage(self):
        return 1.2 * 1.2   

class TicketFactory: 
    def getTicketType(self, ticketType):
        if(ticketType == "Lower Hall"):
            return LowerHallTicket
        elif(ticketType == "Upper Gallery"):
            return UpperGalleryTicket
        elif(ticketType == "VIP"):
            return VIPTicket

class Receipt:
    def __init__(self, booking):
        self.__booking = booking

    def displayReceipt(self):
        pass

class AvailabilitvChecker:
    def __init__(self, type, screen):
        self.__type = type
        self.__screen = screen

class PaymentSystem:
    pass        

class Screen: 
    def __init__(self, capacity):
        self.__capacity = capacity
        self.__screenNumber = int
        self.__seatingCapacity = int
        self.__seatsAvailabe = []
        self.__seats = []
        
    def checkVIPAvailability(self):
        pass

    def checkUpperAvailability(self):
        pass

    def checkLowerAvailability(self):
        pass

    def addSeat(self):
        pass

    def getSeats(self):
        return self.__seats

    def getAvailableSeats(self):
        pass


class AvailabilityChecker:
    def __init__(self, seatType, screen):
        self.seatType = seatType
        self.screen = screen
    
    def checkAvailability(self):
        pass

class Booking: 
    def __init__(self, show, cinema, screen, ticketType, bookingDate):
        self.__bookingReference = int # Randomly Generated
        self.__bookingDate = bookingDate
        self.__ticketType = ticketType
        self.__tickets = []
        self.__cancelled = False
        self.__totalCost = 0
        self.__show = show
        self.__screen = screen
        self.__receipt = None
        self.__cinema = cinema 

    def calculateTotal(self):
        pass

    def addTicket(self):
        pass
    
    def getTotal(self):
        return self.__totalCost

    def getScreen(self):
        return self.__screen

    def getCinema(self):
        return self.__cinema

    def getNumberOfTickets(self):
        return len(self.__tickets)

    def generateReceipt(self):
        self.__receipt = Receipt(self)

    def printReceipt(self):
        pass

    def getBookingReference(self):
        return self.__bookingReference

    def cancel(self):
        self.__cancelled = True


staffTypes = {
    "Booking Staff": BookingStaff,
    "Admin": Admin,
    "Manager": Manager
}

cityContainer = CityContainer()
loggedInUser = Staff(0, "", 0, "", "")
currentCity = City("Bristol", 6, 7, 8)
cinema  = db.cinemas.find_one({"_id": ObjectId("63a22d895cbf5a11ca1f710f")})
currentCinema = None
if(cinema != None):
    currentCinema = Cinema(cinema.get("_id"), currentCity, cinema.get("location"))

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
                    
                    staffType = result.get("type")

                    loggedInUser = staffTypes[staffType](result.get("_id"), result.get("password_hash"), result.get("cinema"), result.get("first_name"), result.get("last_name"))

                    from pages.mainPage import MainFrame
                    from pages.adminPage import AdminFrame
                    from pages.managerPage import ManagerFrame
                    from pages.accountPage import AccountFrame
                     
                    global mainView, adminView, managerView, accountView, menu
                    menu = MenuFrame(app)
                    mainView = MainFrame(app)
                    adminView = AdminFrame(app)
                    managerView = ManagerFrame(app, loggedInUser)
                    accountView = AccountFrame(app)
                    
                    # app.frames.append(loginView)
                    app.frames.append(mainView)
                    app.frames.append(managerView)
                    app.frames.append(adminView)
                    app.frames.append(accountView)


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

    loginView = LoginFrame(app)
    cityContainer = CityContainer()

    loginView.loginFrame.pack(pady=20, padx=60, fill="both", expand=True)
    # menu.menuFrame.pack(fill="both")
    # menu.bookingStaffButton.configure(border_color="#e5d1fe", border_width=4, fg_color="#9f54fb")
    # loginView.loginFrame.pack_forget()
    # mainView.frame.pack(pady=20, padx=60, fill="both", expand=True)

    app.mainloop()

