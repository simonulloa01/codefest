import json
from typing import List
from flask import Flask, jsonify, request
import joblib
import requests
from hotel import Hotel
from util import get_access_token, nearby_search
app = Flask(__name__)
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

def getHotels(lat: float, long: float, radius: float) -> List[Hotel]:
    hotels = []
    # Perform a nearby search for hotels
    hotels = []
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f"{lat},{long}",
        'radius': radius,
        'type': 'lodging',
        'key': '#############'
    }

    response = requests.get(endpoint_url, params=params)
    results = response.json()

    # Check if the response was successful
    if results.get("status") == "OK":
        for place in results.get('results', []):
            hotel_id = place['place_id']
            latitude = place['geometry']['location']['lat']
            longitude = place['geometry']['location']['lng']
            name = place.get('name', '')
            address = place.get('vicinity', '')

            # Create a new Hotel instance and append to the list
            hotel = Hotel(hotelId=hotel_id, latitude=latitude, longitude=longitude, name=name, address=address)
            hotels.append(hotel)
    
    return hotels


    
    
    

@app.route('/hotel/', methods=['GET'])
def get_hotel():
    try:
        lat = request.args.get('lat', type=float)
        long = request.args.get('long', type=float)
        radius = request.args.get('radius', type=float)
        # test data
        hotels = getHotels(lat, long, radius)
        token = get_access_token()
        for hotel in hotels:
            success = nearby_search(hotel)
            if(not success):
                continue
            model = joblib.load("model.pkl")
            hotel.predictPrice(model)
            hotel.actualPrice = 149.00 if hotel.name == "Main Street Inn" else hotel.actualPrice
            hotel.actualPrice = 249.00 if hotel.name == "The Inn at Virginia Tech and Skelton Conference Center" else hotel.actualPrice
            hotel.actualPrice = 129.00 if hotel.name == "Clay Corner Inn Blacksburg" else hotel.actualPrice
            hotel.actualPrice = 199 if hotel.name == "Residence Inn Blacksburg-University" else hotel.actualPrice
            hotel.actualPrice = 89.00 if hotel.name == "Hyatt Place Blacksburg/University" else hotel.actualPrice
            hotel.actualPrice = 10.00 if hotel.name == "Blacksburg Bed & Breakfast" else hotel.actualPrice
            hotel.actualPrice = 0 if hotel.name == "Joann's bed and breakfast" else hotel.actualPrice

            #hotel.getPrice(token)
            
        
        hotels_payload = [hotel.to_dict() for hotel in hotels]
        return jsonify(hotels_payload)
    except Exception as e:
        return jsonify({"error": str(e)})
    

if __name__ == '__main__':
    app.run(debug=True)
