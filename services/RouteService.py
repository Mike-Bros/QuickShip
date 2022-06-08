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
        self.package_list = PackageService().package_list
        self.place_list = PlaceService().place_list
        self.truck_1 = Truck()
        self.truck_2 = Truck()
        self.truck_3 = Truck()

    def get_current_time(self):
        print(self.current_time.strftime("%I:%M %p"))

    def add_minutes(self, min):
        self.current_time = self.current_time + timedelta(minutes=min)

    def start_day(self):
        self.organize_route()

    def organize_route(self):
        for package in self.package_list:
            pass
