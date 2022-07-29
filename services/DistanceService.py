import copy
import itertools

import pandas as pd

from services.PlaceService import PlaceService


class DistanceService:
    """A service class to assist with retrieving distance values

    """

    def __init__(self):
        self.distance_list = []
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
        distance_list = []

        for package in package_list:
            if last_package_address is None:
                last_package_address = copy.deepcopy(package.address)
            else:
                distance_list.append(self.get_distance_between(package.address, last_package_address))

        return sum(distance_list)

    def brute_shortest_path(self, package_list):
        current_cost = float('inf')
        current_best_path = []

        current_best_path_first_half = []
        package_list_first_half = []
        current_best_path_second_half = []
        package_list_second_half = []

        if len(package_list) >= 9:
            count = 0
            for package in package_list:
                count = count + 1
                if count <= 8:
                    package_list_first_half.append(package)
                else:
                    package_list_second_half.append(package)
            count = 0
            for package_list_iteration in itertools.permutations(package_list_first_half):
                count = count + 1
                # print("first half" + str(count))
                iteration_cost = self.get_total_distance(package_list_iteration)
                if iteration_cost < current_cost:
                    current_best_path_first_half = package_list_iteration
                    current_cost = iteration_cost

            count = 0
            current_cost = float('inf')
            for package_list_iteration in itertools.permutations(package_list_second_half):
                count = count + 1
                # print("second half" + str(count))
                iteration_cost = self.get_total_distance(package_list_iteration)
                if iteration_cost < current_cost:
                    current_best_path_second_half = package_list_iteration
                    current_cost = iteration_cost

            for package in current_best_path_first_half:
                current_best_path.append(package)

            for package in current_best_path_second_half:
                current_best_path.append(package)

        else:
            count = 0
            for package_list_iteration in itertools.permutations(package_list):
                count = count + 1
                # print(count)
                iteration_cost = self.get_total_distance(package_list_iteration)
                if iteration_cost < current_cost:
                    current_best_path = package_list_iteration
                    current_cost = iteration_cost

                # print("[", end='')
                # count = 0
                # for package in package_list_iteration:
                #     count = count + 1
                #     if count == len(package_list_iteration):
                #         print(str(package.id) + "] - Itter Cost: " + str(iteration_cost))
                #     else:
                #         print(package.id, end=', ')

        return current_best_path

    def tsp_shortest_path(self, package_list):
        current_cost = float('inf')
        current_best_path = []

        count = 0
        for package_list_iteration in itertools.permutations(package_list):
            count = count + 1
            # print(count)
            iteration_cost = self.get_total_distance(package_list_iteration)
            if iteration_cost < current_cost:
                current_best_path = package_list_iteration
                current_cost = iteration_cost

            # print("[", end='')
            # count = 0
            # for package in package_list_iteration:
            #     count = count + 1
            #     if count == len(package_list_iteration):
            #         print(str(package.id) + "] - Itter Cost: " + str(iteration_cost))
            #     else:
            #         print(package.id, end=', ')

        return current_best_path

