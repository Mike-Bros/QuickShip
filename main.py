from models.Package import Package
from models.Truck import Truck
from services.PackageService import PackageService
from services.PlaceService import PlaceService

if __name__ == '__main__':
    # package_list = PackageService().package_list
    #
    # t1 = Truck()
    # for package in package_list:
    #     if t1.can_add_package():
    #         t1.load_package(package)
    # t1.print()

    places_list = PlaceService().place_list
    for place in places_list:
        place.print()