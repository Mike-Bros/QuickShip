from models.PackageTable import PackageTable
from models.Package import Package
import pandas as pd


class PackageService:
    """A service class to assist ingesting package data

    """
    def __init__(self):
        self.package_hash = PackageTable()
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
        print("Finished ingesting packages")
