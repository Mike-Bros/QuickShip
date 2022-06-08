from models.Place import Place
import pandas as pd


class PlaceService:
    def __init__(self):
        self.place_list = []
        self.ingest_places()

    def ingest_places(self):
        print("Ingesting places...")
        df = pd.read_csv('./places.csv', keep_default_na="")
        for index, row in df.iterrows():
            new_place = Place(row['Name'], row['Address'], row['Zip'])
            self.place_list.append(new_place)
        print("Finished ingesting places")

