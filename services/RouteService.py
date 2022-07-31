import copy
from datetime import datetime, timedelta

from services.DistanceService import DistanceService
from services.PackageService import PackageService
from models.Truck import Truck


class RouteService:
    def __init__(self):
        # time is measured in minutes, find hours by /60
        # start time 8:00 AM - 8*60 = 480 minutes
        self.start_time = datetime(2022, 1, 1, 8, 0)
        self.eod = datetime(2022, 1, 1, 17, 0) # 5:00 PM
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
        self.package_service = PackageService()
        self.all_packages = self.package_service.all_package_list
        self.loaded_packages = []

    def print_current_time(self):
        """Helper function to print the human-readable current time

        """
        print(self.current_time.strftime("%I:%M %p"))

    def add_minutes(self, min):
        """Add minutes to the service's current time

        :param min: Minutes to add
        :type min: int
        """
        self.current_time = self.current_time + timedelta(minutes=min)

    def load_trip(self, trip_id):
        """Loads the service's seed data into the service's trucks for the specified trip_id

        :param trip_id: Trip to seed trucks with
        :type trip_id: int
        """
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
                self.loaded_packages.append(self.package_service.get_package_by_id(package_id))
            self.t1_seed = []

        if len(seed_2) > 0:
            for package_id in seed_2:
                self.load_truck(2, package_id)
                self.loaded_packages.append(self.package_service.get_package_by_id(package_id))
            self.t2_seed = []

    def load_truck(self, truck_id, package_id):
        """Load truck with package

        :param truck_id: Truck to load
        :type truck_id: int
        :param package_id: Package to load
        :type package_id: int
        """
        if truck_id == 1:
            self.truck_1.load_package(self.package_service.get_package_by_id(package_id))
        if truck_id == 2:
            self.truck_2.load_package(self.package_service.get_package_by_id(package_id))

    def optimize_truck_packages_greedy(self, truck_name):
        """Optimizes truck package_list using the DistanceService's greedy_shortest_path function

        :param truck_name: Name of truck attribute to optimize (IE: "truck_1")
        :type truck_name: str
        """
        print("************************************************************")
        print("Optimizing for: " + getattr(self, truck_name).name)

        self.print_optimizing_route_info(getattr(self, truck_name).packages, "Before Optimize")
        self.distance_service.greedy_shortest_path(getattr(self, truck_name))
        self.print_optimizing_route_info(getattr(self, truck_name).packages, "After Optimize")

    def print_optimizing_route_info(self, package_list, label="", package_attribute="id"):
        """Helper function to print helpful route info, main purpose to visualize optimization step

        :param package_list:
        :type package_list: list
        :param label:
        :type label: str
        :param package_attribute:
        :type package_attribute: str
        """
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
        """Starts a route for the given truck, simulates and updates delivery of truck's packages

        :param truck_name: Name of truck attribute to optimize (IE: "truck_1")
        :type truck_name: str
        :param start_time: Time the route is supposed to start, be default 1/1/22 @8:00AM
        :type start_time: datetime
        """
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
                package_id = full_route[i + 1][0]
                package_deadline = self.get_package_deadline_datetime(self.package_service.get_package_by_id(package_id))
                truck.deliver_package(package_id, package_deadline, self.current_time)

        print("[", end='')
        for package in truck.delivered_packages:
            deadline = self.get_package_deadline_datetime(package)
            print("(" + str(package.id) + ", " + str(package.delivery_time < deadline), end='), ')
        print("]")

        getattr(self, truck_name).last_time = self.current_time

    def get_package_deadline_datetime(self, package):
        """Helper function to get the datetime object of the given package's delivery deadline

        :param package:
        :type package: models.Package
        :return:
        :rtype: datetime
        """
        package_deadline_copy = copy.deepcopy(package.deadline)
        if package.deadline != "EOD":
            package_deadline_copy = package_deadline_copy.replace(" ", "")
            package_deadline_copy = package_deadline_copy.replace(":", "")
            package_deadline_copy = package_deadline_copy.replace("AM", "")

            if len(package_deadline_copy) == 3:
                hour = package_deadline_copy[0:1]
                min = package_deadline_copy[1:3]
            else:
                hour = package_deadline_copy[0:2]
                min = package_deadline_copy[2:4]
            return datetime(2022, 1, 1, int(hour), int(min))
        else:
            # EOD = 5PM
            return self.eod
