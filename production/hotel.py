from typing import List

import numpy as np
from const import *
import math

class POI:
    #Place Name,lat,long,distance,Rating,Number of Ratings,Place Type
    def __init__(self, name: str, latitude: float, longitude: float, rating: float, numberOfRatings: int, placeType: str, distance: float):
        """Create a point of interest object for the model to ingest.
        Args:
            hotel (Hotel): the hotel object that the POI realated to
            name (str): the name of the POI
            latitude (float): the latitude of the POI
            longitude (float): the longitude of the POI
            rating (float): the rating of the POI
            numberOfRatings (int): the number of ratings of the POI
            placeType (str): the type of the POI (e.g. restaurant, museum, etc.)
        """
        self.name: str = name
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.rating: float = rating
        self.numberOfRatings: int = numberOfRatings
        self.placeType: str = placeType
        self.distance: float = distance
    
    def to_dict(self):
        """ Convert the POI object to a dictionary."""
        return {
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "rating": self.rating,
            "numberOfRatings": self.numberOfRatings,
            "placeType": self.placeType,
            "distance": self.distance
        }
        

class Hotel:
    def __init__(self, hotelId : str, latitude: float, longitude: float, name: str, address: str):
        self.hotelId: str = hotelId
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.name: str = name
        self.address: str = address
        self.actualPrice: float = -1.0
        self.predictedPrice: float = -1.0
        self.pois: List[POI] = []
        
    
    def predictPrice(self, model):
    # Load the pre-trained model
        # Define the maximum number of POIs to consider
        max_pois = 20

        # You might want to adjust this based on how many features per POI and how many POIs you're considering
        # For simplicity, assuming 4 features per POI and 20 POIs: distance, rating, number_of_ratings, place_type (mapped)
        num_pois = 20
        features_per_poi = 3
        features = np.zeros(num_pois * features_per_poi)

        # Map for place types if your model requires numeric data
        place_type_map = {
            'airport': 1, 'amusement_park': 2, 'aquarium': 3, 'art_gallery': 4, 'casino': 5,
            'church': 6, 'city_hall': 7, 'embassy': 8, 'hindu_temple': 9, 'hospital': 10,
            'light_rail_station': 11, 'local_government_office': 12, 'lodging': 13, 'mosque': 14, 'museum': 15,
            'night_club': 16, 'park': 17, 'shopping_mall': 18, 'spa': 19, 'stadium': 20,
            'synagogue': 21, 'tourist_attraction': 22, 'train_station': 23, 'transit_station': 24, 'university': 25, 'zoo': 26
        }

        # Extract features from the hotel's POIs
        for i, poi in enumerate(self.pois[:num_pois]):  # Limit to the first 20 POIs
            base_index = i * features_per_poi
            features[base_index] = poi.distance
            features[base_index + 1] = poi.rating
            features[base_index + 2] = poi.numberOfRatings


        # Predict the price using the loaded model
        predicted_price = model.predict([features])[0]  # model.predict expects a 2D array
        formatted_price = format(predicted_price, ".2f")

        self.predictedPrice = formatted_price

    def getPrice(self):
        """
        Get the price of the hotel from the Amadeus API.
        """
        
    def addPOI(self, poi : POI):
        """
        Add a point of interest to the hotel object.
        """
        poi.distance = self.haversine_distance(self.latitude, self.longitude, poi.latitude, poi.longitude)
        if(poi.distance <= MAX_POI_DISTANCE):
            self.pois.append(poi)
        return
    
    def to_dict(self):
        return {
            "hotelId": self.hotelId,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "name": self.name,
            "address": self.address,
            "actualPrice": self.actualPrice,
            "predictedPrice": self.predictedPrice,
            "pois": [poi.to_dict() for poi in self.pois]
        }
        
    def haversine_distance(self,lat_1: float, lon_1: float, lat_2: float, lon_2: float) -> float:
            # Convert latitude and longitude from degrees to radians
        lat_1_rad = math.radians(lat_1)
        lon_1_rad = math.radians(lon_1)
        lat_2_rad = math.radians(lat_2)
        lon_2_rad = math.radians(lon_2)

            # Haversine formula
        dlat = lat_2_rad - lat_1_rad
        dlon = lon_2_rad - lon_1_rad

        a = math.sin(dlat / 2)**2 + math.cos(lat_1_rad) * math.cos(lat_2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Radius of Earth in kilometers (use 6371 for kilometers, 3956 for miles)
        R = 6371

            # Distance in kilometers
        distance = R * c
        return distance
        

