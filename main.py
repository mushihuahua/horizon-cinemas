import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.objectid import ObjectId
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from werkzeug.security import generate_password_hash, check_password_hash
import os
import weakref
import random
import certifi


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ca = certifi.where()
cluster = "mongodb+srv://mushihuahua:TfOPb5fwlgyFMNHE@horizoncinemas.ldas1hn.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster, tlsCAFile=ca)

db = client.horizonCinemasDB
ERROR_COLOUR="#e23636"
SUCCESS_COLOUR="#66bb6a"
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
    def __init__(self, id, city, location, numOfScreens=0, screens=[]):
        self.__id = id
        self.__city = city
        self.__location = location
        self.__numOfScreens = numOfScreens
        self.__screens = screens
        self.__listings = []
        self.__bookings = []
        self.__staffMembers = []
    
    def makeBooking(self, newBooking):

        PaymentSystem().authenticatePayment()

        seatIDs = newBooking.getShow().getSeatsAvailable()
        seatNums = []
        ticketType = newBooking.getTicketType()
        ticketTypeClass = TicketFactory().getTicketType(ticketType)
        for seatID in seatIDs:
            seat = db.seats.find_one({"_id": seatID})
            if(seat != None):
                seatNums.append(seat.get("seat_number"))
        
        tickets = []
        numberOfTickets = newBooking.getNumberOfTickets()
        for c, seat in enumerate(seatNums):
            if(seat[0] == ticketType[0]):
                for i in range(numberOfTickets):          
                    tickets.append(newBooking.addTicket(ticketTypeClass(seatNums[c+i])))
                    newBooking.getShow().removeSeat(seatIDs[c])
                break


        bookingDB = {
            "booking_date": newBooking.getBookingDate(),
            "num_of_tickets": newBooking.getNumberOfTickets(),
            "cancelled": False,
            "cost": newBooking.getTotal(),
            "tickets": tickets,
            "show": newBooking.getShow().getID(),
            "cinema": self.getID()
        }
        bookingID = db.bookings.insert_one(bookingDB).inserted_id
        newBooking.setBookingReference(bookingID)
        self.__bookings.append(newBooking)

        return bookingID
 
    def addListing(self, listing): 
        dbListing = {
            "film_name": listing.filmName,
            "film_genre": listing.filmGenre,
            "film_age": listing.filmAge,
            "film_rating": listing.filmRating,
            "film_description": listing.filmDescription,
            "cast": listing.cast,
            "film_length": listing.filmLength,
            "shows": listing.shows
        }

        self.__listings.append(listing)
        return db.listings.insert_one(dbListing).acknowledged

    def removeListing(self, listingID):

        listing = db.listings.find_one({"_id": listingID})
        shows = []
        if(listing != None):
            shows = listing.get("shows")

        for showID in shows:
            db.shows.find_one_and_delete({"_id": showID})
            db.screens.update_many({}, {"$pull": {"shows": showID}})

        return db.listings.delete_one({"_id": listingID}).acknowledged

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

    def removeStaffMember(self, remEmployeeID):
        return db.staff.delete_one({"_id": remEmployeeID}).acknowledged


    def addScreen(self, screen):
        seats = []
        numOfVIP = 10
        numOfLower = int(80*0.3)
        numOfUpper = 80-numOfLower-numOfVIP
        for j in range(numOfLower):
            seats.append(LowerHallSeat(f"L{screen.getScreenNumber()}{j+1}"))
        for j in range(numOfUpper):
            seats.append(UpperGallerySeat(f"U{screen.getScreenNumber()}{j+1}"))
        for j in range(numOfVIP):
            seats.append(VIPSeat(f"V{screen.getScreenNumber()}{j+1}"))

        dbSeats = []
        for seat in seats:
            dbSeat = {
                "seat_number": seat.getSeatNumber(),
            }
            dbSeats.append(db.seats.insert_one(dbSeat).inserted_id)
        
        screen.setCapacity(len(seats))
        screen.setSeats(seats)

        dbScreen = {
            "screen_number": screen.getScreenNumber(),
            "seating_capacity": screen.getCapacity(),
            "seats": dbSeats
        }

        self.__screens.append(screen)
        return db.screens.insert_one(dbScreen).inserted_id

    def getCity(self):
        return self.__city
    
    def getScreens(self):
        return self.__screens    

    def getLocation(self):
        return self.__location

    def getNumOfScreens(self):
        return self.__numOfScreens

    def getID(self):
        return self.__id

    def setID(self, id):
        self.__id = id

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
        
        self.__cities.append(City(cityName, morningPrice, afternoonPrice, eveningPrice))
        return db.cities.insert_one(newCity).acknowledged

    def getCities(self):
        return self.__cities

class City:
    def __init__(self, name="", morningPrice=0, afternoonPrice=0, eveningPrice=0):
        self.__name = name
        self.__morningPrice = morningPrice
        self.__afternoonPrice = afternoonPrice
        self.__eveningPrice = eveningPrice
        self.__cinemas = []

    def getName(self):
        return self.__name

    def getTicketPrice(self, hour):
        if(hour < 12):
            return self.__morningPrice
        if(hour < 18):
            return self.__afternoonPrice
        if(hour < 24):
            return self.__eveningPrice

    def addCinema(self, cinema):

        screens = []
        for i in range(int(cinema.getNumOfScreens())):

            screen = Screen(i+1)
            insertedScreen = cinema.addScreen(screen)
            screens.append(insertedScreen)
            
        dbCinema = {
            "location": cinema.getLocation(),
            "screens": screens
        }
        insertedCinema = db.cinemas.insert_one(dbCinema).inserted_id
        cinema.setID(insertedCinema)

        db.cities.find_one_and_update({'name': self.getName().capitalize()}, {'$push': {'cinemas': insertedCinema}})
        self.__cinemas.append(cinema)

        return True

class Listing: 
    def __init__(self, id, filmName, filmLength, filmDescription, cast, filmGenre, filmAge, filmRating, shows=[]):
        self.id = id
        self.filmName = filmName
        self.filmLength = filmLength
        self.filmDescription = filmDescription
        self.cast = cast
        self.filmGenre = filmGenre
        self.filmAge = filmAge
        self.filmRating = filmRating
        self.shows = shows

    def changeListingInformation(self, listingID, listing):
        
        return db.listings.update_one({"_id":listingID}, {"$set":{"film_name":listing.filmName,
                                                                "film_genre":listing.filmGenre,
                                                                "film_age":listing.filmAge,
                                                                "film_rating":listing.filmRating,
                                                                "film_description":listing.filmDescription,
                                                                "cast":listing.cast,
                                                                "film_length":listing.filmLength,}}).acknowledged

    def getShows(self):
        return self.shows

    def addShow(self, showDate, showTime, screenID):

        screen = db.screens.find_one({"_id": screenID})

        seats = []
        if(screen != None):
            seats = screen.get("seats")

        newShow = {
            "show_date" : showDate, 
            "show_time" : showTime,
            "available_seats": seats,
            "screen_number" : screenID 
        }
        addShowID = db.shows.insert_one(newShow).inserted_id
        db.listings.find_one_and_update({"_id": self.id}, {"$push": {"shows": addShowID}})
        db.screens.find_one_and_update({"_id": screenID}, {"$push": {"shows": addShowID}})

        return addShowID
        
    def removeShow(self, showID, screenID):
        listingID = 0

        for listing in db.listings.find({}):
            for show in listing.get("shows"):
                if(show == ObjectId(showID)):
                    listingID = listing.get("_id")
                    break

        db.shows.find_one_and_delete({"_id": ObjectId(showID)})
        db.listings.find_one_and_update({"_id": listingID}, {"$pull": {"shows": ObjectId(showID)}})
        success = db.screens.find_one_and_update({"_id": screenID}, {"$pull": {"shows": ObjectId(showID)}})

        if(success != None):
            return True
        return False

class Show:
    def __init__(self, id, date, time, seatsAvailable, screen):
        self.__id = id
        self.__date = date
        self.__time = time
        self.__seatsAvailable = seatsAvailable
        self.__screen = screen
        
    def getScreen(self):
        return self.__screen

    def getDate(self):
        return self.__date

    def getTime(self):
        return self.__time

    def getID(self):
        return self.__id

    def getSeatsAvailable(self):
        return self.__seatsAvailable

    def removeSeat(self, seatID):
        self.__seatsAvailable.remove(seatID)
        db.shows.update_one({"_id": self.__id}, {"$pull": {"available_seats": seatID}})

class Seat:
    def __init__(self, seatNumber):
        self.__seatNumber = seatNumber

    def getSeatNumber(self):
        return self.__seatNumber

class LowerHallSeat(Seat): 
    def __init__(self, seatNumber):
        super().__init__(seatNumber)

class UpperGallerySeat(Seat): 
    def __init__(self, seatNumber):
        super().__init__(seatNumber)

class VIPSeat(UpperGallerySeat):
    def __init__(self, seatNumber):
        super().__init__(seatNumber)

class Ticket:
    def __init__(self, seatNo):
        self.__seatNo = seatNo
    
    def getPricePercentage(self):
        pass

    def getSeatNumber(self):
        return self.__seatNo

class LowerHallTicket(Ticket): 
    def getPricePercentage(self):
        return 1
    
    def getTicketType(self):
        return "Lower"

class UpperGalleryTicket(Ticket): 
    def getPricePercentage(self):
        return 1.2 

    def getTicketType(self):
        return "Upper"

class VIPTicket(UpperGalleryTicket):
    def getPricePercentage(self):
        return 1.2 * 1.2   

    def getTicketType(self):
        return "VIP"

class TicketFactory: 
    def getTicketType(self, ticketType):
        if(ticketType == "Lower"):
            return LowerHallTicket
        elif(ticketType == "Upper"):
            return UpperGalleryTicket
        elif(ticketType == "VIP"):
            return VIPTicket
        return Ticket

class Receipt:
    def __init__(self, booking):
        self.__booking = booking

    def displayReceipt(self):
        pass

class PaymentSystem:
    
    def authenticatePayment(self):
        print("Payment Successful")        

class Screen: 
    def __init__(self, screenNumber, capacity=0, seats=[]):
        self.__screenNumber = screenNumber
        self.__seatingCapacity = capacity
        self.__seats = seats
        
    def checkVIPAvailability(self):
        pass

    def checkUpperAvailability(self):
        pass

    def checkLowerAvailability(self):
        pass

    def getSeats(self):
        return self.__seats

    def setSeats(self, seats):
        self.__seats = seats

    def getScreenNumber(self):
        return self.__screenNumber

    def setCapacity(self, capacity):
        self.__seatingCapacity = capacity

    def getCapacity(self):
        return self.__seatingCapacity

class AvailabilityChecker:
    def __init__(self, seatType, show):
        self.seatType = seatType
        self.show = show
    
    def checkAvailability(self):
        seatNums = []
        for seatID in self.show.getSeatsAvailable():
            seat = db.seats.find_one({"_id": seatID})
            if(seat != None):
                seatNums.append(seat.get("seat_number"))

        numOfSeatsAvailable = 0
        for seatNum in seatNums:
            if(self.seatType[0] == seatNum[0]):
                numOfSeatsAvailable += 1
        
        return numOfSeatsAvailable
    

class Booking: 
    def __init__(self, bookingReference, numOfTickets, show, cinema, ticketType, bookingDate, totalCost=0):
        self.__bookingReference = bookingReference 
        self.__numOfTickets = numOfTickets
        self.__bookingDate = bookingDate
        self.__ticketType = ticketType
        self.__tickets = []
        self.__cancelled = False
        self.__totalCost = totalCost
        self.__show = show
        self.__receipt = None
        self.__cinema = cinema 

    def calculateTotal(self):
        ticketTypeClass = TicketFactory().getTicketType(self.__ticketType)
        pricePercentage = ticketTypeClass("").getPricePercentage()

        self.__totalCost = round(pricePercentage * self.__numOfTickets * self.__cinema.getCity().getTicketPrice(self.__show.getTime()), 1)
        return self.__totalCost

    def addTicket(self, ticket):
        ticketDB = {
            "seat_number": ticket.getSeatNumber(),
            "ticket_type": ticket.getTicketType()
        }

        self.__tickets.append(ticket)
        return db.tickets.insert_one(ticketDB).inserted_id

    def getTotal(self):
        return self.__totalCost

    def getCinema(self):
        return self.__cinema

    def getShow(self):
        return self.__show

    def getNumberOfTickets(self):
        return self.__numOfTickets

    def getBookingDate(self):
        return self.__bookingDate

    def generateReceipt(self):
        self.__receipt = Receipt(self)

    def printReceipt(self):
        pass

    def getTicketType(self):
        return self.__ticketType

    def setBookingReference(self, ref):
        self.__bookingReference = ref

    def getBookingReference(self):
        return self.__bookingReference

    def cancel(self):

        bookingDB = db.bookings.find_one({"_id": self.__bookingReference})
        seatsAvailableIDs = self.__show.getSeatsAvailable()
        seats = self.__show.getScreen().getSeats()

        # Get all the tickets of the selected Booking
        ticketIDs = []
        if(bookingDB != None):
            ticketIDs = bookingDB.get("tickets")

        # Get the available seat numbers
        seatsAvailable = []
        for seatID in seatsAvailableIDs:
            seat = db.seats.find_one({"_id": seatID})
            if(seat != None):
                seatsAvailable.append(seat.get("seat_number"))

        # Get the seat numbers associated with the tickets of the selected Booking
        ticketSeats = []
        for ticketID in ticketIDs:
            ticket = db.tickets.find_one({"_id": ticketID})
            if(ticket != None):
                ticketSeats.append(ticket.get("seat_number"))

        # Get the IDs of the seats associated with tickets
        ticketSeatIDs = []
        for ticketSeat in ticketSeats:
            for seat in seats:
                seatDB = db.seats.find_one({"_id": seat})
                if(seatDB != None):
                    if(seatDB.get("seat_number") == ticketSeat):
                        ticketSeatIDs.append(seatDB.get("_id"))

        # Insert the seats associated with the tickets back in the available seats array
        for i in range(len(ticketSeats)):
            for j in range(len(seatsAvailable)):
                if(ticketSeats[i][0] == seatsAvailable[j][0]):
                    if(int(seatsAvailable[j][2:]) > int(ticketSeats[i][2:])):
                        seatsAvailableIDs.insert(j, ticketSeatIDs[i])
                        break
        
        # Remove tickets from database
        for ticketID in ticketIDs:
            db.tickets.delete_one({"_id": ticketID})
        
        db.shows.update_one({"_id": self.__show.getID()}, {"$set": {"available_seats": seatsAvailableIDs}})
        db.bookings.update_one({"_id": self.__bookingReference}, {"$set": {"cancelled": True, "tickets": []}})

        self.__cancelled = True
        return self.__cancelled


staffTypes = {
    "Booking Staff": BookingStaff,
    "Admin": Admin,
    "Manager": Manager
}

cityContainer = CityContainer()
loggedInUser = Staff(0, "", 0, "", "")
currentCity = City("Bristol", 6, 7, 8)
cinema  = db.cinemas.find_one({"_id": ObjectId("63baf1143fa6569bc82de524")})
currentCinema = Cinema("", "", "")
if(cinema != None):
    currentCinema = Cinema(cinema.get("_id"), currentCity, cinema.get("location"), screens=cinema.get("screens"))

class App(ctk.CTk):

    width = 1920
    height = 1080
    width = 1920
    height = 1080
    x_pos = 0
    y_pos = 0

    def __init__(self):
        super().__init__()

        self.frames = []
        self.buttons = []


        self.frames = []
        self.buttons = []

        self.title("Horizon Cinemas")
        if "nt" == os.name:
            self.iconbitmap(bitmap = "icon.ico")

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

                # Check if that employee is employed at the current cinema
                if(result.get("cinema") != currentCinema.getID()):
                    self.error = ctk.CTkLabel(master=self.loginFrame, text="This employee is not employed at this cinema", text_color=ERROR_COLOUR, font=("Roboto", 18))
                    self.error.pack()
                    return

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
                    menu = MenuFrame(app, loggedInUser)
                    mainView = MainFrame(app, loggedInUser)
                    adminView = AdminFrame(app, loggedInUser)
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
    def __init__(self, container, loggedInUser):

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

        # self.accountButton = ctk.CTkButton(master=self.menuFrame, 
        #                             text="Account",
        #                             width=250,
        #                             height=75,
        #                             font=("", 16, "bold"),
        #                             corner_radius=7,
        #                             fg_color="#bb86fc",
        #                             hover_color="#9f54fb",
        #                             command=lambda: container.switchFrame(accountView.frame, self.accountButton))

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

        # Put them on the GUI Pack inline and append them to a buttons array

        self.bookingStaffButton.pack(side=tk.LEFT, padx=15, pady=10)
        employeeType = loggedInUser.__class__.__name__
        if(employeeType == "Admin" or employeeType == "Manager"):
            self.adminButton.pack(side=tk.LEFT, padx=15, pady=10)
        if(employeeType == "Manager"):
            self.managerButton.pack(side=tk.LEFT, padx=15, pady=10)
        # self.accountButton.pack(side=tk.LEFT, padx=15, pady=10)

        self.logoutButton.pack(side=tk.RIGHT, padx=20, pady=10)
        container.buttons.append(self.bookingStaffButton)
        container.buttons.append(self.adminButton)
        container.buttons.append(self.managerButton)
        # container.buttons.append(self.accountButton)

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

