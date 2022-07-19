from models.Place import Place
import pandas as pd


class PlaceService:
    """A service class to assist with retrieving places

    """
    def __init__(self):
        self.place_list = []
        self.ingest_places()

    def ingest_places(self):
        """A function that runs during class init to read in Place data from distances.csv in root.

        """
        print("Ingesting places...")
        df = pd.read_csv('./distances.csv', keep_default_na="")
        for index, row in df.iterrows():
            new_place = Place(index, row['Name'], row['Address'], row['Zip'])
            self.place_list.append(new_place)
        print("Finished ingesting places")
