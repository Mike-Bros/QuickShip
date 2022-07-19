class Package:
    """A model of a package to better store and retrieve package attributes

    """
    def __init__(self, id, address, city, state, zip, deadline, mass, notes=""):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.notes = notes
        self.seperator = "********************************************************************************"

    def print(self):
        """Helper printing function for the package model

        """
        heading = "Package Details"
        stats = "ID: " + str(self.id) + " | Mass: " + str(self.mass) + " | Deadline: " + self.deadline
        full_address = "Address: " + self.address + " " + self.city + " " + self.state + ", " + str(self.zip)
        notes = "Special Notes: " + self.notes

        print(self.seperator)
        print(heading)
        print(stats)
        print(full_address)
        print(notes)
        print(self.seperator)