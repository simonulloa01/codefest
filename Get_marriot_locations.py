from bs4 import BeautifulSoup
import pandas as pd

# Load your .kml file (replace 'marriott_hotels.kml' with your file path)
with open('marriott_hotels_us.kml', 'r', encoding='utf-8') as file:
    kml_data = file.read()

soup = BeautifulSoup(kml_data, 'xml')  # Use 'xml' parser to handle namespaces

# Define the namespace
namespace = {'kml': 'http://www.opengis.net/kml/2.2'}

# Find all Placemark elements within the namespace
placemarks = soup.find_all('Placemark')

# Initialize a list to store the hotel information
hotel_data = []

# Loop through each Placemark and extract relevant data
for placemark in placemarks:
    name = placemark.find('name').text if placemark.find('name') else 'N/A'
    address = placemark.find('address').text if placemark.find('address') else 'N/A'
    
    # Append the extracted data to the list
    hotel_data.append([name, address])

# Convert the list to a pandas DataFrame
df = pd.DataFrame(hotel_data, columns=['Hotel Name', 'Address'])

# Save the DataFrame to a CSV file
df.to_csv('marriott_hotels.csv', index=False)

print("Data extracted and saved to 'marriott_hotels.csv'")