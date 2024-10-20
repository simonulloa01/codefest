import csv
import requests
API_KEY = '20495EF616A845F58C74D2EBB2950A6B'

def get_tripadvisor_id(hotel_name, address, lat, lon):
    api_url = "https://api.tripadvisor.com/v2/hotel_search"  # Hypothetical endpoint
    params = {
        "query": hotel_name,
        "lat": lat,
        "lon": lon,
        "address": address
    }
    
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        # Parse the returned data to extract the hotel ID (assuming the API returns it)
        return data['hotel_id']  # Hypothetical response field for hotel ID
    else:
        return None

# Path to the original CSV file
input_file_path = 'hotels.csv'
# Path to the new CSV file to be created
output_file_path = 'trips_id.csv'

# Open the original CSV file for reading
with open(input_file_path, mode='r', newline='', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    # Create a new CSV file for writing
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
        fieldnames = ['id', 'Hotel Name', 'Address', 'Latitude', 'Longitude', 'TripAdvisorId']
        csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        
        # Read each row from the original CSV
        for row in csv_reader:
            
            # Retrieve TripAdvisor ID for the hotel
            tripadvisor_id = get_tripadvisor_id(row['Hotel Name'], row['Address'], row['Latitude'], row['Longitude'])
            
            # Write the new row to the output CSV
            csv_writer.writerow({
                'id': row['id'],
                'Hotel Name': row['Hotel Name'],
                'Address': row['Address'],
                'Latitude': row['Latitude'],
                'Longitude': row['Longitude'],
                'TripAdvisorId': tripadvisor_id
            })