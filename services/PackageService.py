from models.PackageTable import PackageTable
from models.Package import Package
import pandas as pd


class PackageService:
    """A service class to assist ingesting package data

    """

    def __init__(self):
        self.package_hash = PackageTable()
        self.all_package_list = []
        self.ingest_packages()

    def ingest_packages(self):
        """A function that runs during class init to read in Package data from packages.csv in root.

        """
        print("Ingesting packages...")
        df = pd.read_csv('./packages.csv', keep_default_na="")
        for index, row in df.iterrows():
            new_package = Package(row['ID'], row['Address'], row['City'], row['State'], row['Zip'], row['Deadline'],
                                  row['Mass'], row['Notes'])
            self.package_hash.insert_or_update(new_package.id, new_package)
            self.all_package_list.append(new_package)
        print("Finished ingesting packages")

    def refresh_package_table(self, packages):
        """ Given a list of packages this will refresh the service's package table and list

        :param packages: A list of packages
        :type packages: list
        """
        # Reset the packages
        self.package_hash = PackageTable()
        self.all_package_list = []

        for package in packages:
            self.package_hash.insert_or_update(package.id, package)
            self.all_package_list.append(package)

    def get_package_by_id(self, package_id):
        """Efficiently get package object by given package ID using table lookup

        :param package_id: ID of the package to get
        :type package_id: int
        :return: Package with the given package_id
        :rtype: models.Package
        """
        found_package = self.package_hash.search(package_id)
        if found_package is None:
            raise Exception("Package: " + str(package_id) + " was not found")
        return found_package

    def get_packages_in_range(self, start_time, end_time):
        in_range = []
        for package in self.all_package_list:
            if start_time <= package.delivery_time <= end_time:
                in_range.append(package)
        return in_range

    def print_packages_list(self, packages):

        print('[', end='')
        count = 0
        for package in packages:
            if count < len(packages) - 1:
                print(package.id, end=', ')
                count += 1
            else:
                print(package.id, end=']\n')

    def print_status_check(self, start_time, end_time):
        packages_on_truck_1_en_route = []
        packages_on_truck_1_delivered = []
        packages_on_truck_2_en_route = []
        packages_on_truck_2_delivered = []

        for package in self.all_package_list:
            if start_time <= package.en_route_time <= end_time:
                if package.delivery_truck == "truck_1":
                    packages_on_truck_1_en_route.append(package)
                if package.delivery_truck == "truck_2":
                    packages_on_truck_2_en_route.append(package)
            if start_time <= package.delivery_time <= end_time:
                if package.delivery_truck == "truck_1":
                    packages_on_truck_1_delivered.append(package)
                if package.delivery_truck == "truck_2":
                    packages_on_truck_2_delivered.append(package)

        print("Packages En-Route on Truck 1 during given range...")
        self.print_packages_list(packages_on_truck_1_en_route)
        print("Packages En-Route on Truck 2 during given range...")
        self.print_packages_list(packages_on_truck_2_en_route)

        print("Packages Delivered on Truck 1 during given range...")
        self.print_packages_list(packages_on_truck_1_delivered)
        print("Packages Delivered on Truck 2 during given range...")
        self.print_packages_list(packages_on_truck_2_delivered)
