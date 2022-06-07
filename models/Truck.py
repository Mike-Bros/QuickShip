class Truck:
    def __init__(self):
        self.max_capacity = 16
        self.avg_speed = 18
        self.packages = []
        self.seperator = "--------------------------------------------------------------------------------"

    def load_package(self, package):
        if self.current_capacity() <= 15:
            self.packages.append(package)
            print("Added package: " + str(package.id) + " to truck. Current Capacity: " + str(self.current_capacity()))
        else:
            print("Tried to add too many packages to the truck, the below package was not added")
            package.print()

    def print(self):
        heading = "Truck Details"
        stats = "Max Capacity: " + str(self.max_capacity) \
                + " | Current Capacity: " + str(self.current_capacity()) \
                + " | Avg Speed: " + str(self.avg_speed) \

        print(self.seperator)
        print(heading)
        print(stats)
        print("Packages on Board:")
        for package in self.packages:
            package.print()
        print(self.seperator)

    def current_capacity(self):
        return len(self.packages)