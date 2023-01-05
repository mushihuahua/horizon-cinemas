import customtkinter as ctk
from werkzeug.security import generate_password_hash, check_password_hash


ERROR_COLOUR="#e23636"
SUCCESS_COLOUR="#66bb6a"

class AdminFrame():
    def __init__(self, container, loggedInUser):

        self.loggedInUser = loggedInUser

        self.frames = []
        self.error = None
        self.successMessage = None 

        self.frame = ctk.CTkFrame(master=container, corner_radius=20)

        self.inFrame = ctk.CTkFrame(master=self.frame, corner_radius=20)
        self.reportsFrame = ctk.CTkFrame(master=self.frame, corner_radius=20)
        self.viewListingsFrame = ctk.CTkFrame(master=self.frame, corner_radius=20)

        self.frames.append(self.inFrame)
        self.frames.append(self.reportsFrame)

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
                            text="Admin View",
                            font=("Roboto", 48))

        self.generateReportButton = ctk.CTkButton(master=self.buttonsFrame, 
                                    text="Reports", 
                                    width=250,
                                    height=75,
                                    font=("", 18, "bold"), 
                                    corner_radius=7,
                                    fg_color="#9f54fb",
                                    hover_color="#a722fa",
                                    command=lambda: self.switchFrames(self.reportsFrame))


        

    

        self.createLabel = ctk.CTkLabel(master=self.reportsFrame, text="Create Report", font=("Roboto", 32))
        self.createLabel.place(relx=.5, rely=.2, anchor="center")

        








        '''
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
        '''
        self.inFrame.pack(pady=20, padx=20, fill="both", expand=True)
        self.text.place(relx=.5, rely=.2, anchor="center")
        self.employeeLabel.place(relx=.5, rely=.3, anchor="center")
        self.cinemaLabel.place(relx=.5, rely=.35, anchor="center")

        self.buttonsFrame.pack(fill="both", padx=20)
        self.generateReportButton.pack(side="left", padx=(15, 15))
        #self.viewEmployeesButton.pack(side="left", padx=15)
        #self.createEmployeeAccount.pack(side="left", padx=15)

        '''

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
                success = self.loggedInUser.createNewEmployee(firstName, lastName, id, generate_password_hash(pwd), empType)

            if(success):
                self.successMessage = ctk.CTkLabel(master=self.createAccountFrame, text="Employee account created successfully", text_color=SUCCESS_COLOUR, font=("Roboto", 18))
                self.successMessage.pack()

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
            '''
        









    def switchFrames(self, frame):

        self.buttonsFrame.pack_forget()

        # Unpack all the view frames
        for i in self.frames:
            i.pack_forget()
        
        # Pack the view frame switched to
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.buttonsFrame.pack(fill="both", padx=20)


        self.test = ctk.CTkLabel(master=self.frame, text="Admin")
        self.test.pack()