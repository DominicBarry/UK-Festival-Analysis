"""
Script: historical-weather.py
Purpose: Collects 30 years of historical weather data (1995-2024) for UK festivals
Input: data/festivals.csv (contains festival details with lat/long)
Output: data/all_festivals_historical_weather.csv
Author: Dom Barry
"""

import pandas as pd
import requests
import time
from datetime import datetime
import os

# Define file paths
DATA_DIR = 'data'
INPUT_FILE = os.path.join(DATA_DIR, 'festivals.csv')
CHECKPOINT_DIR = os.path.join(DATA_DIR, 'checkpoints')

# Create checkpoint directory if it doesn't exist
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

[Rest of your existing functions remain the same until save_checkpoint]

def save_checkpoint(records, start_idx, end_idx):
    """
    Saves a chunk of festival data to a checkpoint file in the checkpoints directory
    Each file contains only the new data for festivals in the range
    """
    df = pd.DataFrame(records)
    checkpoint_file = os.path.join(CHECKPOINT_DIR, f'weather_data_festivals_{start_idx+1}_to_{end_idx}.csv')
    df.to_csv(checkpoint_file, index=False)
    print(f"Saved data for festivals {start_idx+1} to {end_idx} to {checkpoint_file}")
    return checkpoint_file

def combine_checkpoint_files(start_festival, end_festival):
    """
    Combines all checkpoint files within the specified festival range into a single file
    """
    print(f"Looking for files containing festivals {start_festival} to {end_festival}")
    
    # Get list of relevant checkpoint files
    checkpoint_files = []
    for filename in os.listdir(CHECKPOINT_DIR):
        if filename.startswith('weather_data_festivals_'):
            try:
                numbers = [int(s) for s in filename.replace('.csv','').split('_') if s.isdigit()]
                if len(numbers) >= 2:
                    file_start = numbers[0]
                    file_end = numbers[1]
                    if not (file_end < start_festival or file_start > end_festival):
                        checkpoint_files.append(os.path.join(CHECKPOINT_DIR, filename))
            except ValueError:
                continue
    
    print(f"\nCombining {len(checkpoint_files)} checkpoint files...")
    print("Files to be combined:")
    for file in sorted(checkpoint_files):
        print(f"- {file}")
    
    # Read and combine all files
    all_data = []
    for file in sorted(checkpoint_files):
        print(f"Reading {file}")
        df = pd.read_csv(file)
        df = df[df['festival_id'].between(start_festival, end_festival)]
        all_data.append(df)
    
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df = final_df.sort_values(['festival_id', 'historical_year', 'full_date'])
        actual_max_id = final_df['festival_id'].max()
        
        # Save to data directory
        output_file = os.path.join(DATA_DIR, f'all_festivals_historical_weather.csv')
        final_df.to_csv(output_file, index=False)
        print(f"\nCreated combined file: {output_file}")
        print(f"Total records: {len(final_df)}")
        
        unique_festivals = sorted(final_df['festival_id'].unique())
        print(f"Unique festivals in combined file: {len(unique_festivals)}")
        print(f"Festival IDs included: {min(unique_festivals)} to {max(unique_festivals)}")
        
        return output_file
    else:
        print("No checkpoint files found to combine")
        return None

def main(start_festival=0, end_festival=207):
    """
    Main function to process festivals and collect weather data
    Parameters:
    - start_festival: Index to start processing from (0-based)
    - end_festival: Index to process up to (exclusive)
    """
    print("Starting historical weather data collection...")
    
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")
    
    print(f"Processing festivals {start_festival + 1} to {end_festival}")
    print("Collecting data for years 1995-2024")
    
    # Load and slice festival data
    festivals_df = pd.read_csv(INPUT_FILE)
    festivals_to_process = festivals_df.iloc[start_festival:end_festival]
    total_festivals = len(festivals_to_process)

    [Rest of main function remains the same]

if __name__ == "__main__":
    # Example usage:
    # For first chunk (festivals 1-50):
    main(start_festival=0, end_festival=50)
    
    # To process all festivals:
    # main(start_festival=0, end_festival=207)
    
    # To resume from a specific festival:
    # main(start_festival=15, end_festival=50)  # Resume from festival 16