from datetime import timedelta

from models.Package import Package
from models.Truck import Truck
from services.DistanceService import DistanceService
from services.PackageService import PackageService
from services.PlaceService import PlaceService
from services.RouteService import RouteService


def sort_packages():
    print("********** Truck 1 **********")
    print("Package list before sort: [", end='')
    for package in route_service.truck_1.packages:
        print(package.id, end=', ')
    print(']')

    distance_list = route_service.get_distance_list(1)
    unsorted_distance = sum(distance_list)
    print("Unsorted distance for truck: " + str(unsorted_distance))

    print()
    route_service.sort_truck_packages(1)

    print("Package list after sort: [", end='')
    for package in route_service.truck_1.packages:
        print(package.id, end=', ')
    print(']')

    distance_list = route_service.get_distance_list(1)
    print(distance_list)
    print("Unsorted total distance: " + str(unsorted_distance) + " | Sorted total distance: " + str(sum(distance_list)))

    print("********** Truck 2 **********")
    print("Package list before sort: [", end='')
    for package in route_service.truck_2.packages:
        print(package.id, end=', ')
    print(']')

    distance_list = route_service.get_distance_list(2)
    unsorted_distance = sum(distance_list)
    print("Unsorted distance for truck: " + str(unsorted_distance))

    print()
    route_service.sort_truck_packages(2)

    print("Package list after sort: [", end='')
    for package in route_service.truck_2.packages:
        print(package.id, end=', ')
    print(']')

    distance_list = route_service.get_distance_list(2)
    print(distance_list)
    print("Unsorted total distance: " + str(unsorted_distance) + " | Sorted total distance: " + str(sum(distance_list)))

    print("********** Truck 3 **********")
    print("Package list before sort: [", end='')
    for package in route_service.truck_2.packages:
        print(package.id, end=', ')
    print(']')

    distance_list = route_service.get_distance_list(2)
    unsorted_distance = sum(distance_list)
    print("Unsorted distance for truck: " + str(unsorted_distance))

    print()
    route_service.sort_truck_packages(2)

    print("Package list after sort: [", end='')
    for package in route_service.truck_2.packages:
        print(package.id, end=', ')
    print(']')

    distance_list = route_service.get_distance_list(1)
    print(distance_list)
    print("Unsorted total distance: " + str(unsorted_distance) + " | Sorted total distance: " + str(sum(distance_list)))


if __name__ == '__main__':
    route_service = RouteService()
    route_service.load_all_trucks()

    # available_packages = route_service.get_available_packages()
    # for package in available_packages:
    #     print(package.id)

    # print(route_service.get_package_by_address('177 W Price Ave').id)

    sort_packages()

    # place_service = PlaceService()
    # package_service = PackageService()
    # distance_service = DistanceService()

    # package_service.package_hash.print_table()

    # t1 = Truck()
    # for package in package_service.all_package_list:
    #     if t1.can_add_package():
    #         t1.load_package(package)
    #     else:
    #         break
    #
    # address = "410 S State St"
    # closest_place = distance_service.min_distance(address, t1.packages)
    # print()
    # print(
    #     address + " is closest to: " + closest_place.address + " with a distance of: " + str(distance_service.get_distance_between(
    #         address, closest_place.address)))

    # print(distance_service.get_distance_between('195 W Oakland Ave', '195 W Oakland Ave'))
    # print(distance_service.get_distance_between('',''))

    # for package in package_list:
    #     if package.id == 1 or package.id == 8:
    #         t1.unload_package(package)
    #
    # places_list = PlaceService().place_list
    # for place in places_list:
    #     place.print()

    # place_service = PlaceService()
    # for place in place_service.place_list:
    #     place.print()

    # package_service = PackageService()
    # package_hash = package_service.package_hash
    #
    # package_hash.print_table()

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
