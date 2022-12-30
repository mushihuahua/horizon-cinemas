import customtkinter as ctk
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from tkcalendar import *


ERROR_COLOUR="#e23636"
SUCCESS_COLOUR="#66bb6a"

class MainFrame():
    def __init__(self, container, loggedInUser):

        date = datetime.today().strftime('%Y-%m-%d')
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:])

        self.loggedInUser = loggedInUser

        self.frames = []
        self.error = None
        self.successMessage = None 

        self.frame = ctk.CTkFrame(master=container, corner_radius=20)

        self.inFrame = ctk.CTkFrame(master=self.frame, corner_radius=20)
        self.makeBookingsFrame = ctk.CTkFrame(master=self.frame, corner_radius=20)
        self.viewBookingsFrame = ctk.CTkFrame(master=self.frame, corner_radius=20)
        self.viewListingsFrame = ctk.CTkFrame(master=self.frame, corner_radius=20)

        self.frames.append(self.inFrame)
        self.frames.append(self.makeBookingsFrame)
        self.frames.append(self.viewBookingsFrame)
        self.frames.append(self.viewListingsFrame)

        self.buttonsFrame = ctk.CTkFrame(master=self.frame, corner_radius=20)
        
        # self.info = InfoFrame(self.inFrame)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)

        self.employeeLabel = ctk.CTkLabel(master=self.inFrame,
                                text=f"{loggedInUser.fullName} - {loggedInUser.__class__.__name__}",
                                    font=("Roboto", 16))

        self.cinemaLabel = ctk.CTkLabel(master=self.inFrame, 
                            text="Bristol, Cabot Circus",
                            font=("Roboto", 16))

        self.text = ctk.CTkLabel(master=self.inFrame, 
                            text="Bookings View",
                            font=("Roboto", 48))


        # Bottom Nav/Buttons

        self.makeBookingsButton = ctk.CTkButton(master=self.buttonsFrame, 
                                    text="Make Booking", 
                                    width=250,
                                    height=75,
                                    font=("", 18, "bold"), 
                                    corner_radius=7,
                                    fg_color="#9f54fb",
                                    hover_color="#a722fa",
                                    command=lambda: self.switchFrames(self.makeBookingsFrame))

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


        

        # Make Bookings Frame

        self.formFrame = ctk.CTkFrame(master=self.makeBookingsFrame, corner_radius=10)

        self.createLabel = ctk.CTkLabel(master=self.makeBookingsFrame, text="Make Booking", font=("Roboto", 32))
        #self.createLabel.place(relx=.5, rely=.2, anchor="center")
        self.createLabel.pack(expand=True)





        self.calendarLabel = ctk.CTkLabel(master=self.makeBookingsFrame, text="Select Date:", font=("Roboto", 15))
        self.calendar = Calendar(master=self.makeBookingsFrame, 
                        selectmode='day', 
                        year=year, 
                        month=month, 
                        day=day,
                        font=("", 10))
        
        self.calendarLabel.pack(expand=True)
        self.calendar.pack(expand=True)

        
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
        
        self.formFrame.pack(pady=10, expand=True)

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





        # Listings Frame

        self.createLabel = ctk.CTkLabel(master=self.viewListingsFrame, text="Listings", font=("Roboto", 32))
        self.createLabel.place(relx=.5, rely=.2, anchor="center")

        # Bookings Frame

        self.createLabel = ctk.CTkLabel(master=self.viewBookingsFrame, text="Bookings", font=("Roboto", 32))
        self.createLabel.place(relx=.5, rely=.2, anchor="center")

        





        self.inFrame.pack(pady=20, padx=20, fill="both", expand=True)
        self.text.place(relx=.5, rely=.2, anchor="center")
        self.employeeLabel.place(relx=.5, rely=.3, anchor="center")
        self.cinemaLabel.place(relx=.5, rely=.35, anchor="center")

        self.buttonsFrame.pack(fill="both", padx=20)
        self.makeBookingsButton.pack(side="left", padx=(15, 15))
        self.viewListingsButton.pack(side="left", padx=15)
        self.viewBookingsButton.pack(side="left", padx=15)
        #self.viewEmployeesButton.pack(side="left", padx=15)
        #self.createEmployeeAccount.pack(side="left", padx=15)



    def switchFrames(self, frame):

        self.buttonsFrame.pack_forget()

        # Unpack all the view frames
        for i in self.frames:
            i.pack_forget()
        
        # Pack the view frame switched to
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.buttonsFrame.pack(fill="both", padx=20)

