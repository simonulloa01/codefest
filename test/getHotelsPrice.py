
import time
import math
import pandas as pd
import requests
from datetime import datetime, timedelta

# Constants
client_id = 'rAzoJyXSy1mh8vIqVA7iV0ujRGKIR7Hm'
client_secret='52v8BJqnXG1eE0Ga'
AMADEUS_ENDPOINT = 'https://test.api.amadeus.com/v3/shopping/hotel-offers'
token_url = 'https://test.api.amadeus.com/v1/security/oauth2/token'

def get_access_token():
    """Fetch access token from Amadeus API."""
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception("Failed to fetch access token")
    
def get_closest_hotel_ids(latitude, longitude, bearer_token):
    url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-geocode"
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "radius": 1
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        hotels = response.json()
        # get all the hotels in the area and return them
        hotel_ids = [hotel['hotelId'] for hotel in hotels['data']]
        
        return hotel_ids
        
        
        
    else:
        return "Null"
    
def get_monthly_prices(lat, lon, check_in_date, check_out_date,token):
    """Fetch hotel pricing information from Amadeus API."""
    hotel_ids = get_closest_hotel_ids(lat, lon, token)
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        "hotelIds": hotel_ids[0],
        "adults": 1,
        'checkInDate': check_in_date,
        'checkOutDate': check_out_date
    }
    if(hotel_ids == "Null"):
        return 0
    
    response = requests.get(AMADEUS_ENDPOINT, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        # You need to parse the JSON response to extract pricing data
        # Here you might sum up daily rates or get a total price
        price = 0
        try:
            price = data['data'][0]['offers'][0]['price']['total']
            price = float(price)
        except:
            price = 0
        return price
    else:
        print("Failed to fetch data:", response.json())
        print("Skipping hotel due to error")
        return 0

def process_hotels(file_path):
    token = get_access_token()
    # Read the hotel data
    hotels = pd.read_csv(file_path)
    results = []

    for index, row in hotels.iterrows():
        ##resume at index 815
        if(index < 3376):
            continue
        hotel_id = row['id']
        hotel_name = row['Hotel Name']
        latitude = row['Latitude']
        longitude = row['Longitude']

        # Assuming you want to check for the next upcoming month
        #get the first day of the june 2025 month
        start_date = datetime(2025, 1, 14)
        end_date = datetime(2025, 1, 16)

        monthly_price = get_monthly_prices(latitude, longitude, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'),token)
        days_in_month = (end_date - start_date).days + 1
        average_daily_price = monthly_price / days_in_month
        if(average_daily_price == 0):
            continue
        #sleep for 0.2 seconds to not exceed the rate limit
       
        # print to file after each hotel
        print(f"Processed {hotel_name} - Average Daily Price: {average_daily_price}")
        with open('hotel_pricing_results.csv', 'a') as f:
            f.write(f"{hotel_id},{hotel_name},{row['Address']},{latitude},{longitude},{average_daily_price}\n") 
       
    
    # Convert results to DataFrame and save or return
    results_df = pd.DataFrame(results)
    results_df.to_csv('hotel_pricing_results.csv', index=False)
    return results_df

# Usage
file_path = 'marriott_hotels_cords.csv'
hotel_pricing_data = process_hotels(file_path)
print(hotel_pricing_data)
