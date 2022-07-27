from datetime import datetime, timedelta
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
        self.place_list = PlaceService().place_list
        # Save point seed, this should give best chance at timely delivers with restrictions,
        # not accounting for package #9
        # self.t1_seed = [13, 14, 15, 16, 19, 20, 1, 29, 30, 31, 34, 37, 40]
        # self.t2_seed = [3, 18, 36, 38]
        # self.t3_seed = [6, 25, 28, 32]
        self.t1_seed = [13, 14, 15, 16, 19, 20, 1, 29, 30, 31, 34, 37, 40, 2, 4, 5]
        self.t2_seed = [3, 18, 36, 38, 7, 8, 10, 11, 12, 17, 21, 22, 23, 24, 26, 27]
        self.t3_seed = [6, 25, 28, 32, 33, 35, 39]
        self.truck_1 = Truck("Truck 1")
        self.truck_2 = Truck("Truck 2")
        self.truck_3 = Truck("Truck 3")
        self.all_packages = PackageService().all_package_list
        self.loaded_packages = []

    def get_current_time(self):
        print(self.current_time.strftime("%I:%M %p"))

    def add_minutes(self, min):
        self.current_time = self.current_time + timedelta(minutes=min)

    def get_available_packages(self):
        available_packages = self.all_packages
        for package in self.loaded_packages:
            if available_packages.__contains__(package):
                available_packages.remove(package)
        return available_packages

    def get_package_by_id(self, id):
        for package in self.all_packages:
            if id == package.id:
                return package
        return None

    def load_all_trucks(self):
        # 13, 14, 15, 16, 19, 20 all need to be delivered together
        # 3, 18, 36, 38 all need to be on 2 per requirements
        # 6, 25, 28, 32 are delayed until 9:05 am
        # 9 needs a corrected address which will be received at 10:20 am

        # Helper function to load trucks with seed data from class init
        self.seed_trucks()

    def seed_trucks(self):
        if len(self.t1_seed) > 0:
            for package_id in self.t1_seed:
                self.load_truck(1, package_id)
                self.loaded_packages.append(self.get_package_by_id(package_id))
            self.t1_seed = []

        if len(self.t2_seed) > 0:
            for package_id in self.t2_seed:
                self.load_truck(2, package_id)
                self.loaded_packages.append(self.get_package_by_id(package_id))
            self.t2_seed = []

        if len(self.t3_seed) > 0:
            for package_id in self.t3_seed:
                self.load_truck(3, package_id)
                self.loaded_packages.append(self.get_package_by_id(package_id))
            self.t3_seed = []

    def load_truck(self, truck_id, package_id):
        if truck_id == 1:
            self.truck_1.load_package(self.get_package_by_id(package_id))
        if truck_id == 2:
            self.truck_2.load_package(self.get_package_by_id(package_id))
        if truck_id == 3:
            self.truck_3.load_package(self.get_package_by_id(package_id))

