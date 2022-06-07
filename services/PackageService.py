from models.Package import Package
import pandas as pd


def ingest_packages():
    df = pd.read_csv('./packages.csv', keep_default_na="")
    package_list = []
    for index, row in df.iterrows():
        new_package = Package(row['ID'], row['Address'], row['City'], row['State'], row['Zip'], row['Deadline'],
                              row['Mass'], row['Notes'])
        package_list.append(new_package)
    return package_list
