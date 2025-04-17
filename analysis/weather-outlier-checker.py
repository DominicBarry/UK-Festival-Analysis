"""
Script: weather-outlier-checker.py
Purpose: Identifies and analyzes outliers in festival weather data
Input: data/all_festivals_historical_weather.csv
Output: Prints outlier analysis report to console
Author: Dom Barry
"""

import pandas as pd
import numpy as np
from scipy import stats
import os

# Define file paths
DATA_DIR = 'data'
INPUT_FILE = os.path.join(DATA_DIR, 'all_festivals_historical_weather.csv')

def load_data():
    """
    Loads weather data and performs initial validation
    Returns DataFrame if successful
    """
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")
    
    print(f"Loading data from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} records")
    return df

def identify_outliers(data, column):
    """
    Identifies outliers using the IQR method
    Returns lower bound, upper bound, and outlier mask
    """
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = (data[column] < lower_bound) | (data[column] > upper_bound)
    return lower_bound, upper_bound, outliers

def analyze_temperature_outliers(df):
    """
    Analyzes temperature outliers
    """
    print("\nAnalyzing Temperature Outliers:")
    print("="*50)
    
    # Max temperature outliers
    lower, upper, outliers = identify_outliers(df, 'max_temp_c')
    outlier_records = df[outliers]
    
    print("\nMaximum Temperature Outliers:")
    print(f"Normal range: {lower:.1f}°C to {upper:.1f}°C")
    print(f"Found {len(outlier_records)} outliers")
    
    if len(outlier_records) > 0:
        print("\nTop 5 highest temperatures:")
        for _, row in outlier_records.nlargest(5, 'max_temp_c').iterrows():
            print(f"{row['festival_name']}: {row['max_temp_c']:.1f}°C on {row['full_date']}")
        
        print("\nTop 5 lowest temperatures:")
        for _, row in outlier_records.nsmallest(5, 'max_temp_c').iterrows():
            print(f"{row['festival_name']}: {row['max_temp_c']:.1f}°C on {row['full_date']}")

def analyze_rainfall_outliers(df):
    """
    Analyzes rainfall outliers
    """
    print("\nAnalyzing Rainfall Outliers:")
    print("="*50)
    
    lower, upper, outliers = identify_outliers(df, 'rainfall_mm')
    outlier_records = df[outliers]
    
    print(f"\nNormal rainfall range: {lower:.1f}mm to {upper:.1f}mm")
    print(f"Found {len(outlier_records)} outliers")
    
    if len(outlier_records) > 0:
        print("\nTop 5 heaviest rainfall days:")
        for _, row in outlier_records.nlargest(5, 'rainfall_mm').iterrows():
            print(f"{row['festival_name']}: {row['rainfall_mm']:.1f}mm on {row['full_date']}")

def analyze_wind_outliers(df):
    """
    Analyzes wind speed outliers
    """
    print("\nAnalyzing Wind Speed Outliers:")
    print("="*50)
    
    lower, upper, outliers = identify_outliers(df, 'max_windspeed_kmh')
    outlier_records = df[outliers]
    
    print(f"\nNormal wind speed range: {lower:.1f}km/h to {upper:.1f}km/h")
    print(f"Found {len(outlier_records)} outliers")
    
    if len(outlier_records) > 0:
        print("\nTop 5 windiest days:")
        for _, row in outlier_records.nlargest(5, 'max_windspeed_kmh').iterrows():
            print(f"{row['festival_name']}: {row['max_windspeed_kmh']:.1f}km/h on {row['full_date']}")

def main():
    """
    Main function to run outlier analysis
    """
    try:
        # Load data
        df = load_data()
        
        # Run outlier analyses
        analyze_temperature_outliers(df)
        analyze_rainfall_outliers(df)
        analyze_wind_outliers(df)
        
        print("\nOutlier analysis complete!")
        
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    main()
