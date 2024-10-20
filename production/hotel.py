from typing import List
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
        
    
    def predictPrice(self):
        """
        Predict the price of the hotel based on the model
        """
        pass
    def getPrice(self):
        """
        Get the price of the hotel from the Amadeus API.
        """
        pass
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
        

