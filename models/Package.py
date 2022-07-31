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
        self.delivery_status = "Not Delivered"
        self.delivery_time = None
        self.seperator = "********************************************************************************"

    def print_verbose(self):
        """Helper function for printing representation of package with all package attributes

        """
        heading = "Package Details"
        stats = "ID: " + str(self.id) + "\t| Mass: " + str(self.mass) + "\t| Deadline: " + self.deadline + "\t| Delivery Time: "
        if self.delivery_time is not None:
            stats = stats + self.delivery_time.strftime("%I:%M %p")
        else:
            stats = stats + str(self.delivery_time)
        status = "Delivery Status: " + str(self.delivery_status)
        full_address = "Address: " + self.address + " " + self.city + " " + self.state + ", " + str(self.zip)
        notes = "Special Notes: " + self.notes

        print(self.seperator)
        print(heading)
        print(stats)
        print(status)
        print(full_address)
        print(notes)
        print(self.seperator)

    def print(self):
        """Helper printing function for the package model

        """
        heading = "Package ID: " + str(self.id) + "\t| Status: " + str(self.delivery_status)
        stats = "Deadline: " + self.deadline + "\t| Delivered: "
        if self.delivery_time is not None:
            stats = stats + self.delivery_time.strftime("%I:%M %p")
        else:
            stats = stats + str(self.delivery_time)

        print(self.seperator)
        print(heading)
        print(stats)
        print(self.seperator)