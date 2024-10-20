import math
import os
import googlemaps


class googleMapsService: 
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        self.client = googlemaps.Client(key=self.api_key)
        
class amadeusService:
    """the amadeus service is responable for collecting price data of a hotel"""
    
    def __init__(self):
        self.api_key = os.getenv('AMADEUS_API_KEY')
        self.api_secret = os.getenv('AMADEUS_API_SECRET')


def haversine_distance(lat_1: float, lon_1: float, lat_2: float, lon_2: float) -> float:
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