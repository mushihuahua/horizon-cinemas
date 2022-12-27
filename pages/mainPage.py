import customtkinter as ctk
from tkcalendar import *

# Booking View
class MainFrame():
    def __init__(self, container):

        from datetime import datetime
        date = datetime.today().strftime('%Y-%m-%d')
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:])

        self.frame = ctk.CTkFrame(master=container, corner_radius=10)
        self.formFrame = ctk.CTkFrame(master=self.frame, corner_radius=10)

        self.viewTitle = ctk.CTkLabel(master=self.frame, text="Bookings", font=("Roboto", 48))
    
        self.calendarLabel = ctk.CTkLabel(master=self.frame, text="Select Date:", font=("Roboto", 15))
        self.calendar = Calendar(master=self.frame, 
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
        self.makeBookingButton = ctk.CTkButton(master=self.formFrame, 
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
                                    
        self.viewListingsButton = ctk.CTkButton(master=self.frame, 
                                    text="View Listings",
                                    width=200,
                                    height=40,
                                    font=("", 16, "bold"),
                                    corner_radius=7,
                                    fg_color="#bb86fc",
                                    hover_color="#9f54fb")


        self.viewTitle.pack(pady=(60,35))
        self.viewBookingsButton.pack(pady=(15, 10))
        self.viewListingsButton.pack(pady=(10, 30))

        self.calendarLabel.pack(pady=(0, 20))
        self.calendar.pack()

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