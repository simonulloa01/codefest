from flask import Flask, jsonify, request
from hotel import Hotel
from util import googleMapsService
app = Flask(__name__)



def getHotels(lat: float, long: float, radius: float) -> list[Hotel]: 
    GoogleMapsService = googleMapsService()
    # Get hotels from Google Maps API
    hotels = GoogleMapsService.client.places_nearby(location=(lat, long), radius=radius, type='lodging')
    # get the place_id of each hotel
    hotel_ids = [hotel['place_id'] for hotel in hotels['results']]
    #get the details of each hotel
    hotel_details = [GoogleMapsService.client.place(place_id=hotel_id) for hotel_id in hotel_ids]
    for hotel_query in hotel_details:
        hotel = Hotel(hotel_query['name'], hotel_query['geometry']['location']['lat'], hotel_query['geometry']['location']['lng'], hotel_query['formatted_address'])
        # add the hotel to the list of hotels
        hotels.append(hotel)
    return []


@app.route('/hotel/', methods=['GET'])
def get_hotel():
    
    lat = request.args.get('lat', type=float)
    long = request.args.get('long', type=float)
    radius = request.args.get('radius', type=float)
    # test data
    lat = 37.23283004520936
    long = -80.4305801374387
    radius = 10
    hotels = getHotels(lat, long, radius)
    print(hotels)
    # Example data
    hotel_data = {
        
        "hotelId": 1,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "name": "Hotel California",
        "address": "1234 California St, San Francisco, CA 94123",
        "actualPrice": 100.00,
        "predictedPrice": 110.00,
        "pois": [
            {
                "name": "Golden Gate Bridge",
                "latitude": 37.8199,
                "longitude": -122.4783,
                "rating": 4.7,
                "numberOfRatings": 10000,
                "placeType": "Bridge",
                "distance": 10.0
            },
            {
                "name": "Fisherman's Wharf",
                "latitude": 37.8080,
                "longitude": -122.4177,
                "rating": 4.5,
                "numberOfRatings": 5000,
                "placeType": "Wharf",
                "distance": 5.0
            }
        ]
    }
    return jsonify(hotel_data)
    

if __name__ == '__main__':
    app.run(debug=True)
