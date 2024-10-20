import csv
import requests

# Function to get latitude and longitude using Google Maps Geocoding API
def get_lat_long(address, google_api_key):
    # Replace spaces with '+' to format the address for the URL
    formatted_address = address.replace(" ", "+")
    
    # Google Maps Geocoding API endpoint
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={formatted_address}&key={google_api_key}"
    
    # Make the request
    response = requests.get(url)
    
    # Parse the JSON response
    data = response.json()
    
    # Check if the status is OK and results are available
    if data['status'] == 'OK' and len(data['results']) > 0:
        # Get latitude and longitude from the response
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return lat, lng
    else:
        print(f"Error finding location for address: {address}")
        return None, None

# Function to read the marriot_hotels.csv, get lat and long, and write to new CSV
def process_hotels(file_input, file_output, google_api_key):
    # Open the input CSV file for reading
    with open(file_input, mode='r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        # Open the output CSV file for writing (append mode to write after each call)
        with open(file_output, mode='w', newline='', encoding='utf-8') as csv_output:
            csv_writer = csv.writer(csv_output)
            
            # Write the header row
            csv_writer.writerow(["id", "Hotel Name", "Address", "Latitude", "Longitude"])
            
            # Skip the header row of the input file
            next(csv_reader)
            
            # Process each row in the input file
            for row in csv_reader:
                hotel_id = row[0]
                hotel_name = row[1]
                address = row[2]
                
                # Get latitude and longitude for the current address
                latitude, longitude = get_lat_long(address, google_api_key)
                
                # If valid lat/long is found, write to the CSV file immediately
                if latitude is not None and longitude is not None:
                    print(f"Writing data for {hotel_id}:{hotel_name} - {latitude},{longitude}")
                    csv_writer.writerow([hotel_id, hotel_name, address, latitude, longitude])
                else:
                    print(f"Skipping {hotel_name} due to missing lat/long")

# Example usage
if __name__ == "__main__":
    # Google API key (replace with your actual API key)
    google_api_key = "AIzaSyAjQM8DzQDosr3XDgkcVui_MjuaJmEIW0E"
    
    # Input and output file paths
    input_file = "marriott_hotels.csv"
    output_file = "marriott_hotels_lat_long.csv"
    
    # Process the hotels and write to the new file
    process_hotels(input_file, output_file, google_api_key)
