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

class Cinema:
    def __init__(self, city, location):
        self.__city = city
        self.__location = location
        self.__screens = []
        self.__listings = []
        self.__bookings = []
        self.__staffMembers = []
        
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

    def hireStaffMember(self, staffMember):
        pass

    def removeStaffMember(self, staffMember):
        pass

    def addScreen(self, screen):
        pass

    def removeScreen(self, screen):
        pass

    def getCity(self):
        pass
    
class CityContainer: 
    def __init__(self):
        self.__cities = []

    def addCity(self, city):
        pass
    
    def removeCity(self, city):
        pass

class City:
    def __init__(self, name, morningPrice, afternoonPrice, eveningPrice):
        self.__name = name
        self.__morningPrice = morningPrice
        self.__afternoonPrice = afternoonPrice
        self.__eveningPrice = eveningPrice
        self.__cinemas = []

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

if(__name__ == "__main__"):
    # print(client.list_database_names())
    app = App()
    frame = MainFrame(app)
    app.mainloop()
