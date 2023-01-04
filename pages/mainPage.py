import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkcalendar import *
# Booking View
class MainFrame():
    def __init__(self, container, loggedInUser):

        from datetime import datetime
        date = datetime.today().strftime('%Y-%m-%d')
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:])

        self.loggedInUser = loggedInUser
        self.frames = []
        self.error = None
        self.successMessage = None
        self.selectedListingID = None

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

        self.viewTitle = ctk.CTkLabel(master=self.formFrame, text="Booking Form", font=("Roboto", 48))
    
        self.calendarLabel = ctk.CTkLabel(master=self.formFrame, text="Select Date:", font=("Roboto", 15))
        self.calendar = Calendar(master=self.formFrame, 
                        selectmode='day', 
                        year=year, 
                        month=month, 
                        day=day,
                        font=("", 10))
    
        self.selectFilmLabel = ctk.CTkLabel(master=self.formFrame, text="Select Film:", font=("Roboto", 15))
        self.selectFilm = ctk.CTkOptionMenu(master=self.formFrame, 
                            values=["Film 1", "Film 2", "Etc."],
                            width=200,
                            height=30,
                            font=("", 16, "bold"),
                            corner_radius=4)
        self.selectShowingLabel = ctk.CTkLabel(master=self.formFrame, text="Select Showing:", font=("Roboto", 15))    
        self.selectShowing = ctk.CTkOptionMenu(master=self.formFrame, 
                            values=["Showing 1", "Showing 2", "Etc."],
                            width=200,
                            height=30,
                            font=("", 16, "bold"),
                            corner_radius=4)  
        self.maxSeatsLabel = ctk.CTkLabel(master=self.formFrame, text="Max Seats:", font=("Roboto", 15)) 
        self.maxSeats = ctk.CTkLabel(master=self.formFrame, text="0", font=("Roboto", 15)) 
        self.selectTicketsLabel = ctk.CTkLabel(master=self.formFrame, text="Select Tickets", font=("Roboto", 18)) 
        self.lowTicketsLabel = ctk.CTkLabel(master=self.formFrame, text="Lower Hall Tickets:", font=("Roboto", 15)) 
        self.lowHallTickets = ctk.CTkOptionMenu(master=self.formFrame, 
                            values=["1", "2", "Etc."],
                            width=200,
                            height=30,
                            font=("", 16, "bold"),
                            corner_radius=4)    
        self.upperTicketsLabel = ctk.CTkLabel(master=self.formFrame, text="Upper Hall Tickets:", font=("Roboto", 15)) 
        self.upperHallTickets = ctk.CTkOptionMenu(master=self.formFrame, 
                            values=["1", "2", "Etc."],
                            width=200,
                            height=30,
                            font=("", 16, "bold"),
                            corner_radius=4) 
        self.vipTicketsLabel = ctk.CTkLabel(master=self.formFrame, text="VIP Tickets:", font=("Roboto", 15)) 
        self.vipHallTickets = ctk.CTkOptionMenu(master=self.formFrame, 
                            values=["1", "2", "Etc."],
                            width=200,
                            height=30,
                            font=("", 16, "bold"),
                            corner_radius=4)                                     
        self.totalPriceLabel = ctk.CTkLabel(master=self.formFrame, text="Total Price:", font=("Roboto", 15)) 
        self.totalPrice = ctk.CTkLabel(master=self.formFrame, text="£0", font=("Roboto", 18)) 

        self.availabilityLabel = ctk.CTkLabel(master=self.formFrame, text="Availability:", font=("Roboto", 15)) 
        self.availability = ctk.CTkLabel(master=self.formFrame, text=" ", font=("Roboto", 18)) 

        self.makeBookingButton = ctk.CTkButton(master=self.formFrame, 
                                    text="Make Booking",
                                    width=200,
                                    height=40,
                                    font=("", 16, "bold"),
                                    corner_radius=7)

        self.formFrame.pack(pady=20, padx=20, fill="both", expand=True)

        self.viewTitle.place(relx=.5, rely=.1, anchor="center")

        self.calendarLabel.place(relx=.38, rely=.3, anchor="center")
        self.calendar.place(relx=.5, rely=.3, anchor="center")

        self.selectFilmLabel.place(relx=.4, rely=.45, anchor="center")
        self.selectFilm.place(relx=.5, rely=.45, anchor="center")

        self.selectShowingLabel.place(relx=.4, rely=.5, anchor="center")
        self.selectShowing.place(relx=.5, rely=.5, anchor="center")

        self.selectTicketsLabel.place(relx=.5, rely=.55, anchor="center")
        self.lowTicketsLabel.place(relx=.35, rely=.6, anchor="center")
        self.lowHallTickets.place(relx=.35, rely=.65, anchor="center")
        self.upperTicketsLabel.place(relx=.5, rely=.6, anchor="center")
        self.upperHallTickets.place(relx=.5, rely=.65, anchor="center")
        self.vipTicketsLabel.place(relx=.65, rely=.6, anchor="center")
        self.vipHallTickets.place(relx=.65, rely=.65, anchor="center")
        
        self.totalPriceLabel.place(relx=.4, rely=.7, anchor="center")
        self.totalPrice.place(relx=.5, rely=.7, anchor="center")
        self.availabilityLabel.place(relx=.4, rely=.75, anchor="center")
        self.availability.place(relx=.5, rely=.75, anchor="center")
        self.makeBookingButton.place(relx=.5, rely=.8, anchor="center")

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

        self.selectedListing = ctk.StringVar()

        if(len(self.listingsList) == 0):
            self.listingsList = ["Empty"]

        self.listingComboBox = ctk.CTkComboBox(master=self.viewListingsFrame, font=("", 15), values=self.listingsList, variable=self.selectedListing, command=self.__viewListings, height=40, width=350)
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
        self.showsLabel.pack(padx=20, pady=5, anchor="w")

        # View Bookings
        self.viewBookingsLabel = ctk.CTkLabel(master=self.viewBookingsFrame, text="View Bookings", font=("Roboto", 32, "bold"))
        self.viewBookingsLabel.pack(pady=40, padx=30)
        
        self.bookings = db.bookings.find()
        self.bookingsList = [listing.get("film_name") for listing in self.listings]

        if(len(list(self.bookings)) == 0):
            self.bookingsList = ["Empty"]

        self.bookingComboBox = ctk.CTkComboBox(master=self.viewBookingsFrame, font=("", 15), values=self.bookingsList, height=40, width=350)
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
                        hover_color="#9f54fb")
        
        self.cancelButton.pack(pady=10)

        # Add Listing
        self.listingFormLabel = ctk.CTkLabel(master=self.addListingFrame, text="Listing Form", font=("Roboto", 32, "bold"))
        self.listingFormLabel.place(relx=.5, rely=.05, anchor="center")

        self.filmName = ctk.CTkEntry(master=self.addListingFrame, 
                width=250, 
                height=52, 
                placeholder_text="Film Name", 
                font=("Roboto", 14))
        self.filmName.place(relx=.425, rely=.15, anchor="center")
        # self.firstNameEntry.bind('<Return>', self.__createAccount)

        self.filmGenre = ctk.CTkEntry(master=self.addListingFrame, 
                width=250, 
                height=52, 
                placeholder_text="Film Genre", 
                font=("Roboto", 14))
        self.filmGenre.place(relx=.575, rely=.15, anchor="center")
        # self.firstNameEntry.bind('<Return>', self.__createAccount)

        self.filmAge = ctk.CTkEntry(master=self.addListingFrame, 
                width=250, 
                height=52, 
                placeholder_text="Film Release Year", 
                font=("Roboto", 14))
        self.filmAge.place(relx=.425, rely=.25, anchor="center")
        # self.firstNameEntry.bind('<Return>', self.__createAccount)

        self.filmRating = ctk.CTkEntry(master=self.addListingFrame, 
                width=250, 
                height=52, 
                placeholder_text="Film Rating", 
                font=("Roboto", 14))
        self.filmRating.place(relx=.575, rely=.25, anchor="center")
        # self.firstNameEntry.bind('<Return>', self.__createAccount)

        self.lengthHours = tk.StringVar()
        self.filmLength1 = ttk.Spinbox(master=self.addListingFrame, from_=0, to=4, textvariable=self.lengthHours, width=12, font=("Roboto", 16))
        self.filmLength1.place(relx=.45, rely=.325, anchor="center")

        self.lengthMinutes = tk.StringVar()
        self.filmLength2 = ttk.Spinbox(master=self.addListingFrame, from_=0, to=59, textvariable=self.lengthMinutes, width=12, font=("Roboto", 16))
        self.filmLength2.place(relx=.55, rely=.325, anchor="center")

        self.filmDetails = ctk.CTkEntry(master=self.addListingFrame, 
                width=500, 
                height=52, 
                placeholder_text="Film Details", 
                font=("Roboto", 14))
        self.filmDetails.place(relx=.5, rely=.4, anchor="center")
        # self.firstNameEntry.bind('<Return>', self.__createAccount)

        self.actorDetails = ctk.CTkEntry(master=self.addListingFrame, 
                width=500, 
                height=52, 
                placeholder_text="Cast", 
                font=("Roboto", 14))
        self.actorDetails.place(relx=.5, rely=.475, anchor="center")
        # self.firstNameEntry.bind('<Return>', self.__createAccount)

        self.addButton = ctk.CTkButton(master=self.addListingFrame, 
                        text="Add Listing", 
                        width=250, 
                        height=52, 
                        font=("Roboto", 20),
                        fg_color="#bb86fc",
                        hover_color="#9f54fb",
                        command=self.__addListing)
        
        self.addButton.place(relx=.5, rely=.550, anchor="center")
    
        self.updateButton = ctk.CTkButton(master=self.addListingFrame, 
                        text="Update Listing", 
                        width=250, 
                        height=52, 
                        font=("Roboto", 20),
                        fg_color="#bb86fc",
                        hover_color="#9f54fb",
                        command=self.__updateListing)
        
        self.updateButton.place(relx=.5, rely=.625, anchor="center")


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
        self.showTimeLabel.place(relx=.37, rely=.25, anchor="center")

        timeHours = tk.StringVar()
        self.showTime1 = ttk.Spinbox(master=self.addShowFrame, from_=0, to=23, textvariable=timeHours, width=12, font=("Roboto", 16))
        self.showTime1.place(relx=.45, rely=.25, anchor="center")

        timeMinutes = tk.StringVar()
        self.showTime2 = ttk.Spinbox(master=self.addShowFrame, from_=0, to=59, textvariable=timeMinutes, width=12, font=("Roboto", 16))
        self.showTime2.place(relx=.55, rely=.25, anchor="center")

        self.addShowButton = ctk.CTkButton(master=self.addShowFrame, 
                        text="Add Show", 
                        width=250, 
                        height=52, 
                        font=("Roboto", 20),
                        fg_color="#bb86fc",
                        hover_color="#9f54fb")
        
        self.addShowButton.place(relx=.5, rely=.35, anchor="center")        
    
    # Loads the selected listing info into the add/update forms entry boxes when the 'Update Listing' button is clicked and the add/update listing form frame is loaded
    def __loadListingInfo(self):
        from main import ERROR_COLOUR, SUCCESS_COLOUR, currentCinema, Listing, db
        
        # Selected listing info
        listing = db.listings.find_one({"_id": self.selectedListingID})

        # Load listing info in add/update listing form
        self.filmName.insert(-1, listing.get("film_name"))
        self.filmGenre.insert(-1, listing.get("film_genre"))
        self.filmAge.insert(-1, listing.get("film_age"))
        self.filmRating.insert(-1, listing.get("film_rating"))
        self.filmDetails.insert(-1, listing.get("film_description"))
        self.actorDetails.insert(-1, listing.get("cast"))
        film_length = listing.get("film_length")
        self.filmLength1.insert(-1, film_length[0])
        self.filmLength2.insert(-1, film_length[3:-1])


    # Update the listing
    def __updateListing(self):
        from main import ERROR_COLOUR, SUCCESS_COLOUR, currentCinema, Listing, db

        listing = db.listings.find_one({"_id": self.selectedListingID})
        listingID = self.selectedListingID
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
            listing = Listing(filmName, filmLength, filmDetails, cast, filmGenre, filmAge, filmRating)
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
            listing = Listing(filmName, filmLength, filmDetails, cast, filmGenre, filmAge, filmRating)
            success = currentCinema.addListing(listing)

        if(success):
            self.successMessage = ctk.CTkLabel(master=self.addListingFrame, text="Listing added", text_color=SUCCESS_COLOUR, font=("Roboto", 18))
            self.successMessage.pack()
        
            self.listings = list(db.listings.find())
            self.listingsList.append(filmName)
            self.listingComboBox.configure(values=self.listingsList)

    def __viewListings(self, choice):
        
        from main import db

        selectedListing = self.listings[self.listingsList.index(self.selectedListing.get())]
        self.filmNameLabel.configure(text=("Film Name: " + selectedListing.get("film_name")))
        self.filmDateLabel.configure(text=("Film Release Date: " + str(selectedListing.get("film_age"))))
        self.filmDescriptionLabel.configure(text=("Film Description: " + selectedListing.get("film_description")))
        self.filmGenreLabel.configure(text=("Film Genre: " + selectedListing.get("film_genre")))
        self.filmRatingLabel.configure(text=("Film Rating: " + selectedListing.get("film_rating")))
        self.actorDetailsLabel.configure(text=("Cast: " + selectedListing.get("cast")))
        self.filmLengthLabel.configure(text=("Film Length: " + selectedListing.get("film_length")))
        self.selectedListingID = selectedListing.get("_id")

        self.shows = []
        self.showsButtons = []
        listing = db.listings.find_one({"_id": self.selectedListingID})
        
        if(listing != None):
            self.shows = listing.get("shows")

        for i in self.showsButtons:
            i.pack_forget()

        self.selectedShow = ctk.StringVar()
        for i in range(len(self.shows)):
            r = ctk.CTkRadioButton(master=self.viewListingsFrame, text=f"Show {i+1} - Date Time", value=f"show{i+1}", variable=self.selectedShow)
            self.showsButtons.append(r)
            r.pack(fill='x', padx=5, pady=5)


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
                self.bookingButton.configure(text="Add Listing", command=lambda: self.switchFrames(self.addListingFrame))
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
                                            command=None)

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