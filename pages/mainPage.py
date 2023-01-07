import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkcalendar import *
import datetime
from bson import ObjectId

# Booking View
class MainFrame():
    def __init__(self, container, loggedInUser):

        from main import db, currentCinema

        date = datetime.date.today().strftime('%Y-%m-%d')
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:])

        self.loggedInUser = loggedInUser
        self.frames = []
        self.error = None
        self.successMessage = None
        self.selectedListingID = None
        self.selectedBookingID = None
        self.showsButtons = []

        self.frame = ctk.CTkFrame(master=container, corner_radius=10)
        self.formFrame = ctk.CTkFrame(master=self.frame, corner_radius=10)
        self.viewListingsFrame = ctk.CTkFrame(master=self.frame, corner_radius=10)
        self.viewBookingsFrame = ctk.CTkFrame(master=self.frame, corner_radius=10)

        self.frames.append(self.formFrame)
        self.frames.append(self.viewListingsFrame)
        self.frames.append(self.viewBookingsFrame)

        self.addListingFrame = ctk.CTkFrame(master=self.frame, corner_radius=10)
        self.addShowFrame = ctk.CTkFrame(master=self.frame, corner_radius=10)
        self.frames.append(self.addListingFrame)
        self.frames.append(self.addShowFrame)

        self.buttonsFrame = ctk.CTkFrame(master=self.frame, corner_radius=20)

        # Booking Form
        self.viewTitle = ctk.CTkLabel(master=self.formFrame, text="Booking Form", font=("Roboto", 48))
    
        self.calendarLabel = ctk.CTkLabel(master=self.formFrame, text="Select Date:", font=("Roboto", 15))
        self.calendar = Calendar(master=self.formFrame, 
                        selectmode='day', 
                        year=year, 
                        month=month, 
                        day=day+1,
                        mindate=datetime.date.today()+ datetime.timedelta(days=1),
                        font=("", 10))
    
        self.calendar.bind("<<CalendarSelected>>", self.__loadListingsBooking)

        self.selectFilmLabel = ctk.CTkLabel(master=self.formFrame, text="Select Film:", font=("Roboto", 15))
        self.selectFilm = ctk.CTkOptionMenu(master=self.formFrame, 
                            values=[""],
                            width=200,
                            height=30,
                            font=("", 16, "bold"),
                            corner_radius=4,
                            command=self.__loadShowsBooking)
        self.selectShowingLabel = ctk.CTkLabel(master=self.formFrame, text="Select Showing:", font=("Roboto", 15))    
        self.selectShowing = ctk.CTkOptionMenu(master=self.formFrame, 
                            values=[""],
                            width=200,
                            height=30,
                            font=("", 16, "bold"),
                            corner_radius=4)  

        self.ticketTypeLabel = ctk.CTkLabel(master=self.formFrame, text="Ticket Type:", font=("Roboto", 15)) 
        self.ticketType = ctk.StringVar(value="")
        self.lowHallTickets = ctk.CTkRadioButton(master=self.formFrame, text="Lower Hall", variable=self.ticketType, value="Lower")    
        self.upperHallTickets = ctk.CTkRadioButton(master=self.formFrame, text="Upper Hall", variable=self.ticketType, value="Upper") 
        self.vipHallTickets = ctk.CTkRadioButton(master=self.formFrame, text="VIP", variable=self.ticketType, value="VIP")                                     
        self.totalPriceLabel = ctk.CTkLabel(master=self.formFrame, text="Total Price:", font=("Roboto", 15)) 
        self.totalPrice = ctk.CTkLabel(master=self.formFrame, text=" ", font=("Roboto", 18)) 

        self.numberOfTicketsLabel = ctk.CTkLabel(master=self.formFrame, text="Number of Tickets:", font=("Roboto", 15))    
        self.numberOfTickets = ctk.CTkOptionMenu(master=self.formFrame, 
                            values=[str(i+1) for i in range(10)],
                            width=200,
                            height=30,
                            font=("", 16, "bold"),
                            corner_radius=4)

        self.selectedCinema = ctk.StringVar(value=currentCinema.getLocation())
        cinemas = [cinema.get("location") for cinema in db.cinemas.find({})]  
        self.cinemasLabel = ctk.CTkLabel(master=self.formFrame, text="Cinema:", font=("Roboto", 15))    
        self.cinemasMenu = ctk.CTkOptionMenu(master=self.formFrame, 
                            values=cinemas,
                            variable=self.selectedCinema,
                            width=200,
                            height=30,
                            font=("", 16, "bold"),
                            corner_radius=4,
                            command=self.__loadListingsBooking)
        self.__loadListingsBooking()

        self.availabilityLabel = ctk.CTkLabel(master=self.formFrame, text="Available Seats:", font=("Roboto", 15)) 
        self.availability = ctk.CTkLabel(master=self.formFrame, text=" ", font=("Roboto", 18)) 

        self.makeBookingButton = ctk.CTkButton(master=self.formFrame, 
                                    text="Make Booking",
                                    width=200,
                                    height=40,
                                    font=("", 16, "bold"),
                                    corner_radius=7,
                                    command=self.__makeBooking)

        self.checkAvailAndPriceButton = ctk.CTkButton(master=self.formFrame, 
                                    text="Check Availability and Price",
                                    width=200,
                                    height=40,
                                    font=("", 16, "bold"),
                                    corner_radius=7,
                                    command=self.__checkAvailabilityAndPrice)

        self.formFrame.pack(pady=20, padx=20, fill="both", expand=True)

        self.viewTitle.place(relx=.5, rely=.1, anchor="center")

        self.calendarLabel.place(relx=.38, rely=.3, anchor="center")
        self.calendar.place(relx=.5, rely=.3, anchor="center")

        if(self.loggedInUser.__class__.__name__ == "Manager" or self.loggedInUser.__class__.__name__ == "Admin"):
            self.cinemasLabel.place(relx=.35, rely=.45, anchor="center")
            self.cinemasMenu.place(relx=.5, rely=.45, anchor="center")


        self.selectFilmLabel.place(relx=.35, rely=.5, anchor="center")
        self.selectFilm.place(relx=.5, rely=.5, anchor="center")

        self.selectShowingLabel.place(relx=.35, rely=.55, anchor="center")
        self.selectShowing.place(relx=.5, rely=.55, anchor="center")

        self.ticketTypeLabel.place(relx=.3, rely=.6, anchor="center")
        self.lowHallTickets.place(relx=.425, rely=.6, anchor="center")
        self.upperHallTickets.place(relx=.5, rely=.6, anchor="center")
        self.vipHallTickets.place(relx=.575, rely=.6, anchor="center")

        self.numberOfTicketsLabel.place(relx=.35, rely=.65, anchor="center")
        self.numberOfTickets.place(relx=.5, rely=.65, anchor="center")

        self.totalPriceLabel.place(relx=.4, rely=.7, anchor="center")
        self.totalPrice.place(relx=.5, rely=.7, anchor="center")
        self.availabilityLabel.place(relx=.4, rely=.75, anchor="center")
        self.availability.place(relx=.5, rely=.75, anchor="center")
        self.checkAvailAndPriceButton.place(relx=.4, rely=.8, anchor="center")
        self.makeBookingButton.place(relx=.6, rely=.8, anchor="center")

        # Navigation Buttons
        self.bookingButton = ctk.CTkButton(master=self.buttonsFrame, 
                                    text="Booking Form", 
                                    width=250,
                                    height=75,
                                    font=("", 18, "bold"), 
                                    corner_radius=7,
                                    fg_color="#9f54fb",
                                    hover_color="#a722fa",
                                    command=lambda: self.switchFrames(self.formFrame))

        self.viewListingsButton = ctk.CTkButton(master=self.buttonsFrame, 
                                    text="View Listings", 
                                    width=250,
                                    height=75,
                                    font=("", 18, "bold"), 
                                    corner_radius=7,
                                    fg_color="#9f54fb",
                                    hover_color="#a722fa",
                                    command=lambda: self.switchFrames(self.viewListingsFrame))

        self.viewBookingsButton = ctk.CTkButton(master=self.buttonsFrame, 
                                    text="View Bookings", 
                                    width=250,
                                    height=75,
                                    font=("", 18, "bold"), 
                                    corner_radius=7,
                                    fg_color="#9f54fb",
                                    hover_color="#a722fa",
                                    command=lambda: self.switchFrames(self.viewBookingsFrame))

        self.buttonsFrame.pack(fill="both", padx=20)
        self.bookingButton.pack(side="left", padx=(15, 15))
        self.viewListingsButton.pack(side="left", padx=15)
        self.viewBookingsButton.pack(side="left", padx=15)

        # View Listings
        from main import db

        self.viewListingsLabel = ctk.CTkLabel(master=self.viewListingsFrame, text="View Listings", font=("Roboto", 32, "bold"))
        self.viewListingsLabel.pack(pady=40, padx=30)
        
        self.listings = list(db.listings.find())
        self.listingsList = [listing.get("film_name") for listing in self.listings]

        self.selectedListing = ctk.StringVar(value="Select Listing")

        self.listingComboBox = ctk.CTkComboBox(master=self.viewListingsFrame, font=("", 15), values=self.listingsList, variable=self.selectedListing, command = self.__viewListings, height=40, width=350)
        self.listingComboBox.pack(padx=20, pady=20)

        self.filmNameLabel = ctk.CTkLabel(master=self.viewListingsFrame, text="Film Name: ", font=("", 18))
        self.filmNameLabel.pack(padx=20, pady=5)
        
        self.filmDateLabel = ctk.CTkLabel(master=self.viewListingsFrame, text="Film Release Date: ", font=("", 18))
        self.filmDateLabel.pack(padx=20, pady=5)

        self.filmDescriptionLabel = ctk.CTkLabel(master=self.viewListingsFrame, text="Film Description: ", font=("", 18))
        self.filmDescriptionLabel.pack(padx=20, pady=5)

        self.filmGenreLabel = ctk.CTkLabel(master=self.viewListingsFrame, text="Film Genre: ", font=("", 18))
        self.filmGenreLabel.pack(padx=20, pady=5)

        self.filmRatingLabel = ctk.CTkLabel(master=self.viewListingsFrame, text="Film Rating: ", font=("", 18))
        self.filmRatingLabel.pack(padx=20, pady=5)

        self.actorDetailsLabel = ctk.CTkLabel(master=self.viewListingsFrame, text="Cast: ", font=("", 18))
        self.actorDetailsLabel.pack(padx=20, pady=5)

        self.filmLengthLabel = ctk.CTkLabel(master=self.viewListingsFrame, text="Film Length: ", font=("", 18))
        self.filmLengthLabel.pack(padx=20, pady=5)

        self.showsLabel = ctk.CTkLabel(master=self.viewListingsFrame, text="Shows: ", font=("", 18))
        self.showsLabel.pack(padx=20, anchor="w")

        # View Bookings
        self.viewBookingsLabel = ctk.CTkLabel(master=self.viewBookingsFrame, text="View Bookings", font=("Roboto", 32, "bold"))
        self.viewBookingsLabel.pack(pady=40, padx=30)
        
        self.bookings = list(db.bookings.find({"cancelled": False}))
        self.bookingsList = [str(booking.get("_id")) for booking in self.bookings]
        
        self.selectedBooking = ctk.StringVar(value="Select Booking")
        
        if(len(list(self.bookings)) == 0):
            self.bookingsList = ["Empty"]

        self.bookingComboBox = ctk.CTkComboBox(master=self.viewBookingsFrame, values = self.bookingsList, command = self.__viewBooking,  variable=self.selectedBooking, font=("", 15), height=40, width=350)
        self.bookingComboBox.pack(padx=20, pady=20)

        self.bookingRef = ctk.CTkLabel(master=self.viewBookingsFrame, text="Booking Reference: ", font=("", 18))
        self.bookingRef.pack(padx=20, pady=10)

        self.bookingDate = ctk.CTkLabel(master=self.viewBookingsFrame, text="Booking Date: ", font=("", 18))
        self.bookingDate.pack(padx=20, pady=10)
        
        self.NoOfTickets = ctk.CTkLabel(master=self.viewBookingsFrame, text="Number of Tickets: ", font=("", 18))
        self.NoOfTickets.pack(padx=20, pady=10)

        self.cancelled = ctk.CTkLabel(master=self.viewBookingsFrame, text="Cancelled: ", font=("", 18))
        self.cancelled.pack(padx=20, pady=10)

        self.totalCost = ctk.CTkLabel(master=self.viewBookingsFrame, text="Total Cost: ", font=("", 18))
        self.totalCost.pack(padx=20, pady=10)

        self.cancelButton = ctk.CTkButton(master=self.viewBookingsFrame, 
                        text="Cancel Booking", 
                        width=250, 
                        height=52, 
                        font=("Roboto", 20),
                        fg_color="#bb86fc",
                        hover_color="#9f54fb",
                        command=self.__cancelBooking)
        
        self.cancelButton.pack(pady=10)

        # Add Listing
        self.listingFormLabel = ctk.CTkLabel(master=self.addListingFrame, text="Listing Form", font=("Roboto", 32, "bold"))
        self.listingFormLabel.place(relx=.5, rely=.05, anchor="center")

        self.filmName = ctk.CTkEntry(master=self.addListingFrame, 
                width=250, 
                height=52, 
                placeholder_text="Film Name", 
                font=("Roboto", 14))
        self.filmName.place(relx=.4, rely=.2, anchor="center")
        # self.firstNameEntry.bind('<Return>', self.__createAccount)

        self.filmGenre = ctk.CTkEntry(master=self.addListingFrame, 
                width=250, 
                height=52, 
                placeholder_text="Film Genre", 
                font=("Roboto", 14))
        self.filmGenre.place(relx=.6, rely=.2, anchor="center")
        # self.firstNameEntry.bind('<Return>', self.__createAccount)

        self.filmAge = ctk.CTkEntry(master=self.addListingFrame, 
                width=250, 
                height=52, 
                placeholder_text="Film Release Year", 
                font=("Roboto", 14))
        self.filmAge.place(relx=.4, rely=.3, anchor="center")
        # self.firstNameEntry.bind('<Return>', self.__createAccount)

        self.filmRating = ctk.CTkEntry(master=self.addListingFrame, 
                width=250, 
                height=52, 
                placeholder_text="Film Rating", 
                font=("Roboto", 14))
        self.filmRating.place(relx=.6, rely=.3, anchor="center")
        # self.firstNameEntry.bind('<Return>', self.__createAccount)

        self.filmLengthEntryLabel = ctk.CTkLabel(master=self.addListingFrame, text="Film Length:", font=("Roboto", 14))
        self.filmLengthEntryLabel.place(relx=.35, rely=.375, anchor="center")

        self.lengthHours = tk.StringVar()
        self.filmLength1 = ttk.Spinbox(master=self.addListingFrame, from_=0, to=4, textvariable=self.lengthHours, width=12, font=("Roboto", 16))
        self.filmLength1.place(relx=.45, rely=.375, anchor="center")

        self.lengthMinutes = tk.StringVar()
        self.filmLength2 = ttk.Spinbox(master=self.addListingFrame, from_=0, to=59, textvariable=self.lengthMinutes, width=12, font=("Roboto", 16))
        self.filmLength2.place(relx=.6, rely=.375, anchor="center")

        self.filmDetails = ctk.CTkEntry(master=self.addListingFrame, 
                width=500, 
                height=52, 
                placeholder_text="Film Details", 
                font=("Roboto", 14))
        self.filmDetails.place(relx=.5, rely=.475, anchor="center")
        # self.firstNameEntry.bind('<Return>', self.__createAccount)

        self.actorDetails = ctk.CTkEntry(master=self.addListingFrame, 
                width=500, 
                height=52, 
                placeholder_text="Cast: ", 
                font=("Roboto", 14))
        self.actorDetails.place(relx=.5, rely=.575, anchor="center")
        # self.firstNameEntry.bind('<Return>', self.__createAccount)

        self.addButton = ctk.CTkButton(master=self.addListingFrame, 
                        text="Add Listing", 
                        width=250, 
                        height=52, 
                        font=("Roboto", 20),
                        fg_color="#bb86fc",
                        hover_color="#9f54fb",
                        command=self.__addListing)
        
        self.addButton.place(relx=.5, rely=.675, anchor="center")
    
        self.updateButton = ctk.CTkButton(master=self.addListingFrame, 
                        text="Update Listing", 
                        width=250, 
                        height=52, 
                        font=("Roboto", 20),
                        fg_color="#bb86fc",
                        hover_color="#9f54fb",
                        command=self.__updateListing)
        
        self.updateButton.place(relx=.5, rely=.775, anchor="center")


        # Add Show
        self.addShowLabel = ctk.CTkLabel(master=self.addShowFrame, text="Add Show", font=("Roboto", 32, "bold"))
        self.addShowLabel.place(relx=.5, rely=.05, anchor="center")

        self.showDate = DateEntry(master=self.addShowFrame, 
                width=25, 
                font=("Roboto", 14))
        
        self.showDate.delete(0, "end")
        self.showDate.insert(0, "Show Date")
        self.showDate.place(relx=.5, rely=.15, anchor="center")
        # self.firstNameEntry.bind('<Return>', self.__createAccount)

        self.showTimeLabel = ctk.CTkLabel(master=self.addShowFrame, text="Show Time:", font=("Roboto", 14))
        self.showTimeLabel.place(relx=.35, rely=.25, anchor="center")

        self.timeHours = ctk.StringVar()
        self.showTime1 = ttk.Spinbox(master=self.addShowFrame, from_=0, to=23, textvariable=self.timeHours, width=12, font=("Roboto", 16))
        self.showTime1.place(relx=.45, rely=.25, anchor="center")

        self.timeMinutes = ctk.StringVar()
        self.showTime2 = ttk.Spinbox(master=self.addShowFrame, from_=0, to=59, textvariable=self.timeMinutes, width=12, font=("Roboto", 16))
        self.showTime2.place(relx=.575, rely=.25, anchor="center")

        from main import currentCinema

        self.selectionScreens = [f"Screen {i+1}" for i in range(len(currentCinema.getScreens()))]
            
        self.screenSelected = ctk.StringVar(value="Select a Screen")
        self.selectScreen = ctk.CTkOptionMenu(master=self.addShowFrame,
                                    fg_color="#bb86fc",
                                    button_color="#9f54fb",
                                    button_hover_color="#a722fa", 
                                    variable=self.screenSelected, 
                                    values=self.selectionScreens,
                                    width=250, 
                                    height=32)

        self.selectScreen.place(relx=.5, rely=.35, anchor="center")

        self.addShowButton = ctk.CTkButton(master=self.addShowFrame, 
                        text="Add Show", 
                        width=250, 
                        height=52, 
                        font=("Roboto", 20),
                        fg_color="#bb86fc",
                        hover_color="#9f54fb",
                        command= self.__addShow)
        
        self.addShowButton.place(relx=.5, rely=.45, anchor="center")
    

    def __checkAvailabilityAndPrice(self):

        from main import db, currentCinema, Booking, Show, AvailabilityChecker, City, Cinema, ERROR_COLOUR, SUCCESS_COLOUR

        if(self.error != None):
            self.error.pack_forget()

        if(self.selectFilm.get() == ""):
            self.error = ctk.CTkLabel(master=self.formFrame, text="Select a film", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return -1 

        if(self.selectShowing.get() == ""):
            self.error = ctk.CTkLabel(master=self.formFrame, text="Select a show", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return -1
        
        if(self.ticketType.get() == ""):
            self.error = ctk.CTkLabel(master=self.formFrame, text="Select a Ticket Type", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return -1

        cinema = None
        if(self.loggedInUser.__class__.__name__ == "BookingStaff"):
            cinema = currentCinema
        else:
            cinemaLocation = self.cinemasMenu.get()
            cinemaDB = db.cinemas.find_one({"location": cinemaLocation})

            cinemaID = None
            cityID = None
            city = None
            if(cinemaDB != None):
                cinemaID = cinemaDB.get("_id")
                cityDB = db.cities.find({"cinemas": cinemaID})
                if(cityDB != None):
                    cityDB = list(cityDB)[0]
                    city = City(cityDB.get("name"), cityDB.get("morning_price"), cityDB.get("afternoon_price"), cityDB.get("evening_price"))
            
            cinema = Cinema(cinemaID, city, cinemaLocation)


        # Get the number of seats available
        bookingType = self.ticketType.get()
        showID = self.availableListings[self.selectFilm.get()][self.availableShows.index(self.selectShowing.get())]
        showDB = db.shows.find_one({"_id": showID})
        seatsAvailable = []
        showTime = ""
        if(showDB != None):
            seatsAvailable = showDB.get("available_seats") 
            showTime = showDB.get("show_time").split(":")[0].lstrip("0")
        
        if(showTime == ""):
            showTime = 0

        show = Show(showID, "", int(showTime), seatsAvailable, "")
        numOfSeatsAvailable = AvailabilityChecker(bookingType, show).checkAvailability()

        self.availability.configure(text=str(numOfSeatsAvailable))

        # Get the price
        numberOfTickets = self.numberOfTickets.get()

        self.currentBooking = Booking(0, int(numberOfTickets), show, cinema, bookingType, datetime.date.today().strftime('%d-%m-%Y'))
        price = self.currentBooking.calculateTotal()

        self.totalPrice.configure(text=f"£{price:.1f}")
        return numOfSeatsAvailable

    def __viewBooking(self, choice):
        
        from main import db
        
        self.selectedBookingID = choice
        selectedBooking = db.bookings.find_one({"_id" : ObjectId(choice)})
        if(selectedBooking != None):
            self.bookingRef.configure(text=("Booking Reference: " + str(selectedBooking.get("_id"))))
            self.bookingDate.configure(text=("Booking Date: " + str(selectedBooking.get("booking_date"))))
            self.NoOfTickets.configure(text=("Number of Tickets: " + str(selectedBooking.get("num_of_tickets"))))
            self.cancelled.configure(text=("Cancelled: " + str(selectedBooking.get("cancelled"))))
            self.totalCost.configure(text=("Total Cost: £" + str(selectedBooking.get("cost"))))
    
    def __makeBooking(self):

        from main import SUCCESS_COLOUR, ERROR_COLOUR


        if(self.successMessage != None):
            self.successMessage.pack_forget() 

        if(self.error != None):
            self.error.pack_forget()

        if(self.__checkAvailabilityAndPrice() == -1):
            return

        if(self.__checkAvailabilityAndPrice() < int(self.numberOfTickets.get())):
            self.error = ctk.CTkLabel(master=self.formFrame, text="Not enough seats available", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return

        bookingID = self.currentBooking.getCinema().makeBooking(self.currentBooking)
        self.bookingsList.append(str(bookingID))
        self.bookingComboBox.configure(values=self.bookingsList)

        self.successMessage = ctk.CTkLabel(master=self.formFrame, text="Booking Successful", text_color=SUCCESS_COLOUR, font=("Roboto", 18))
        self.successMessage.pack()          

    def __cancelBooking(self):

        from main import ERROR_COLOUR, SUCCESS_COLOUR, Booking, Show, Screen, db

        if(self.error != None):
            self.error.pack_forget()

        if(self.successMessage != None):
            self.successMessage.pack_forget() 

        if(self.selectedBookingID == None):
            self.error = ctk.CTkLabel(master=self.viewBookingsFrame, text="Select a Booking", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return 

        booking = None
        show = None
        selectedBooking = db.bookings.find_one({"_id" : ObjectId(self.selectedBookingID)})
        if(selectedBooking != None):
            showID = selectedBooking.get("show")
            showDB = db.shows.find_one({"_id": showID})
            if(showDB != None):
                screenID = showDB.get("screen_number")
                screenDB = db.screens.find_one({"_id": screenID})
                if(screenDB != None):
                    screen = Screen(screenDB.get("_id"), len(screenDB.get("seats")), screenDB.get("seats"))
                    show = Show(showID, showDB.get("show_date"), showDB.get("show_time"), showDB.get("available_seats"), screen)
        
                    booking = Booking(selectedBooking.get("_id"), selectedBooking.get("num_of_tickets"), show, "", "", selectedBooking.get("booking_date"), selectedBooking.get("cost"))

        if(booking == None):
            self.error = ctk.CTkLabel(master=self.viewBookingsFrame, text="Something Went Wrong", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return     

        success = booking.cancel()    

        if(success):    
            self.successMessage = ctk.CTkLabel(master=self.viewBookingsFrame, text="Booking Canceled Successfully", text_color=SUCCESS_COLOUR, font=("Roboto", 18))
            self.successMessage.pack()  

            self.bookingsList.remove(self.selectedBookingID)
            self.bookingComboBox.configure(values=self.bookingsList)
            self.selectedBookingID = None



    def __addShow(self):
        from main import currentCinema, ERROR_COLOUR, SUCCESS_COLOUR, db
        
        if(self.error != None):
            self.error.pack_forget()

        if(self.successMessage != None):
            self.successMessage.pack_forget() 
        
        if(self.selectedListingID == None):
            self.error = ctk.CTkLabel(master=self.addShowFrame, text="You have to select a listing first", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return  

        if(self.screenSelected.get() == "Select a Screen"):
            self.error = ctk.CTkLabel(master=self.addShowFrame, text="Select a screen", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return                 
        
        screenIndex = self.selectionScreens.index(self.screenSelected.get())
        showDate = self.showDate.get_date()
        showTimeHour = self.timeHours.get()
        showTimeMinutes = self.timeMinutes.get()
        showTime = f"{showTimeHour.zfill(2)}:{showTimeMinutes.zfill(2)}"
        showScreen = currentCinema.getScreens()[screenIndex]
        todayDate = datetime.date.today()
        
        success = False
        
        listing = db.listings.find_one({"_id": self.selectedListingID})
        numOfShows = 0
        if(listing != None):
            if(listing.get("shows") != None):
                numOfShows = len(listing.get("shows"))
            
        if(numOfShows == 4):
            self.error = ctk.CTkLabel(master=self.addShowFrame, text="There are already 4 shows associated with this listing", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return   
         
        if (showTimeHour == '' or showTimeMinutes == ''):
            self.error = ctk.CTkLabel(master=self.addShowFrame, text="Enter timings", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return 
        
        if(int(showTimeHour) > 23 or int(showTimeHour) < 0):
            self.error = ctk.CTkLabel(master=self.addShowFrame, text="Incorrect timings entered", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return 
        
        if(int(showTimeMinutes) > 59 or int(showTimeMinutes) < 0):
            self.error = ctk.CTkLabel(master=self.addShowFrame, text="Incorrect timings entered", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return  
                    
        if(showDate <= todayDate):
            self.error = ctk.CTkLabel(master=self.addShowFrame, text="Shows can't be before tomorrow", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return  
        
        if(self.loggedInUser.__class__.__name__ == "Manager"):
            success = self.currentListing.addShow(showDate.strftime("%d-%m-%Y"), showTime, showScreen)
            
        if(success):
            self.successMessage = ctk.CTkLabel(master=self.addShowFrame, text="Show added", text_color=SUCCESS_COLOUR, font=("Roboto", 18))
            self.successMessage.pack()
            
            date = showDate.strftime("%d-%m-%Y")

            newShow = ctk.CTkRadioButton(master=self.viewListingsFrame, text=f"Show {numOfShows+1} - {date} {showTime}", value=success, variable=self.selectedShow)
            self.showsButtons.append(newShow)
            newShow.pack(fill='x', padx=5, pady=5, side="left")  
            return              
        
    def __removeShow(self):
        from main import SUCCESS_COLOUR, ERROR_COLOUR

        if(self.error != None):
            self.error.pack_forget()

        if(self.successMessage != None):
            self.successMessage.pack_forget() 

        if(self.selectedListingID == None):
            self.error = ctk.CTkLabel(master=self.viewListingsFrame, text="Select a listing", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return   

        showNum = self.selectedShow.get()

        if(showNum == ''):
            self.error = ctk.CTkLabel(master=self.viewListingsFrame, text="Select a show", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return            

        success = self.currentListing.removeShow(showNum)

        if(success):
            self.successMessage = ctk.CTkLabel(master=self.viewListingsFrame, text="Show Removed", text_color=SUCCESS_COLOUR, font=("Roboto", 18))        
            self.successMessage.pack()

            self.__viewListings(self.choice)
                        

    def __loadListingsBooking(self, event=None):

        from main import db, currentCinema

        showSearchDate = self.calendar.selection_get()
        if(showSearchDate != None):
            showSearchDate = showSearchDate.strftime('%d-%m-%Y')
        
        showsDB = list(db.shows.find({"show_date": showSearchDate}))

        shows = []
        listingsDB = []
        cinemaDB = db.cinemas.find_one({"location": self.selectedCinema.get()})
        for show in showsDB:
            showScreen = show.get("screen_number")
            if(cinemaDB != None):
                if(showScreen not in cinemaDB.get("screens")):
                    continue
            shows.append(show.get("_id"))
            listingsDB.append(db.listings.find_one({"shows": show.get("_id")}).get("film_name"))
        
        self.availableListings = dict((listing, []) for listing in listingsDB)

        for i in range(len(shows)):
            self.availableListings[listingsDB[i]].append(shows[i])

        listingValues = list(self.availableListings.keys())
        if(listingValues == []):
            listingValues = [""]
        self.selectFilm.configure(values=listingValues)
        self.selectShowing.configure(values=[""])
        self.selectFilm.set(value="")
        self.selectShowing.set(value="")

    def __loadShowsBooking(self, value):

        from main import db

        if(value == "Empty"):
            return
        
        self.availableShows = []
        i = 1
        for id in self.availableListings[value]:
            showTime = db.shows.find_one({"_id": id}).get("show_time")
            self.availableShows.append(f"Show {i} - {showTime}")
            i+=1

        self.selectShowing.configure(values=self.availableShows)
        self.selectShowing.set(value="")

    def __clearListingInfo(self):
        self.filmName.delete(0, "end")
        self.filmGenre.delete(0, "end")
        self.filmAge.delete(0, "end")
        self.filmRating.delete(0, "end")
        self.filmDetails.delete(0, "end")
        self.actorDetails.delete(0, "end")
        self.filmLength1.delete(0, "end")
        self.filmLength2.delete(0, "end")      

    # Loads the selected listing info into the add/update forms entry boxes when the 'Update Listing' button is clicked and the add/update listing form frame is loaded
    def __loadListingInfo(self):

        from main import db, ERROR_COLOUR

        if(self.error != None):
            self.error.pack_forget()

        # If no listing is selected, output an error message
        if(self.selectedListingID == None):
            self.error = ctk.CTkLabel(master=self.addListingFrame, text="You have to select a listing to update", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return 

        # Selected listing info
        listing = db.listings.find_one({"_id": self.selectedListingID})

        self.__clearListingInfo()

        if(listing != None):
            # Load listing info in add/update listing form
            self.filmName.insert(-1, listing.get("film_name"))
            self.filmGenre.insert(-1, listing.get("film_genre"))
            self.filmAge.insert(-1, listing.get("film_age"))
            self.filmRating.insert(-1, listing.get("film_rating"))
            self.filmDetails.insert(-1, listing.get("film_description"))
            self.actorDetails.insert(-1, listing.get("cast"))
            film_length = listing.get("film_length")
            self.filmLength1.insert(-1, film_length.split("h ")[0])
            self.filmLength2.insert(-1, film_length.split("h ")[1].replace("m", ''))


    # Update the listing
    def __updateListing(self):
        from main import ERROR_COLOUR, SUCCESS_COLOUR, Listing, db

        listing = db.listings.find_one({"_id": self.selectedListingID})
        listingID = self.selectedListingID
        oldListingFilmName = ""
        if(listing != None):
            oldListingFilmName = listing["film_name"]
       
        filmName = self.filmName.get()
        filmGenre = self.filmGenre.get()
        filmAge = self.filmAge.get()
        filmRating = self.filmRating.get()
        filmDetails = self.filmDetails.get()
        cast = self.actorDetails.get()

        lengthHours = self.lengthHours.get()
        lengthMinutes = self.lengthMinutes.get()
        filmLength = f"{lengthHours}h {lengthMinutes}m"

        if(self.error != None):
            self.error.pack_forget()

        if(self.successMessage != None):
            self.successMessage.pack_forget()

        if(len(filmName) == 0):
            self.error = ctk.CTkLabel(master=self.addListingFrame, text="Film Name is required", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return 

        if(len(filmGenre) == 0):
            self.error = ctk.CTkLabel(master=self.addListingFrame, text="Film Genre is required", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return 

        try:
            filmAge = int(filmAge)
        except ValueError:
            self.error = ctk.CTkLabel(master=self.addListingFrame, text="Film Age should be a number", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return

        if(len(filmRating) == 0):
            self.error = ctk.CTkLabel(master=self.addListingFrame, text="Film Rating is required", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return 

        if(len(filmDetails) == 0):
            self.error = ctk.CTkLabel(master=self.addListingFrame, text="Film Details is required", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return 

        if(len(cast) == 0):
            self.error = ctk.CTkLabel(master=self.addListingFrame, text="Cast Details is required", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return 
        
        try:
            lengthHours = int(lengthHours)
        except ValueError:
            self.error = ctk.CTkLabel(master=self.addListingFrame, text="Film Length (Hours) should be a number", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return

        try:
            lengthMinutes = int(lengthMinutes)
        except ValueError:
            self.error = ctk.CTkLabel(master=self.addListingFrame, text="Film Length (Minutes) should be a number", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return

        success = False
        if(self.loggedInUser.__class__.__name__ == "Admin" or self.loggedInUser.__class__.__name__ == "Manager"):
            listing = Listing(0, filmName, filmLength, filmDetails, cast, filmGenre, filmAge, filmRating)
            success = listing.changeListingInformation(listingID, listing)

        if(success):
            self.successMessage = ctk.CTkLabel(master=self.addListingFrame, text="Listing updated", text_color=SUCCESS_COLOUR, font=("Roboto", 18))
            self.successMessage.pack()
        
            self.listings = list(db.listings.find())
            if filmName not in self.listingsList:
                for i in range(len(self.listingsList)):
                    if self.listingsList[i] == oldListingFilmName:
                        self.listingsList[i] = filmName

            self.listingComboBox.configure(values=self.listingsList)
        
        

    def __addListing(self):
        from main import ERROR_COLOUR, SUCCESS_COLOUR, currentCinema, Listing, db

        filmName = self.filmName.get()
        filmGenre = self.filmGenre.get()
        filmAge = self.filmAge.get()
        filmRating = self.filmRating.get()
        filmDetails = self.filmDetails.get()
        cast = self.actorDetails.get()

        lengthHours = self.lengthHours.get()
        lengthMinutes = self.lengthMinutes.get()
        filmLength = f"{lengthHours}h {lengthMinutes}m"

        if(self.error != None):
            self.error.pack_forget()

        if(self.successMessage != None):
            self.successMessage.pack_forget()

        if(len(filmName) == 0):
            self.error = ctk.CTkLabel(master=self.addListingFrame, text="Film Name is required", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return 

        if(len(filmGenre) == 0):
            self.error = ctk.CTkLabel(master=self.addListingFrame, text="Film Genre is required", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return 

        try:
            filmAge = int(filmAge)
        except ValueError:
            self.error = ctk.CTkLabel(master=self.addListingFrame, text="Film Age should be a number", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return

        if(len(filmRating) == 0):
            self.error = ctk.CTkLabel(master=self.addListingFrame, text="Film Rating is required", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return 

        if(len(filmDetails) == 0):
            self.error = ctk.CTkLabel(master=self.addListingFrame, text="Film Details is required", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return 

        if(len(cast) == 0):
            self.error = ctk.CTkLabel(master=self.addListingFrame, text="Cast Details is required", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return 
        
        try:
            lengthHours = int(lengthHours)
        except ValueError:
            self.error = ctk.CTkLabel(master=self.addListingFrame, text="Film Length (Hours) should be a number", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return

        try:
            lengthMinutes = int(lengthMinutes)
        except ValueError:
            self.error = ctk.CTkLabel(master=self.addListingFrame, text="Film Length (Minutes) should be a number", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return

        success = False
        if(self.loggedInUser.__class__.__name__ == "Admin" or self.loggedInUser.__class__.__name__ == "Manager"):
            listing = Listing(0, filmName, filmLength, filmDetails, cast, filmGenre, filmAge, filmRating)
            success = currentCinema.addListing(listing)

        if(success):
            self.successMessage = ctk.CTkLabel(master=self.addListingFrame, text="Listing added", text_color=SUCCESS_COLOUR, font=("Roboto", 18))
            self.successMessage.pack()

            self.__clearListingInfo()
        
            self.listings = list(db.listings.find())
            self.listingsList.append(filmName)
            self.listingComboBox.configure(values=self.listingsList)

    def __viewListings(self, choice):
        
        from main import db, Listing

        self.choice = choice
        selectedListing = self.listings[self.listingsList.index(self.selectedListing.get())]
        self.filmNameLabel.configure(text=("Film Name: " + selectedListing.get("film_name")))
        self.filmDateLabel.configure(text=("Film Release Date: " + str(selectedListing.get("film_age"))))
        self.filmDescriptionLabel.configure(text=("Film Description: " + selectedListing.get("film_description")))
        self.filmGenreLabel.configure(text=("Film Genre: " + selectedListing.get("film_genre")))
        self.filmRatingLabel.configure(text=("Film Rating: " + selectedListing.get("film_rating")))
        self.actorDetailsLabel.configure(text=("Cast: " + selectedListing.get("cast")))
        self.filmLengthLabel.configure(text=("Film Length: " + selectedListing.get("film_length")))
        self.selectedListingID = selectedListing.get("_id")
        self.currentListing = Listing(selectedListing.get("_id"), selectedListing.get("film_name"), selectedListing.get("film_length"), selectedListing.get("film_description"), selectedListing.get("cast"), selectedListing.get("film_genre"), selectedListing.get("film_age"), selectedListing.get("film_rating"), selectedListing.get("shows"))

        self.shows = []
        listing = db.listings.find_one({"_id": self.selectedListingID})
        
        if(listing != None):
            self.shows = listing.get("shows")

        for i in self.showsButtons:
            i.pack_forget()
        
        self.selectedShow = ctk.StringVar()
        for i in range(len(self.shows)):
            show = db.shows.find_one({"_id": self.shows[i]})
            if(show != None):
                showDate = show.get("show_date")
                showTime = show.get("show_time")
                r = ctk.CTkRadioButton(master=self.viewListingsFrame, text=f"Show {i+1} - {showDate} {showTime}", value=show.get("_id"), variable=self.selectedShow)
                self.showsButtons.append(r)
                r.pack(fill='x', padx=5, side="left")
            
    def __removeListing(self):
        from main import db, SUCCESS_COLOUR, ERROR_COLOUR, currentCinema

        if(self.error != None):
            self.error.pack_forget()

        if(self.successMessage != None):
            self.successMessage.pack_forget()

        listingFound = db.listings.find_one({"_id": self.selectedListingID})

        if(listingFound == None):
            self.error = ctk.CTkLabel(master=self.viewListingsFrame, text="Listing does not exist", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return 

        success = currentCinema.removeListing(self.selectedListingID)
        if(success):
            
            selectedListing = self.listings[self.listingsList.index(self.selectedListing.get())]
            self.listings.remove(selectedListing)
            self.listingsList.remove(listingFound.get("film_name"))
            self.listingComboBox.configure(values=self.listingsList)
            self.selectedListingID = None
            self.selectedListing.set("Select Listing")

            self.successMessage = ctk.CTkLabel(master=self.viewListingsFrame, text="Listing Removed", text_color=SUCCESS_COLOUR, font=("Roboto", 18))
            self.successMessage.pack()


    def switchFrames(self, frame):

        self.buttonsFrame.pack_forget()

        # Unpack all the view frames
        for i in self.frames:
            i.pack_forget()
        
        # Pack the view frame switched to
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        employeeType = self.loggedInUser.__class__.__name__
        if(employeeType == "Admin" or employeeType == "Manager"):
            if(frame == self.viewListingsFrame):
                self.bookingButton.configure(text="Add Listing", command=lambda: [self.switchFrames(self.addListingFrame), self.__clearListingInfo()])
                self.viewListingsButton.configure(text="Update Listing", command=lambda: [self.switchFrames(self.addListingFrame), self.__loadListingInfo()])
                self.viewBookingsButton.configure(text="Remove Listing", command=self.__removeListing)

                self.addShowButton = ctk.CTkButton(master=self.buttonsFrame, 
                                            text="Add Show", 
                                            width=150,
                                            height=75,
                                            font=("", 18, "bold"), 
                                            corner_radius=7,
                                            fg_color="#9f54fb",
                                            hover_color="#a722fa",
                                            command=lambda: self.switchFrames(self.addShowFrame))

                self.addShowButton.pack(side="left", padx=15)

                self.removeShowButton = ctk.CTkButton(master=self.buttonsFrame, 
                                            text="Remove Show", 
                                            width=150,
                                            height=75,
                                            font=("", 18, "bold"), 
                                            corner_radius=7,
                                            fg_color="#9f54fb",
                                            hover_color="#a722fa",
                                            command=self.__removeShow)

                self.removeShowButton.pack(side="left", padx=15)

                self.backButton = ctk.CTkButton(master=self.buttonsFrame, 
                                            text="Back", 
                                            width=150,
                                            height=75,
                                            font=("", 18, "bold"), 
                                            corner_radius=7,
                                            fg_color="#9f54fb",
                                            hover_color="#a722fa",
                                            command=self.back)

                self.backButton.pack(side="left", padx=15)

            if(frame == self.addListingFrame or frame == self.addShowFrame):
                self.viewBookingsButton.configure(text="", command=None, width=0)
                self.viewListingsButton.configure(text="", command=None, width=0)
                if(frame != self.addShowFrame):
                    self.addShowButton.configure(text="", command=None, width=0)
                self.removeShowButton.configure(text="", command=None, width=0)

        self.buttonsFrame.pack(fill="both", padx=20)

    def back(self):
        self.switchFrames(self.formFrame)
        self.bookingButton.configure(text="Booking Form", command=lambda: self.switchFrames(self.formFrame), width=250)
        self.viewListingsButton.configure(text="View Listings", command=lambda: self.switchFrames(self.viewListingsFrame), width=250)
        self.viewBookingsButton.configure(text="View Bookings", command=lambda: self.switchFrames(self.viewBookingsFrame), width=250)  
        self.backButton.pack_forget()      
        self.addShowButton.pack_forget()      
        self.removeShowButton.pack_forget()      
