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
        self.delivery_truck = None
        self.delivery_status = "Not Delivered"
        self.en_route_time = None
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
        status = "Package Left Hub: " + self.en_route_time.strftime("%I:%M %p") + "\t| Delivery Status: " + str(self.delivery_status) + "\t| Deliver Truck: " + self.delivery_truck
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
        heading = "Package ID: " + str(self.id) + "\t| Status: " + str(self.delivery_status) + "\t| Delivery Truck: " + self.delivery_truck
        stats = "Deadline: " + self.deadline + "\t| Package Left Hub: " + self.en_route_time.strftime("%I:%M %p") + "\t| Delivered: "
        if self.delivery_time is not None:
            stats = stats + self.delivery_time.strftime("%I:%M %p")
        else:
            stats = stats + str(self.delivery_time)

        print(self.seperator)
        print(heading)
        print(stats)
        print(self.seperator)