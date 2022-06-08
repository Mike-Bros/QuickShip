class Place:
    def __init__(self, name, address, zip):
        self.name = name
        self.address = address
        self.zip = zip
        self.seperator = "********************************************************************************"

    def print(self):
        print(self.seperator)
        print("Name: " + self.name)
        print("Address: " + self.address + ", " + str(self.zip))
        print(self.seperator)
