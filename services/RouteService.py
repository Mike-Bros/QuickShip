import copy
from datetime import datetime, timedelta

from services.DistanceService import DistanceService
from services.PackageService import PackageService
from services.PlaceService import PlaceService
from models.Truck import Truck


class RouteService:
    def __init__(self):
        # time is measured in minutes, find hours by /60
        # start time 8:00 AM - 8*60 = 480 minutes
        self.start_time = datetime(2022, 1, 1, 8, 0)
        self.current_time = self.start_time
        self.time_increment = 2
        self.distance_service = DistanceService()
        self.place_list = self.distance_service.place_list
        self.t1_trip_1_seed = [13, 14, 15, 16, 19, 20, 1, 29, 34, 7]
        self.t2_trip_1_seed = [30, 37, 40, 31]
        self.t1_trip_2_seed = [8, 9, 10, 11, 12, 17, 21, 22, 23, 24]
        self.t2_trip_2_seed = [25, 6]
        self.t1_trip_3_seed = [26, 27, 28, 32]
        self.t2_trip_3_seed = [3, 18, 36, 38, 5, 2, 4, 33, 35, 39]
        self.truck_1 = Truck("Truck 1")
        self.truck_2 = Truck("Truck 2")
        self.all_packages = PackageService().all_package_list
        self.loaded_packages = []

    def print_current_time(self):
        print(self.current_time.strftime("%I:%M %p"))

    def add_minutes(self, min):
        self.current_time = self.current_time + timedelta(minutes=min)

    def get_available_packages(self):
        available_packages = self.all_packages.copy()
        for package in self.loaded_packages:
            if available_packages.__contains__(package):
                available_packages.remove(package)
        return available_packages

    def get_package_by_id(self, id):
        for package in self.all_packages:
            if id == package.id:
                return package
        return None

    def get_package_by_address(self, address):
        """

        :param address:
        :type address: str
        :return: The first package associated with given address
        :rtype: models.Package
        """
        for package in self.all_packages:
            if address == package.address:
                return package
        return None

    def load_trip(self, trip_id):
        seed_1 = None
        seed_2 = None
        if trip_id == 1:
            seed_1 = self.t1_trip_1_seed
            seed_2 = self.t2_trip_1_seed
        if trip_id == 2:
            seed_1 = self.t1_trip_2_seed
            seed_2 = self.t2_trip_2_seed
        if trip_id == 3:
            seed_1 = self.t1_trip_3_seed
            seed_2 = self.t2_trip_3_seed

        if seed_1 is None or seed_2 is None:
            raise Exception("Unknown trip_id given to load_trip in RouteService")

        if len(seed_1) > 0:
            for package_id in seed_1:
                self.load_truck(1, package_id)
                self.loaded_packages.append(self.get_package_by_id(package_id))
            self.t1_seed = []

        if len(seed_2) > 0:
            for package_id in seed_2:
                self.load_truck(2, package_id)
                self.loaded_packages.append(self.get_package_by_id(package_id))
            self.t2_seed = []

    def load_truck(self, truck_id, package_id):
        if truck_id == 1:
            self.truck_1.load_package(self.get_package_by_id(package_id))
        if truck_id == 2:
            self.truck_2.load_package(self.get_package_by_id(package_id))

    def optimize_truck_packages_greedy(self, truck_name):
        print("************************************************************")
        print("Optimizing for: " + getattr(self, truck_name).name)

        self.print_optimizing_route_info(getattr(self, truck_name).packages, "Before Optimize")
        self.distance_service.greedy_shortest_path(getattr(self, truck_name))
        self.print_optimizing_route_info(getattr(self, truck_name).packages, "After Optimize")

    def print_optimizing_route_info(self, package_list, label="", package_attribute="id"):
        print(label + " (List of the Package." + package_attribute + ")")
        print("[", end='')
        count = 0
        for package in package_list:
            count = count + 1
            if count == len(package_list):
                total_distance = self.distance_service.get_total_route_weight(package_list)
                total_distance = total_distance.__round__(2)
                minutes = (total_distance / 18) * 60
                minutes = minutes.__round__(2)
                print(str(getattr(package, package_attribute)) + "] - Distance: " + str(
                    total_distance) + " | Minutes: " + str(minutes))
            else:
                print(getattr(package, package_attribute), end=', ')

    def start_route(self, truck_name, start_time=datetime(2022, 1, 1, 8, 0)):
        print("************************************************************")
        print("Starting route for: " + getattr(self, truck_name).name)
        truck = getattr(self, truck_name)
        self.current_time = start_time

        full_route = [["Start", "HUB"]]
        # Update packages to be 'en-route' and build path
        for package in truck.packages:
            package.delivery_status = "En-Route"
            full_route.append([package.id, package.address])
        full_route.append(["End", "HUB"])

        print("Full Planned Route: ", end='')
        print(full_route)

        for i in range(0, len(full_route) - 1):
            delivery_distance = self.distance_service.get_distance_between(full_route[i][1], full_route[i + 1][1])
            # print(full_route[i][1] + " - " + full_route[i + 1][1] + "\t| " + str(delivery_distance))
            minutes_taken = (delivery_distance / 18) * 60
            minutes_taken = minutes_taken.__round__(2)
            self.add_minutes(minutes_taken)
            if full_route[i + 1][0] != 'End':
                truck.deliver_package(full_route[i + 1][0], self.current_time)

        print("[", end='')
        for package in truck.delivered_packages:
            if package.deadline != "EOD":
                package.deadline = package.deadline.replace(" ", "")
                package.deadline = package.deadline.replace(":", "")
                package.deadline = package.deadline.replace("AM", "")

                if len(package.deadline) == 3:
                    hour = package.deadline[0:1]
                    min = package.deadline[1:3]
                else:
                    hour = package.deadline[0:2]
                    min = package.deadline[2:4]
                deadline = datetime(2022, 1, 1, int(hour), int(min))
                print("(" + str(package.id) + ", " + str(package.delivery_time < deadline), end='), ')
            else:
                print("(" + str(package.id) + ", True", end='), ')
        print("]")

        getattr(self, truck_name).last_time = self.current_time


