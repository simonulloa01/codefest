from flask import Flask, jsonify, request
from production import Hotel
from production.const import MILES_TO_KM

app = Flask(__name__)



def getHotels(lat: float, long: float, radius: float) -> list[Hotel]: 
    pass


@app.route('/hotel/', methods=['GET'])
def get_hotel():
    
    lat = request.args.get('lat', type=float)
    long = request.args.get('long', type=float)
    radius = MILES_TO_KM * request.args.get('radius', type=float)
    # test data
    lat = 37.215163
    long = -80.423494
    radius = 20
    #list[Hotel] = getHotels(lat, long, radius)
    
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
