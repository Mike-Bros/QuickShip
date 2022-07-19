class Place:
    """A model of a place to better store and retrieve place attributes

    """
    def __init__(self, id, name, address, zip):
        self.id = id
        self.name = name
        self.address = address
        self.zip = zip
        self.seperator = "********************************************************************************"

    def print(self):
        """Helper printing function for the place model

        """
        print(self.seperator)
        print("ID: " + str(self.id))
        print("Name: " + self.name)
        print("Address: " + self.address + ", " + str(self.zip))
        print(self.seperator)
