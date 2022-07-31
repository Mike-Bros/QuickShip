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
        # Reset the packages
        self.package_hash = PackageTable()
        self.all_package_list = []

        for package in packages:
            self.package_hash.insert_or_update(package.id, package)
            self.all_package_list.append(package)

    def get_package_by_id(self, package_id):
        found_package = self.package_hash.search(package_id)
        if found_package is None:
            raise Exception("Package: " + str(package_id) + " was not found")
        return found_package
