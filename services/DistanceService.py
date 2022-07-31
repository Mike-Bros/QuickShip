import copy
import itertools

import pandas as pd

from services.PlaceService import PlaceService


class DistanceService:
    """A service class to assist with retrieving distance values

    """

    def __init__(self):
        self.distance_list = []
        self.vertices_added = []
        self.place_list = PlaceService().place_list
        self.ingest_distances()

    def ingest_distances(self):
        """A function that runs during class init to read in Distance data from distances.csv in root.

        """
        print("Ingesting Distances...")
        df = pd.read_csv('./distances.csv', keep_default_na="")
        for index, row in df.iterrows():
            curr_address_distances = []
            for place in self.place_list:
                curr_address_distances.append(row[place.address])
            self.distance_list.append(curr_address_distances)
        print("Finished ingesting Distances")

    def get_place_by_address(self, address):
        for place in self.place_list:
            if place.address == address:
                return place
        return None

    def get_distance_between(self, address_a, address_b):
        """Get Distance Between Addresses

        Given address a & b returns the distance in miles as a float.

        :param address_a:
        :type address_a: str
        :param address_b:
        :type address_b: str
        :return: The distance between address a & b
        :rtype: float
        """
        place_a_index = None
        place_b_index = None

        for place in self.place_list:
            if address_a == place.address:
                place_a_index = place.id - 1
                break

        for place in self.place_list:
            if address_b == place.address:
                place_b_index = place.id - 1
                break

        if place_a_index is None:
            raise Exception('Given address A is unknown')

        if place_b_index is None:
            raise Exception('Given address B is unknown')

        distance_value = self.distance_list[place_a_index][place_b_index]
        if distance_value == '':
            distance_value = self.distance_list[place_b_index][place_a_index]

        return float(distance_value)

    def get_total_distance(self, package_list):
        last_package_address = None
        distance_list = [self.get_distance_between("HUB", package_list[0].address)]

        for package in package_list:
            if last_package_address is None:
                last_package_address = copy.deepcopy(package.address)
            else:
                distance_list.append(self.get_distance_between(package.address, last_package_address))
        distance_list.append(self.get_distance_between("HUB", package_list[-1].address))
        return sum(distance_list)

    def greedy_shortest_path(self, truck):
        cur_route = copy.deepcopy(truck.packages)

        close_package_a = min(cur_route, key=lambda p: self.get_distance_between("HUB", p.address))
        cur_route.remove(close_package_a)
        close_package_b = min(cur_route, key=lambda p: self.get_distance_between("HUB", p.address))
        cur_route.remove(close_package_b)

        # If the package list is any longer than 9 there are too many permutations to calculate quickly
        # Instead split the list in half and find the optimized permutation of each half
        # Then when the optimized halves are put together only the connection between the end of the first half and
        # start of the second half is not accounted for and may be non-optimal
        if len(cur_route) >= 9:
            mid_index = int(len(cur_route) / 2)
            half_a = cur_route[:mid_index]
            half_b = cur_route[mid_index:]
            cur_route_a = []
            cur_route_b = []

            # for half_a iteration add close_package_a to beginning before checking route weight
            for route_perm in itertools.permutations(half_a):
                new_route = [close_package_a]
                for package in route_perm:
                    new_route.append(package)
                if self.get_total_route_weight(new_route) < self.get_total_route_weight(cur_route):
                    cur_route_a = new_route

            # Get end of cur_route_a and find close package in half_b, this will be the first package in half b route
            # This is to get an approximately okay distance between the start and finish of the 2 optimized halves
            half_a_end = cur_route_a[-1]
            start_of_half_b = min(half_b, key=lambda p: self.get_distance_between(half_a_end.address, p.address))
            half_b.remove(start_of_half_b)

            # for half_b iteration add close_package_b to beginning before checking route weight
            for route_perm in itertools.permutations(half_b):
                new_route = [start_of_half_b]
                for package in route_perm:
                    new_route.append(package)
                new_route.append(close_package_b)
                if self.get_total_route_weight(new_route) < self.get_total_route_weight(cur_route):
                    cur_route_b = new_route

            if not cur_route_a or not cur_route_b:
                raise Exception("In optimizing split route, either cur_route_a or cur_route_b was never set")
            truck.packages = cur_route_a + cur_route_b

        else:
            for route_perm in itertools.permutations(cur_route):
                # for each iteration add close_package_a to beginning and close_package_b to end
                # before checking route weight
                new_route = [close_package_a]
                for package in route_perm:
                    new_route.append(package)
                new_route.append(close_package_b)
                if self.get_total_route_weight(new_route) < self.get_total_route_weight(cur_route):
                    cur_route = new_route

            truck.packages = cur_route

    def get_total_route_weight(self, route, toggle_half_mode=''):
        complete_route = None
        if toggle_half_mode == '':
            # Create complete route list of addresses including start and goal which is always HUB
            complete_route = ["HUB"]
            for package in route:
                complete_route.append(package.address)
            complete_route.append("HUB")
        if toggle_half_mode == 'a':
            # Create first half route list of addresses including start which is always HUB
            complete_route = ["HUB"]
            for package in route:
                complete_route.append(package.address)
        if toggle_half_mode == 'b':
            # Create second half route list of addresses including end which is always HUB
            complete_route = []
            for package in route:
                complete_route.append(package.address)
            complete_route.append("HUB")

        if complete_route is None:
            raise Exception("Value for toggle_half_mode is not known, should either be '', 'a', or 'b'")

        # Calculate weight by computing distance between each index
        weight = 0
        for i in range(0, len(complete_route) - 1):
            weight = weight + self.get_distance_between(complete_route[i], complete_route[i + 1])
        return weight
