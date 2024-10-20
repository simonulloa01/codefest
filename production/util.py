import math
import requests

from hotel import POI, Hotel
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
        

def nearby_search(hotel : Hotel) -> bool:
    # Create the JSON request body with all place types included
    place_types = [
    'airport', 'amusement_park', 'aquarium', 'art_gallery', 'casino',
    'church', 'city_hall', 'embassy', 'hindu_temple', 'hospital',
    'light_rail_station', 'local_government_office', 'lodging', 'mosque', 'museum', 'night_club', 'park',
    'shopping_mall', 'spa',
    'stadium', 'synagogue', 'tourist_attraction', 'train_station', 'transit_station',
    'university', 'zoo'
    ]
    body = {
        "includedTypes": place_types,
        "maxResultCount": 20,  # Adjust based on the maximum number of results you need
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": hotel.latitude,
                    "longitude": hotel.longitude
                },
                "radius": 1000*10
            }
        }
    }
    # Add the FieldMask header to specify which fields to include in the response
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": "AIzaSyAjQM8DzQDosr3XDgkcVui_MjuaJmEIW0E",
        "X-Goog-FieldMask": "places.displayName,places.location,places.rating,places.userRatingCount,places.types"
    }
    # Make the POST request to the Places API
    response = requests.post("https://places.googleapis.com/v1/places:searchNearby", json=body, headers=headers)
    
    if response.status_code == 200:
        places = response.json().get('places', [])
        for place in places:
            name = place.get('displayName', {'text': 'N/A'}).get('text', 'N/A')
            rating = float(place.get('rating', 0))
            location = place.get('location', {})
            latitude = float(location.get('latitude', 0))
            longitude = float(location.get('longitude', 0))
            user_ratings_total = int(place.get('userRatingCount', 0))
            types = place.get('types', [])
            place_type = types[0] if types else 'N/A'  # Get the first place type if available
            distance = haversine_distance(hotel.latitude, hotel.longitude, latitude, longitude)
            
            poi = POI(name, latitude, longitude, rating, user_ratings_total, place_type, distance)
            hotel.addPOI(poi)
        print(f"Added {len(hotel.pois)} POIs to hotel '{hotel.name}'.")
        return True
    else:
        print(f"Error for hotel '{hotel.name}': {response.status_code}, {response.text}")
        return False

def get_access_token() -> str:
    """Fetch access token from Amadeus API."""
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': 'GwUXcKXGux48StL5aMI6Wof4ag7WNirR',
        'client_secret': '2b6p4AVaPWWZRQ2O'
    }
    response = requests.post("https://test.api.amadeus.com/v1/security/oauth2/token", headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception("Failed to fetch access token")