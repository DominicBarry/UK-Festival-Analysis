"""
Script: weather-data-validator-detailed.py
Purpose: Validates and analyzes weather data completeness and quality for festival data
Input: data/all_festivals_historical_weather.csv
Output: Prints detailed validation report to console
Author: Dom Barry
"""

import pandas as pd
import numpy as np
import os

# Define file paths
DATA_DIR = 'data'
INPUT_FILE = os.path.join(DATA_DIR, 'all_festivals_historical_weather.csv')

def load_and_validate_data():
    """
    Loads weather data and performs detailed validation checks
    Returns DataFrame if successful
    """
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")
    
    print(f"Loading data from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} records\n")
    return df

def print_section_header(title):
    """Prints formatted section header"""
    print("\n" + "="*50)
    print(title)
    print("="*50 + "\n")

def analyze_missing_values(df):
    """Analyzes and reports on missing values in the dataset"""
    print_section_header("Missing Values Analysis")
    
    missing_values = df.isnull().sum()
    print("Missing values by column:")
    for column, count in missing_values[missing_values > 0].items():
        print(f"{column}: {count} missing values ({(count/len(df))*100:.2f}%)")

def analyze_data_ranges(df):
    """Analyzes and reports on data ranges and potential outliers"""
    print_section_header("Data Ranges Analysis")
    
    numeric_columns = ['max_temp_c', 'min_temp_c', 'rainfall_mm', 
                      'total_precipitation_mm', 'max_windspeed_kmh']
    
    for column in numeric_columns:
        print(f"\n{column} Analysis:")
        print(f"Min: {df[column].min():.2f}")
        print(f"Max: {df[column].max():.2f}")
        print(f"Mean: {df[column].mean():.2f}")
        print(f"Std Dev: {df[column].std():.2f}")
        
        # Identify potential outliers using IQR method
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        
        if not outliers.empty:
            print(f"\nPotential outliers detected ({len(outliers)} records):")
            print(f"Values outside range: {lower_bound:.2f} to {upper_bound:.2f}")

def analyze_completeness_by_festival(df):
    """Analyzes data completeness for each festival"""
    print_section_header("Festival-level Completeness Analysis")
    
    festival_summary = df.groupby('festival_name').agg({
        'historical_year': 'nunique',
        'calendar_date': 'count'
    }).reset_index()
    
    print("Festivals with incomplete data:")
    incomplete = festival_summary[festival_summary['historical_year'] < 30]
    if len(incomplete) > 0:
        for _, row in incomplete.iterrows():
            print(f"\nFestival: {row['festival_name']}")
            print(f"Years of data: {row['historical_year']}")
            print(f"Total records: {row['calendar_date']}")
    else:
        print("All festivals have complete data for all 30 years")

def analyze_temporal_coverage(df):
    """Analyzes temporal coverage of the dataset"""
    print_section_header("Temporal Coverage Analysis")
    
    year_counts = df['historical_year'].value_counts().sort_index()
    print("Records per year:")
    for year, count in year_counts.items():
        print(f"{year}: {count} records")

def main():
    """
    Main function to run all validation checks
    """
    try:
        df = load_and_validate_data()
        
        print_section_header("Dataset Overview")
        print(f"Total records: {len(df)}")
        print(f"Unique festivals: {df['festival_name'].nunique()}")
        print(f"Date range: {df['full_date'].min()} to {df['full_date'].max()}")
        
        analyze_missing_values(df)
        analyze_data_ranges(df)
        analyze_completeness_by_festival(df)
        analyze_temporal_coverage(df)
        
    except Exception as e:
        print(f"Error during validation: {e}")

if __name__ == "__main__":
    main()
