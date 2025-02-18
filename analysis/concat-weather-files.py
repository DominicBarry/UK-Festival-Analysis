import pandas as pd

def concatenate_weather_files():
    """
    Concatenates specified weather CSV files into a single file
    """
    # List of files to combine
    files = [
        'festivals_weather_1_to_50.csv',
        'festivals_weather_51_to_150.csv',
        'festivals_weather_151_to_206.csv'
    ]
    
    print("Starting file concatenation...")
    
    # Read and combine files
    dfs = []
    for file in files:
        print(f"Reading {file}")
        df = pd.read_csv(file)
        dfs.append(df)
        print(f"Added {len(df)} rows from {file}")
    
    # Combine all dataframes
    final_df = pd.concat(dfs, ignore_index=True)
    
    # Sort by festival ID, year, and date
    final_df = final_df.sort_values(['festival_id', 'historical_year', 'full_date'])
    
    # Save combined file
    output_file = 'all_festivals_weather.csv'
    final_df.to_csv(output_file, index=False)
    
    # Print summary
    print("\nConcatenation complete!")
    print(f"Total records: {len(final_df)}")
    unique_festivals = sorted(final_df['festival_id'].unique())
    print(f"Unique festivals: {len(unique_festivals)}")
    print(f"Festival ID range: {min(unique_festivals)} to {max(unique_festivals)}")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    concatenate_weather_files()
