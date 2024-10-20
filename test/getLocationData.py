import pandas as pd

def load_valid_hotel_ids(filepath):
    """Load valid hotel IDs from a CSV file."""
    data = pd.read_csv(filepath)
    return set(data['id'])  # Using a set for faster membership testing

def combine_files(file_list):
    """Combine multiple CSV files into a single DataFrame."""
    combined_data = pd.concat([pd.read_csv(f) for f in file_list], ignore_index=True)
    return combined_data

def filter_hotels_and_places(data, valid_ids):
    """Filter a DataFrame to only include rows with valid hotel IDs."""
    filtered_data = data[data['Hotel ID'].isin(valid_ids)]
    return filtered_data

if __name__ == "__main__":
    # File paths
    marriott_file = "marriott_hotels_lat_long.csv"
    input_files = [f"hotels_and_places_{i}.csv" for i in range(8)]  # List of file names from 0 to 7
    output_file = "filtered_hotels_and_places.csv"
    
    # Load valid hotel IDs
    valid_hotel_ids = load_valid_hotel_ids(marriott_file)
    
    # Combine input files
    combined_data = combine_files(input_files)
    
    # Filter combined data by valid hotel IDs
    filtered_data = filter_hotels_and_places(combined_data, valid_hotel_ids)
    filtered_data.to_csv(output_file, index=False)
    
    print(f"Filtered data written to {output_file}")
