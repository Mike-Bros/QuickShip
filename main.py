from models.Package import Package
from models.Truck import Truck
from services import PackageService

if __name__ == '__main__':
    package_list = PackageService.ingest_packages()

    t1 = Truck()

    for package in package_list:
        if t1.can_add_package():
            t1.load_package(package)

    t1.print()