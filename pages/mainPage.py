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

        self.frames = []

        self.frame = ctk.CTkFrame(master=container, corner_radius=10)
        self.formFrame = ctk.CTkFrame(master=self.frame, corner_radius=10)

        self.frames.append(self.formFrame)

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
                                    hover_color="#a722fa")

        self.viewListingsButton = ctk.CTkButton(master=self.buttonsFrame, 
                                    text="View Listings", 
                                    width=250,
                                    height=75,
                                    font=("", 18, "bold"), 
                                    corner_radius=7,
                                    fg_color="#9f54fb",
                                    hover_color="#a722fa")

        self.viewBookingsButton = ctk.CTkButton(master=self.buttonsFrame, 
                                    text="View Bookings", 
                                    width=400,
                                    height=75,
                                    font=("", 18, "bold"), 
                                    corner_radius=7,
                                    fg_color="#9f54fb",
                                    hover_color="#a722fa")

        self.buttonsFrame.pack(fill="both", padx=20)
        self.bookingButton.pack(side="left", padx=(15, 15))
        self.viewListingsButton.pack(side="left", padx=15)
        self.viewBookingsButton.pack(side="left", padx=15)


    def switchFrames(self, frame):

        self.buttonsFrame.pack_forget()

        # Unpack all the view frames
        for i in self.frames:
            i.pack_forget()
        
        # Pack the view frame switched to
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.buttonsFrame.pack(fill="both", padx=20)