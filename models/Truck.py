class Truck:
    def __init__(self):
        self.max_capacity = 16
        self.avg_speed = 18
        self.packages = []
        self.seperator = "--------------------------------------------------------------------------------"

    def load_package(self, package):
        if self.can_add_package():
            self.packages.append(package)
            print("Loaded package #" + str(package.id) + " | Current Capacity: " + str(self.current_capacity()))
        else:
            print("Tried to add too many packages to the truck, the below package was not added")
            package.print()

    def unload_package(self, package):
        if self.current_capacity() > 0:
            self.packages.remove(package)
            print("Package #" + str(package.id) + " was unloaded")

    def print(self):
        heading = "Truck Details"
        stats = "Max Capacity: " + str(self.max_capacity) \
                + " | Current Capacity: " + str(self.current_capacity()) \
                + " | Avg Speed: " + str(self.avg_speed)

        print(self.seperator)
        print(heading)
        print(stats)
        print("Packages on Board:")
        for package in self.packages:
            package.print()
        print(self.seperator)

    def current_capacity(self):
        return len(self.packages)

    def can_add_package(self):
        if self.current_capacity() <= 15:
            return True
        else:
            return False
