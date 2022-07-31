class Truck:
    """A model of a truck to facilitate packaging simulation per project requirements

    """

    def __init__(self, name):
        self.name = name
        self.max_capacity = 16
        self.avg_speed = 18
        self.packages = []
        self.delivered_packages = []
        self.starting_address = "HUB"
        self.last_time = None
        self.seperator = "--------------------------------------------------------------------------------"

    def load_package(self, package):
        """Load a package into the truck

        Does not allow for packages to go over the preset truck capacity

        :param package:
        :type package: models.Package
        """
        if self.can_add_package():
            self.packages.append(package)
            print(self.name + " Loaded package #" + str(package.id) + " | Current Capacity: " + str(
                self.current_capacity()) + "/" + str(self.max_capacity))
        else:
            print("Tried to add too many packages to the truck, the below package was not added")
            package.print()

    def unload_package(self, package):
        """Unload a package off of the truck

        :param package:
        :type package: models.Package
        """
        if self.current_capacity() > 0:
            self.packages.remove(package)
            # print("Package #" + str(package.id) + " was unloaded")

    def deliver_package(self, package_id, delivery_time):
        """Deliver a package, unloads package, adds package to the delivered packages, set package delivery time and status

        :param delivery_time: Time the package was delivered
        :type delivery_time:
        :param package:
        :type package: models.Package
        """
        package = None
        for p in self.packages:
            if p.id == package_id:
                package = p

        if package is None:
            raise Exception("Given package to deliver is not on the truck!")

        self.unload_package(package)
        self.delivered_packages.append(package)
        package.delivery_status = "Delivered"
        package.delivery_time = delivery_time


    def print(self):
        """Helper printing function for the truck model

        """
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

    def print_packages(self):
        for package in self.packages:
            print(package.id, end=', ')
        print()

    def current_capacity(self):
        """Helper function to get the current number of packages in the truck

        :return: Number of packages loaded in the truck
        :rtype: int
        """
        return len(self.packages)

    def can_add_package(self):
        """Helper function to check if more packages can be added or if the truck is at max capacity

        :return:
        :rtype: bool
        """
        if self.current_capacity() <= 15:
            return True
        else:
            return False