import requests
import googlemaps
import pandas as pd
import time
import math


# Load your API key
API_KEY = 'AIzaSyAjQM8DzQDosr3XDgkcVui_MjuaJmEIW0E'
# List of place types
place_types = [
    'airport', 'amusement_park', 'aquarium', 'art_gallery', 'casino',
    'church', 'city_hall', 'embassy', 'hindu_temple', 'hospital',
    'light_rail_station', 'local_government_office', 'lodging', 'mosque', 'museum', 'night_club', 'park',
    'shopping_mall', 'spa',
    'stadium', 'synagogue', 'tourist_attraction', 'train_station', 'transit_station',
    'university', 'zoo'
]

# Base URLs
geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
places_search_url = "https://places.googleapis.com/v1/places:searchNearby"
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth.

    Parameters:
    lat1, lon1: float - Latitude and longitude of the first point.
    lat2, lon2: float - Latitude and longitude of the second point.

    Returns:
    Distance in meters.
    """
    # Radius of the Earth in meters
    R = 6371000

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in meters
    distance = R * c
    return distance

# Example usage:
lat1, lon1 = 38.8977, -77.0365  # White House coordinates
lat2, lon2 = 40.7128, -74.0060  # New York City coordinates

print(f"Distance: {haversine_distance(lat1, lon1, lat2, lon2)} meters")
# Geocode the hotel address to get latitude and longitude
def geocode_address(address):
    params = {'address': address, 'key': API_KEY}
    response = requests.get(geocode_url, params=params)
    if response.status_code == 200:
        geocode_result = response.json()
        if geocode_result['results']:
            location = geocode_result['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None

# Perform the Nearby Search for a hotel in a single API call
def nearby_search(hotel_id, lat, lon, radius=1000*10):
    # Create the JSON request body with all place types included
    body = {
        "includedTypes": place_types,
        "maxResultCount": 20,  # Adjust based on the maximum number of results you need
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": lat,
                    "longitude": lon
                },
                "radius": radius
            }
        }
    }

    # Add the FieldMask header to specify which fields to include in the response
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.location,places.rating,places.userRatingCount,places.types"
    }

    # Make the POST request to the Places API
    response = requests.post(places_search_url, json=body, headers=headers)
    if response.status_code == 200:
        places = response.json().get('places', [])
        results = []
        for place in places:
            place_name = place.get('displayName', {'text': 'N/A'}).get('text', 'N/A')
            rating = place.get('rating', 'N/A')
            location = place.get('location', {})
            place_lat = location.get('latitude', 'N/A')
            place_lon = location.get('longitude', 'N/A')
            distance = haversine_distance(lat, lon, place_lat, place_lon)
            user_ratings_total = place.get('userRatingCount', 'N/A')
            place_type = ','.join(place.get('types', []))
            results.append([hotel_id, place_name,place_lat,place_lon, distance, rating, user_ratings_total, place_type])
        print(f"Found {len(results)} places.")
        return results
    else:
        print(f"Error for hotel {hotel_id}: {response.status_code}, {response.text}")
        return []

# Write nearby places to a CSV file
def write_to_csv(hotel_id, hotel_name, address, nearby_places, file_index):
    file_name = f'hotels_and_places_{file_index}.csv'
    df = pd.DataFrame(nearby_places, columns=['Hotel ID', 'Place Name',"lat","long","distance", 'Rating', 'Number of Ratings', 'Place Type'])
    df['Hotel Name'] = hotel_name
    df['Hotel Address'] = address

    # Append to the file (create new header if it's a new file)
    df.to_csv(file_name, mode='a', header=not pd.io.common.file_exists(file_name), index=False)

# Process the hotels and get nearby places
def process_hotels(file_path):
    df_hotels = pd.read_csv(file_path)
    file_index = 0

    for i, row in df_hotels.iterrows():
        hotel_id = i + 1
        hotel_name = row['Hotel Name']
        address = row['Address']
        
        # Geocode the hotel to get latitude and longitude
        lat, lon = geocode_address(address)

        if lat and lon:
            print(f"Processing {hotel_name} (ID: {hotel_id}) at {lat}, {lon}...")

            # Get nearby places for the hotel
            nearby_places = nearby_search(hotel_id, lat, lon)
            if(nearby_places.count == 0):
                print(f"No nearby places found for {hotel_name} (ID: {hotel_id})")
            else:
            # Write the nearby places to CSV
                write_to_csv(hotel_id, hotel_name, address, nearby_places, file_index)
        
        # For every 500 hotels, increase the file index to create a new file
        if (hotel_id % 500) == 0:
            file_index += 1

        # Add a delay to avoid API rate limits
        time.sleep(1)

# Run the process for all hotels in the CSV file
process_hotels('marriott_hotels.csv')