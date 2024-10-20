import pandas as pd

def truncate_float(value):
    """Truncate the last two decimal places of a float."""
    return int(value * 100) / 100.0  # Using int for truncation

def process_csv(input_filepath, output_filepath):
    # Load data from CSV file
    data = pd.read_csv(input_filepath)
    
    # Apply the truncate_float function to the 'distance' column
    data['distance'] = data['distance'].apply(truncate_float)
    
    # Save the processed data to a new CSV file
    data.to_csv(output_filepath, index=False)
    print(f"Processed data written to {output_filepath}")

# File paths
input_file = "filter_hotel_places_single_type_4.csv"
output_file = "fliter_hotel_place.csv"

# Process the CSV file
process_csv(input_file, output_file)
