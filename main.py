class Staff:
    def __init__(self, employeeID, passwordHash, fullName, cinema, firstName, lastName):
        self.ID = employeeID
        self.passwordHash = passwordHash
        self.cinema = cinema
        self.firstName = firstName
        self.lastName = lastName
        fullName = self.firstName +' '+ self.lastName
        self.fullName = fullName
        
    def get_passwordHash(self):
        return self.passwordHash

    def set_passwordHash(self, passwordHash):
        self.passwordHash = passwordHash
    
    def changePassword(self, newPass):
        self.passwordHash = newPass
    
    def __str__(self):
        return f"{self.fullName} {self.passwordHash}"

class BookingStaff: 
    def __init__(self, employeeID, passwordHash, fullName, cinema, firstName, lastName):
        super().__init__(employeeID, passwordHash, fullName, cinema, firstName, lastName)
        self.ID = employeeID
        self.passwordHash = passwordHash
        self.cinema = cinema
        self.firstName = firstName
        self.lastName = lastName
        fullName = self.firstName +' '+ self.lastName
        self.fullName = fullName

class Manager: 
    def __init__(self, employeeID, passwordHash, fullName, cinema, firstName, lastName):
        super().__init__(employeeID, passwordHash, fullName, cinema, firstName, lastName)
        self.ID = employeeID
        self.passwordHash = passwordHash
        self.cinema = cinema
        self.firstName = firstName
        self.lastName = lastName
        fullName = self.firstName +' '+ self.lastName
        self.fullName = fullName
    
class Admin: 
    def __init__(self, employeeID, passwordHash, fullName, cinema, firstName, lastName, report):
        super().__init__(employeeID, passwordHash, fullName, cinema, firstName, lastName)
        self.ID = employeeID
        self.passwordHash = passwordHash
        self.cinema = cinema
        self.firstName = firstName
        self.lastName = lastName
        fullName = self.firstName + ' ' + self.lastName
        self.fullName = fullName
        self.__report = report 
    
    def generateReport():
        pass

class Report: 
    def __init__(self, numberOfListingBookings, totalMonthlyRevenue, topFilm, staffBookings):
        self.__numberOfListingBookings = numberOfListingBookings
        self.__totalMonthlyRevenue = totalMonthlyRevenue
        self.__topFilm = topFilm
        self.__staffBookings = staffBookings
    

    def displayReport(self):
        pass

       

test = Staff(1, "hi", "Steve Bannon", "test", "Steve", "Bannon")
print(test)
newPassword = "hello"
test.changePassword("hello")
print(test)

        




        


