import customtkinter as ctk
import tkinter as tk
from werkzeug.security import generate_password_hash, check_password_hash
from main import currentCinema, db, cityContainer
from bson.objectid import ObjectId


ERROR_COLOUR="#e23636"
SUCCESS_COLOUR="#66bb6a"

class ManagerFrame():
    def __init__(self, container, loggedInUser):

        self.loggedInUser = loggedInUser
        self.frames = []
        self.error = None
        self.successMessage = None
        self.selectedEmployeeId = None

        self.frame = ctk.CTkFrame(master=container, corner_radius=20)


        self.inFrame = ctk.CTkFrame(master=self.frame, corner_radius=20)
        
        self.addCityFrame = ctk.CTkFrame(master=self.frame, corner_radius=20)
        self.addCinemaFrame = ctk.CTkFrame(master=self.frame, corner_radius=20)
        self.viewEmployeesFrame = ctk.CTkFrame(master=self.frame, corner_radius=20)
        self.createAccountFrame = ctk.CTkFrame(master=self.frame, corner_radius=20)

        self.frames.append(self.inFrame)
        
        self.frames.append(self.addCityFrame)
        self.frames.append(self.addCinemaFrame)
        self.frames.append(self.viewEmployeesFrame)
        self.frames.append(self.createAccountFrame)


        self.buttonsFrame = ctk.CTkFrame(master=self.frame, corner_radius=20)
        
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)

        self.employeeLabel = ctk.CTkLabel(master=self.inFrame,
                                text=f"{loggedInUser.fullName} - {loggedInUser.__class__.__name__}",
                                    font=("Roboto", 16))

        self.cinemaLabel = ctk.CTkLabel(master=self.inFrame, 
                            text=f"{currentCinema.getCity().getName()}, {currentCinema.getLocation()}",
                            font=("Roboto", 16))

        self.text = ctk.CTkLabel(master=self.inFrame, 
                            text="Manager View",
                            font=("Roboto", 48))

        # BUTTONS
        self.addCityButton = ctk.CTkButton(master=self.buttonsFrame, 
                                    text="Add City", 
                                    width=250,
                                    height=75,
                                    font=("", 18, "bold"), 
                                    corner_radius=7,
                                    fg_color="#9f54fb",
                                    hover_color="#a722fa",
                                    command=lambda: self.switchFrames(self.addCityFrame))

        self.addCinemaButton = ctk.CTkButton(master=self.buttonsFrame, 
                                    text="Add Cinema", 
                                    width=250,
                                    height=75,
                                    font=("", 18, "bold"), 
                                    corner_radius=7,
                                    fg_color="#9f54fb",
                                    hover_color="#a722fa",
                                    command=lambda: self.switchFrames(self.addCinemaFrame))

        self.viewEmployeesButton = ctk.CTkButton(master=self.buttonsFrame, 
                                    text="View Staff Members", 
                                    width=400,
                                    height=75,
                                    font=("", 18, "bold"), 
                                    corner_radius=7,
                                    fg_color="#9f54fb",
                                    hover_color="#a722fa",
                                    command=lambda: self.switchFrames(self.viewEmployeesFrame))

        self.createEmployeeAccount = ctk.CTkButton(master=self.buttonsFrame, 
                                    text="Create Staff Member Account", 
                                    width=400,
                                    height=75,
                                    font=("", 18, "bold"), 
                                    corner_radius=7,
                                    fg_color="#9f54fb",
                                    hover_color="#a722fa",
                                    command=lambda: self.switchFrames(self.createAccountFrame))

        # CREATE ACCOUNT
        self.createLabel = ctk.CTkLabel(master=self.createAccountFrame, text="Create Staff Member Account", font=("Roboto", 32))
        self.createLabel.place(relx=.5, rely=.2, anchor="center")

        self.firstNameEntry = ctk.CTkEntry(master=self.createAccountFrame, 
                        width=500, 
                        height=52, 
                        placeholder_text="First Name", 
                        font=("Roboto", 14))
        self.firstNameEntry.place(relx=.5, rely=.3, anchor="center")
        self.firstNameEntry.bind('<Return>', self.__createAccount)

        self.lastNameEntry = ctk.CTkEntry(master=self.createAccountFrame, 
                        width=500, 
                        height=52, 
                        placeholder_text="Last Name", 
                        font=("Roboto", 14))
        self.lastNameEntry.place(relx=.5, rely=.4, anchor="center")
        self.lastNameEntry.bind('<Return>', self.__createAccount)

        self.typeValue = ctk.StringVar(master=self.createAccountFrame)
        self.typeValue.set("Select Staff Type")
        types = ["Booking Staff", "Admin", "Manager"]

        self.staffType = ctk.CTkOptionMenu(master=self.createAccountFrame,
                                    fg_color="#bb86fc",
                                    button_color="#9f54fb",
                                    button_hover_color="#a722fa", 
                                    variable=self.typeValue, 
                                    values=types,
                                    width=500, 
                                    height=52)

        self.staffType.place(relx=.5, rely=.5, anchor="center")

        self.idEntry = ctk.CTkEntry(master=self.createAccountFrame, 
                        width=500, 
                        height=52, 
                        placeholder_text="Employee ID", 
                        font=("Roboto", 14))
        self.idEntry.place(relx=.5, rely=.6, anchor="center")
        self.idEntry.bind('<Return>', self.__createAccount)


        self.pwdEntry = ctk.CTkEntry(master=self.createAccountFrame, 
                        width=500, 
                        height=52, 
                        placeholder_text="Password",
                        show="*",
                        font=("Roboto", 14))
        self.pwdEntry.place(relx=.5, rely=.7, anchor="center")
        self.pwdEntry.bind('<Return>', self.__createAccount)

        self.createButton = ctk.CTkButton(master=self.createAccountFrame, 
                        text="Create Account", 
                        width=250, 
                        height=52, 
                        font=("Roboto", 20),
                        fg_color="#bb86fc",
                        hover_color="#9f54fb",
                        command=self.__createAccount)

        self.createButton.place(relx=.5, rely=.8, anchor="center")

        # VIEW EMPLOYEES                
        self.viewEmployeesLabel = ctk.CTkLabel(master=self.viewEmployeesFrame, text="View Staff Members", font=("Roboto", 32, "bold"))
        self.viewEmployeesLabel.pack(pady=40, padx=30)

        self.employees = list(db.staff.find())
        self.employeeList = [(member.get("first_name") + " " + member.get("last_name") + " - " + str(member.get("_id"))) for member in self.employees]

        self.employeeComboBox = ctk.CTkComboBox(master=self.viewEmployeesFrame, font=("", 15), values=self.employeeList, command=self.__employeeChooser, height=40, width=350)
        self.employeeComboBox.pack(padx=20, pady=20)


        self.employeeIDLabel = ctk.CTkLabel(master=self.viewEmployeesFrame, text="Employee ID: ", font=("", 18))
        self.employeeIDLabel.pack(padx=20, pady=20)

        self.employeeNameLabel = ctk.CTkLabel(master=self.viewEmployeesFrame, text="Employee Name: ", font=("", 18))
        self.employeeNameLabel.pack(padx=20, pady=20)
        
        self.employeeTypeLabel = ctk.CTkLabel(master=self.viewEmployeesFrame, text="Employee Type: ", font=("", 18))
        self.employeeTypeLabel.pack(padx=20, pady=20)

        self.employeeCinemaLabel = ctk.CTkLabel(master=self.viewEmployeesFrame, text="Employee Cinema: ", font=("", 18))
        self.employeeCinemaLabel.pack(padx=20, pady=20)

        self.removeButton = ctk.CTkButton(master=self.viewEmployeesFrame, 
                        text="Remove Staff Member Account", 
                        width=300, 
                        height=60, 
                        font=("Roboto", 20),
                        fg_color="#bb86fc",
                        hover_color="#9f54fb",
                        command = self.__removeEmployee)

        self.removeButton.pack(pady=20) 

        # ADD CITY 
        self.addCityLabel = ctk.CTkLabel(master=self.addCityFrame, text="Add City", font=("Roboto", 32, "bold"))
        self.addCityLabel.place(relx=.5, rely=.1, anchor="center")

        self.cityName = ctk.CTkEntry(master=self.addCityFrame, 
                        width=500, 
                        height=52, 
                        placeholder_text="City Name", 
                        font=("Roboto", 14))
        self.cityName.place(relx=.5, rely=.25, anchor="center")
        self.cityName.bind('<Return>', self.__addCity)

        self.cityMorningPrice = ctk.CTkEntry(master=self.addCityFrame, 
                        width=150, 
                        height=52, 
                        placeholder_text="City Morning Price", 
                        font=("Roboto", 14))
        self.cityMorningPrice.place(relx=.35, rely=.4, anchor="center")
        self.cityMorningPrice.bind('<Return>', self.__addCity)

        self.cityAfternoonPrice = ctk.CTkEntry(master=self.addCityFrame, 
                        width=150, 
                        height=52, 
                        placeholder_text="City Afternoon Price", 
                        font=("Roboto", 14))
        self.cityAfternoonPrice.place(relx=.5, rely=.4, anchor="center")
        self.cityAfternoonPrice.bind('<Return>', self.__addCity)

        self.cityEveningPrice = ctk.CTkEntry(master=self.addCityFrame, 
                        width=150, 
                        height=52, 
                        placeholder_text="City Evening Price", 
                        font=("Roboto", 14))
        self.cityEveningPrice.place(relx=.65, rely=.4, anchor="center")
        self.cityEveningPrice.bind('<Return>', self.__addCity)

        self.addCity = ctk.CTkButton(master=self.addCityFrame, 
                        text="Add City", 
                        width=250, 
                        height=52, 
                        font=("Roboto", 20),
                        fg_color="#bb86fc",
                        hover_color="#9f54fb",
                        command = self.__addCity)

        self.addCity.place(relx=.5, rely=.55, anchor="center")       


        # ADD CINEMA
        self.addCinemaLabel = ctk.CTkLabel(master=self.addCinemaFrame, text="Add Cinema", font=("Roboto", 32, "bold"))
        self.addCinemaLabel.pack(pady=(150, 25))

        cities = [city for city in db.cities.find()] 
        self.cityChoices = [city.get("name") for city in cities]
        self.cityChoice = ctk.StringVar(master=self.addCinemaFrame)
        self.cityChoice.set("Select City")

        self.cityList = ctk.CTkOptionMenu(master=self.addCinemaFrame,
                                    fg_color="#bb86fc",
                                    button_color="#9f54fb",
                                    button_hover_color="#a722fa", 
                                    variable=self.cityChoice, 
                                    values=self.cityChoices,
                                    width=500, 
                                    height=52)
                                
        self.cityList.pack(pady=20) 

        screens = [str(i+1) for i in range(6)]
        self.screenChoice = ctk.StringVar(master=self.addCinemaFrame)
        self.screenChoice.set("Number of Screens")

        self.noOfScreens = ctk.CTkOptionMenu(master=self.addCinemaFrame,
                                    fg_color="#bb86fc",
                                    button_color="#9f54fb",
                                    button_hover_color="#a722fa", 
                                    variable=self.screenChoice, 
                                    values=screens,
                                    width=500, 
                                    height=52)
                                
        self.noOfScreens.pack(pady=20) 

        self.locationEntry = ctk.CTkEntry(master=self.addCinemaFrame, 
                        width=500, 
                        height=52, 
                        placeholder_text="Cinema Location", 
                        font=("Roboto", 14))
        self.locationEntry.pack(pady=20)
        self.locationEntry.bind('<Return>', self.__addCinema)

        self.addCinema = ctk.CTkButton(master=self.addCinemaFrame, 
                        text="Add Cinema", 
                        width=250, 
                        height=52, 
                        font=("Roboto", 20),
                        fg_color="#bb86fc",
                        hover_color="#9f54fb",
                        command=self.__addCinema)

        self.addCinema.pack(pady=20)        
               

        # DISPLAY
        self.inFrame.pack(pady=20, padx=20, fill="both", expand=True)
        self.text.place(relx=.5, rely=.2, anchor="center")
        self.employeeLabel.place(relx=.5, rely=.3, anchor="center")
        self.cinemaLabel.place(relx=.5, rely=.35, anchor="center")

        self.buttonsFrame.pack(fill="both", padx=20)
        self.addCityButton.pack(side="left", padx=(15, 15))
        self.addCinemaButton.pack(side="left", padx=15)
        self.viewEmployeesButton.pack(side="left", padx=15)
        self.createEmployeeAccount.pack(side="left", padx=15)

    def __addCity(self, event=None):
        cityName = self.cityName.get()
        morningPrice = self.cityMorningPrice.get()
        afternoonPrice = self.cityAfternoonPrice.get()
        eveningPrice = self.cityEveningPrice.get()

        if(self.error != None):
            self.error.pack_forget()
        
        if(self.successMessage != None):
            self.successMessage.pack_forget()
        
        if(len(cityName) == 0):
            self.error = ctk.CTkLabel(master=self.addCityFrame, text="Invalid city name", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return

        cityExists = db.cities.find_one({"name": cityName.capitalize()})

        if(cityExists != None):
            self.error = ctk.CTkLabel(master=self.addCityFrame, text="City already exists", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return

        try:
            morningPrice = int(morningPrice)
            afternoonPrice = int(afternoonPrice)
            eveningPrice = int(eveningPrice)

        except ValueError:
            self.error = ctk.CTkLabel(master=self.addCityFrame, text="Prices should be a number", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return

        success = False
        if(self.loggedInUser.__class__.__name__ == "Manager"):
            success = cityContainer.addCity(cityName, morningPrice, afternoonPrice, eveningPrice)
            
        if(success):
            self.successMessage = ctk.CTkLabel(master=self.addCityFrame, text="City added successfully", text_color=SUCCESS_COLOUR, font=("Roboto", 18))
            self.successMessage.pack()

            self.cityChoices.append(cityName)
            self.cityList.configure(values=self.cityChoices)

            self.cityName.delete(0, "end")
            self.cityMorningPrice.delete(0, "end")
            self.cityAfternoonPrice.delete(0, "end")
            self.cityEveningPrice.delete(0, "end")
        
        else:
            self.error = ctk.CTkLabel(master=self.addCityFrame, text="Error occured, city could not be added", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()

    def __addCinema(self, event=None):
        from main import Cinema, City

        cityName = self.cityChoice.get()
        noOfScreens = self.screenChoice.get()
        cinemaLocation = self.locationEntry.get()

        if(self.error != None):
            self.error.pack_forget()
        
        if(self.successMessage != None):
            self.successMessage.pack_forget()

        if(cityName == "Select City"):
            self.error = ctk.CTkLabel(master=self.addCinemaFrame, text="Select a City", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return 

        if(noOfScreens == "Number of Screens"):
            self.error = ctk.CTkLabel(master=self.addCinemaFrame, text="Select Number of Screens", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return   

        if(len(cinemaLocation) == 0):
            self.error = ctk.CTkLabel(master=self.addCinemaFrame, text="Invalid cinema location", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return    

        self.successMessage = ctk.CTkLabel(master=self.addCinemaFrame, text="This may take around 15 seconds", text_color=SUCCESS_COLOUR, font=("Roboto", 18))
        self.successMessage.pack()

        dbCity = db.cities.find_one({"name": cityName})
        if(dbCity != None):
            city = City(dbCity.get("name").capitalize(), dbCity.get("morning_price"), dbCity.get("afternoon_price"), dbCity.get("evening_price"))
            cinema = Cinema(0, city, cinemaLocation, int(noOfScreens))

            if(self.loggedInUser.__class__.__name__ == "Manager"):

                success = city.addCinema(cinema)

                if(success):
                    self.successMessage.configure(text="Cinema successfully added")

                    self.locationEntry.delete(0, "end")
                    self.cityChoice.set("Select City")
                    self.screenChoice.set("Number of Screens")   

                    return 
        else:
            self.error = ctk.CTkLabel(master=self.addCinemaFrame, text="City does not exist anymore", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return                

    def __createAccount(self, event=None):

        firstName = self.firstNameEntry.get()
        lastName = self.lastNameEntry.get()
        id = self.idEntry.get()
        pwd = self.pwdEntry.get()
        empType = self.typeValue.get()

        if(self.error != None):
            self.error.pack_forget()
        
        if(self.successMessage != None):
            self.successMessage.pack_forget()

        if(len(firstName) <= 1):
            self.error = ctk.CTkLabel(master=self.createAccountFrame, text="Invalid first name", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return   
        
        if(len(lastName) <= 1):
            self.error = ctk.CTkLabel(master=self.createAccountFrame, text="Invalid last name", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return   

        try:
            id = int(id)

            if(empType == "Select Staff Type"):
                self.error = ctk.CTkLabel(master=self.createAccountFrame, text="Select a Staff Type", text_color=ERROR_COLOUR, font=("Roboto", 18))
                self.error.pack()
                return

            if(len(str(id)) != 6):
                self.error = ctk.CTkLabel(master=self.createAccountFrame, text="Employee ID should be a 6 digit number", text_color=ERROR_COLOUR, font=("Roboto", 18))
                self.error.pack()
                return
            
            import main

            if(main.db.staff.find_one({"_id": id}) != None):
                self.error = ctk.CTkLabel(master=self.createAccountFrame, text="Employee ID already exists", text_color=ERROR_COLOUR, font=("Roboto", 18))
                self.error.pack()
                return

            if(len(str(pwd)) < 8 or len(str(pwd)) > 16):
                self.error = ctk.CTkLabel(master=self.createAccountFrame, text="The password should be 8 to 16 characters long", text_color=ERROR_COLOUR, font=("Roboto", 18))
                self.error.pack()
                return

            success = False
            if(self.loggedInUser.__class__.__name__ == "Manager"):
                success = currentCinema.createNewEmployee(firstName, lastName, id, generate_password_hash(pwd), empType)

            if(success):
                self.successMessage = ctk.CTkLabel(master=self.createAccountFrame, text="Employee account created successfully", text_color=SUCCESS_COLOUR, font=("Roboto", 18))
                self.successMessage.pack()

                self.employeeList.append(firstName + " " + lastName + " - " + str(id))
                self.employeeComboBox.configure(values=self.employeeList)

                self.firstNameEntry.delete(0, "end")
                self.lastNameEntry.delete(0, "end")
                self.idEntry.delete(0, "end")
                self.pwdEntry.delete(0, "end")
                self.typeValue.set("Select Staff Type")

            else:
                self.error = ctk.CTkLabel(master=self.createAccountFrame, text="Error occured, account could not be created", text_color=ERROR_COLOUR, font=("Roboto", 18))
                self.error.pack()


        except ValueError:
            if(self.error != None):
                self.error.pack_forget()
            self.error = ctk.CTkLabel(master=self.createAccountFrame, text="Employee ID should be a number", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()


    def switchFrames(self, frame):

        self.buttonsFrame.pack_forget()

        # Unpack all the view frames
        for i in self.frames:
            i.pack_forget()
        
        # Pack the view frame switched to
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.buttonsFrame.pack(fill="both", padx=20)     

    def __employeeChooser(self, choice):

        selectedEmployee = None
    
        for employee in db.staff.find():
            if(str(employee["_id"]) == choice.split(" - ")[1]):
                selectedEmployee = employee
                self.selectedEmployeeId = employee.get("_id")
                
            
        if(selectedEmployee != None):
            self.employeeIDLabel.configure(text=("Employee ID: " + str(selectedEmployee.get("_id"))))
            self.employeeNameLabel.configure(text=("Employee Name: " + str(selectedEmployee.get("first_name")) + " " + str(selectedEmployee.get("last_name"))))
            self.employeeTypeLabel.configure(text=("Employee Type: " + str(selectedEmployee.get("type"))))
            cinema = db.cinemas.find_one({"_id": selectedEmployee.get("cinema")})
            if(cinema != None):
                self.employeeCinemaLabel.configure(text=("Employee Cinema: " + str(cinema.get("location"))))

    def __removeEmployee(self):
        
        if(self.error != None):
            self.error.pack_forget()
        
        if(self.successMessage != None):
            self.successMessage.pack_forget()
            
        selectedEmployeeSel = db.staff.find_one({"_id": self.selectedEmployeeId})
        
        if(selectedEmployeeSel == None):
            self.error = ctk.CTkLabel(master= self.viewEmployeesFrame, text="Staff member does not exist", text_color=ERROR_COLOUR, font=("Roboto", 18))
            self.error.pack()
            return 
        

        success = currentCinema.removeStaffMember(self.selectedEmployeeId)
        
        if(success):
            self.employeeList.remove(selectedEmployeeSel.get("first_name") + " " + selectedEmployeeSel.get("last_name") + " - " + str(selectedEmployeeSel.get("_id")))
            self.employeeComboBox.configure(values=self.employeeList)

            self.successMessage = ctk.CTkLabel(master=self.viewEmployeesFrame, text="Staff Removed", text_color=SUCCESS_COLOUR, font=("Roboto", 18))
            self.successMessage.pack()
        
        
        


