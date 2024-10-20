import os
import googlemaps


class googleMapsService: 
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        self.client = googlemaps.Client(key=self.api_key)
        
class amadeusService:
    
    def __init__(self):
        self.api_key = os.getenv('AMADEUS_API_KEY')
        self.api_secret = os.getenv('AMADEUS_API_SECRET')
    
    