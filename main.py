from datetime import timedelta

from models.Package import Package
from models.Truck import Truck
from services.PackageService import PackageService
from services.PlaceService import PlaceService
from services.RouteService import RouteService

if __name__ == '__main__':
    package_list = PackageService().package_list

    t1 = Truck()
    for package in package_list:
        if t1.can_add_package():
            t1.load_package(package)
    t1.print()

    for package in package_list:
        if package.id == 1 or package.id == 8:
            t1.unload_package(package)

    # places_list = PlaceService().place_list
    # for place in places_list:
    #     place.print()