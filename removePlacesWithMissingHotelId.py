import pandas as pd

def load_valid_hotel_ids(filepath):
    """Load valid hotel IDs from a CSV file."""
    data = pd.read_csv(filepath)
    return set(data['id'])  # Using a set for faster membership testing

def find_missing_ids(valid_ids, max_id):
    """Find missing IDs in the range from 0 to max_id."""
    full_set = set(range(max_id + 1))
    missing_ids = full_set - valid_ids
    return sorted(list(missing_ids))  # Return a sorted list of missing IDs

def filter_hotels_and_places(input_filepath, output_filepath, valid_ids):
    """Filter a CSV file to only include rows with valid hotel IDs."""
    data = pd.read_csv(input_filepath)
    filtered_data = data[data['Hotel ID'].isin(valid_ids)]
    filtered_data.to_csv(output_filepath, index=False)

if __name__ == "__main__":
    # File paths
    marriott_file = "marriott_hotels_lat_long.csv"
    input_file = "hotels_and_places_0.csv"
    output_file = "filtered_hotels_and_places_0.csv"
    
    # Load valid hotel IDs
    valid_hotel_ids = load_valid_hotel_ids(marriott_file)
    
    # Find and print missing IDs
    missing_ids = find_missing_ids(valid_hotel_ids, 3770)
    print(f"Missing IDs: {missing_ids}")
    
    # Filter the hotels_and_places_0.csv file by valid hotel IDs
    filter_hotels_and_places(input_file, output_file, valid_hotel_ids)
    
    print(f"Filtered data written to {output_file}")
