import copy

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

    def get_closest_package_id(self, address, packages):
        """Get the package_id of the closest package given the starting address and a list of packages that still need to be delivered

        :param address: Starting address
        :type address: str
        :param packages: Packages that still need to be delivered
        :type packages: list
        :return: The id of the closest package
        :rtype: int
        """

        min_distance = None
        closest_package_id = None

        # print("Packages to choose from: [", end='')
        # for package in packages:
        #     print(package.id, end=', ')
        # print(']')

        # find the min_distance of
        for package in packages:
            temp_distance = self.get_distance_between(package.address, address)
            if min_distance is None:
                # print("Setting first min_distance: " + str(temp_distance))
                min_distance = copy.deepcopy(temp_distance)
            if closest_package_id is None:
                # print("Setting first closest_package_id: " + str(package.id))
                closest_package_id = copy.deepcopy(package.id)

            if temp_distance < min_distance:
                # print("New closest place found. Old distance: " + str(min_distance) + " | New Distance: " + str(
                #     temp_distance))
                # closest_place Place object
                closest_package_id = copy.deepcopy(package.id)
                min_distance = copy.deepcopy(temp_distance)

        # for package in packages:
        #     if package.address != 'HUB' and package.address != address:
        #         temp_distance = self.get_distance_between(package.address, address)
        #         if min_distance is None:
        #             min_distance = temp_distance
        #         if closest_place is None:
        #             closest_place = self.get_place_by_address(package.address)
        #
        #         elif temp_distance < min_distance:
        #             print("New closest place found. Old distance: " + str(min_distance) + " | New Distance: " + str(
        #                 temp_distance))
        #             print("Old closest place: " + closest_place.address + " | New Place: " + package.address)
        #             closest_place = self.get_place_by_address(package.address)
        #             min_distance = temp_distance

        # for place in self.place_list:
        #     if place.address != 'HUB' and place.address != address:
        #         temp_distance = self.get_distance_between(place.address, address)
        #         if min_distance is None:
        #             min_distance = temp_distance
        #         if closest_place is None:
        #             closest_place = place
        #
        #         elif temp_distance < min_distance:
        #             print("New closest place found. Old distance: " + str(min_distance) + " | New Distance: " + str(
        #                 temp_distance))
        #             print("Old closest place: " + closest_place.address + " | New Place: " + place.address)
        #             closest_place = place
        #             min_distance = temp_distance

        if closest_package_id is None:
            raise Exception("Something very wrong has occurred, no closest package has been found")

        return closest_package_id
