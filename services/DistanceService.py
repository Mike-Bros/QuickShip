import pandas as pd

from services.PlaceService import PlaceService


class DistanceService:
    def __init__(self):
        self.distance_list = []
        self.place_list = PlaceService().place_list
        self.ingest_distances()

    def ingest_distances(self):
        print("Ingesting packages...")
        df = pd.read_csv('./distances.csv', keep_default_na="")
        for index, row in df.iterrows():
            curr_address_distances = []
            for place in self.place_list:
                curr_address_distances.append(row[place.address])
            self.distance_list.append(curr_address_distances)
        print("Finished ingesting packages")

    def get_distance_between(self, address_a, address_b):
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
        return distance_value
