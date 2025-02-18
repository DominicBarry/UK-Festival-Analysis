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

def create_historical_dates(start_date, end_date):
    """
    Takes a festival's 2025 dates and creates equivalent dates for years 1995-2024
    Example: If festival is 11/06/2025 - 15/06/2025
    Creates date pairs for 11/06-15/06 for each year 1995-2024
    """
    date_ranges = []
    
    # Parse 2025 dates using UK format (DD/MM/YYYY)
    start_dt = pd.to_datetime(start_date, format='%d/%m/%Y')
    end_dt = pd.to_datetime(end_date, format='%d/%m/%Y')
    
    # Extract day and month (ignore year as we'll use these for historical dates)
    start_day = start_dt.day
    start_month = start_dt.month
    end_day = end_dt.day
    end_month = end_dt.month
    
    # Create equivalent dates for each year 1995-2024
    for year in range(1995, 2025):
        historical_start = pd.Timestamp(year=year, month=start_month, day=start_day)
        historical_end = pd.Timestamp(year=year, month=end_month, day=end_day)
        date_ranges.append((historical_start, historical_end))
    
    return date_ranges

def fetch_historical_weather(lat, long, start_date, end_date):
    """
    Fetches weather data from OpenMeteo API for given dates and location
    Includes rate limit handling and retries
    """
    base_url = "https://archive-api.open-meteo.com/v1/archive"
    
    # Set up API parameters
    params = {
        'latitude': float(lat),
        'longitude': float(long),
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'daily': ['temperature_2m_max', 'temperature_2m_min', 'precipitation_sum', 'rain_sum', 'windspeed_10m_max'],
        'timezone': 'Europe/London'
    }
    
    max_retries = 5
    base_delay = 3  # 3 second delay between requests
    
    # Try the API call with retry logic
    for attempt in range(max_retries):
        try:
            response = requests.get(base_url, params=params)
            
            # Handle rate limiting
            if response.status_code == 429:  # Rate limit hit
                wait_time = (attempt + 1) * 120  # 2 minutes, increasing with each retry
                print(f"Rate limit hit. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue
                
            response.raise_for_status()
            time.sleep(base_delay)  # Basic delay between requests
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 60
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                return None
    return None

def process_historical_weather(weather_data, festival_info, year):
    """
    Processes raw weather API data into structured records
    Creates one record per day for the festival period
    """
    if not weather_data or 'daily' not in weather_data:
        return []
    
    daily = weather_data['daily']
    records = []
    
    # Create a record for each day in the festival period
    for i in range(len(daily['time'])):
        record = {
            'festival_id': festival_info['ID'],
            'festival_name': festival_info['Title'],
            'historical_year': year,
            'calendar_date': daily['time'][i][-5:],  # Extract MM-DD
            'full_date': daily['time'][i],
            'max_temp_c': daily['temperature_2m_max'][i],
            'min_temp_c': daily['temperature_2m_min'][i],
            'rainfall_mm': daily['rain_sum'][i],
            'total_precipitation_mm': daily['precipitation_sum'][i],
            'max_windspeed_kmh': daily['windspeed_10m_max'][i],
            'lat': festival_info['lat'],
            'long': festival_info['long']
        }
        records.append(record)
    
    return records

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
    
    # Initialize processing variables
    chunk_size = 10
    current_chunk = []
    chunk_start_idx = start_festival
    successful_festivals = 0
    failed_festivals = []
    
    # Process each festival
    for idx, festival in festivals_to_process.iterrows():
        try:
            print(f"\nProcessing festival {idx + 1}/{end_festival}: {festival['Title']}")
            
            # Get historical date ranges for this festival
            festival_records = []
            years_processed = 0
            
            # Process each year for this festival
            date_ranges = create_historical_dates(festival['startDate'], festival['endDate'])
            for start_date, end_date in date_ranges:
                year = start_date.year
                
                weather_data = fetch_historical_weather(
                    festival['lat'],
                    festival['long'],
                    start_date,
                    end_date
                )
                
                if weather_data:
                    records = process_historical_weather(weather_data, festival, year)
                    festival_records.extend(records)
                    years_processed += 1
                    print(f"Processed year {year}")
                else:
                    print(f"Failed to get data for {year}")
            
            # Add festival data to current chunk
            if festival_records:
                current_chunk.extend(festival_records)
                successful_festivals += 1
                print(f"Successfully processed {years_processed} years for {festival['Title']}")
            else:
                failed_festivals.append(festival['Title'])
            
            # Save checkpoint if chunk is full or we're at the end
            if len(current_chunk) >= chunk_size * 30 or idx == end_festival - 1:
                save_checkpoint(current_chunk, chunk_start_idx, idx + 1)
                current_chunk = []
                chunk_start_idx = idx + 1
                
        except Exception as e:
            print(f"Error processing {festival['Title']}: {e}")
            print(f"Last processed festival index: {idx}")
            failed_festivals.append(festival['Title'])
            # Save current chunk before failing
            if current_chunk:
                save_checkpoint(current_chunk, chunk_start_idx, idx + 1)
            raise
    
    # Combine checkpoint files into final dataset
    print("\nCreating final combined dataset...")
    combined_file = combine_checkpoint_files(start_festival, end_festival)
    
    if combined_file:
        print(f"\nFinal dataset saved to: {combined_file}")
    
    # Print completion summary
    print("\nData collection completed!")
    print(f"Successfully processed: {successful_festivals}/{total_festivals} festivals")
    
    if failed_festivals:
        print("\nFailed to process these festivals:")
        for festival in failed_festivals:
            print(f"- {festival}")

if __name__ == "__main__":
    # Test run with just first 2 festivals
    main(start_festival=0, end_festival=2)
