from models.Package import Package
import pandas as pd


class PackageService:
    def __init__(self):
        self.package_list = []
        self.ingest_packages()

    def ingest_packages(self):
        print("Ingesting packages...")
        df = pd.read_csv('./packages.csv', keep_default_na="")
        for index, row in df.iterrows():
            new_package = Package(row['ID'], row['Address'], row['City'], row['State'], row['Zip'], row['Deadline'],
                                  row['Mass'], row['Notes'])
            self.package_list.append(new_package)
        print("Finished ingesting packages")