from typing import List
from production.const import MAX_POI_DISTANCE
from production.util import haversine_distance

class POI:
    #Place Name,lat,long,distance,Rating,Number of Ratings,Place Type
    def __init__(self, name: str, latitude: float, longitude: float, rating: float, numberOfRatings: int, placeType: str):
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
        self.distance: float = -1.0
        

class Hotel:
    def __init__(self, hotelId : int, latitude: float, longitude: float, name: str, address: str):
        self.hotelId: int = hotelId
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
        poi.distance = haversine_distance(self.latitude, self.longitude, poi.latitude, poi.longitude)
        if(poi.distance <= MAX_POI_DISTANCE):
            self.pois.append(poi)
        return
    

