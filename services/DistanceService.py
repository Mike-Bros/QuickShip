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
        print("Ingesting packages...")
        df = pd.read_csv('./distances.csv', keep_default_na="")
        for index, row in df.iterrows():
            curr_address_distances = []
            for place in self.place_list:
                curr_address_distances.append(row[place.address])
            self.distance_list.append(curr_address_distances)
        print("Finished ingesting packages")

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
                place_a_index = place.id
            if address_b == place.address:
                place_b_index = place.id
        if place_a_index is None:
            raise Exception('Given address A is unknown')
        if place_b_index is None:
            raise Exception('Given address B is unknown')

        distance_value = self.distance_list[place_a_index][place_b_index]
        if distance_value == '':
            distance_value = self.distance_list[place_b_index][place_a_index]

        return float(distance_value)

    def min_distance(self, address, packages):
        """Get the minimum distance to travel given the starting address and packages that still need to be delivered

        :param address: Starting address
        :type address: str
        :param packages: Packages that still need to be delivered
        :type packages: list
        :return: The closest place to address
        :rtype: models.Place
        """

        min_distance = None
        closest_place = None
        for place in self.place_list:
            if place.address != 'HUB' and place.address != address:
                temp_distance = self.get_distance_between(place.address, address)
                if min_distance is None:
                    min_distance = temp_distance
                if closest_place is None:
                    closest_place = place

                elif temp_distance < min_distance:
                    print("New closest place found. Old distance: " + str(min_distance) + " | New Distance: " + str(
                        temp_distance))
                    print("Old closest place: " + closest_place.address + " | New Place: " + place.address)
                    closest_place = place
                    min_distance = temp_distance

        if closest_place is None:
            raise Exception("Something very wrong has occurred, no closest place has been found")

        return closest_place
