from datetime import timedelta

from models.HashTable import HashTable
from models.Package import Package
from models.Truck import Truck
from services.PackageService import PackageService
from services.PlaceService import PlaceService
from services.RouteService import RouteService

if __name__ == '__main__':
    package_service = PackageService()
    package_hash = package_service.package_hash

    package_hash.print_table()

    # t1 = Truck()
    # for package in package_list:
    #     if t1.can_add_package():
    #         t1.load_package(package)
    # t1.print()
    #
    # for package in package_list:
    #     if package.id == 1 or package.id == 8:
    #         t1.unload_package(package)
    #
    # places_list = PlaceService().place_list
    # for place in places_list:
    #     place.print()

    # items = [
    #     [1, "123 Main"],
    #     [2, "1234 Circle"],
    #     [3, "321 Street"],
    #     [12, "978 Curb"],
    #     [11, "123 Court"],
    # ]
    #
    # myHash = HashTable()
    #
    # print("Adding Items...........")
    # for i in range(len(items)):
    #     myHash.insert_or_update(items[i][0], items[i][1])
    #
    # print("\nPrinting...........")
    # myHash.print_table()
    #
    # print("\nSearches...........")
    # print(myHash.search(2))
    # print(myHash.search(0))
    #
    # print("\nRemove Everything...........")
    # # myHash.remove(11)
    # for i in range(len(items)):
    #     myHash.remove(items[i][0])
    #
    # print("\nPrinting after removal...........")
    # myHash.print_table()
