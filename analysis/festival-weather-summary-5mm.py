"""
Script: festival-weather-summary-5mm.py
Purpose: Creates festival-level weather metrics and scoring, considering days with >5mm rain as rain days
Input: data/all_festivals_historical_weather.csv
Output: data/festival_weather_comparison.csv
Author: Dom Barry
"""

import pandas as pd
import numpy as np
from scipy import stats
import os

# Define file paths
DATA_DIR = 'data'
INPUT_FILE = os.path.join(DATA_DIR, 'all_festivals_historical_weather.csv')
OUTPUT_FILE = os.path.join(DATA_DIR, 'festival_weather_comparison.csv')

def load_weather_data():
    """
    Loads the historical weather data and performs initial validation
    Returns DataFrame if successful
    """
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")
    
    print(f"Loading data from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} records")
    return df

def calculate_festival_metrics(df):
    """
    Calculates weather metrics for each festival
    Returns DataFrame with festival-level metrics
    """
    print("Calculating festival weather metrics...")
    
    # Group by festival and calculate metrics
    festival_metrics = df.groupby('festival_name').agg({
        'max_temp_c': ['mean', 'min', 'max', 'std'],
        'min_temp_c': ['mean', 'min', 'max', 'std'],
        'rainfall_mm': ['mean', 'max', 'sum'],
        'max_windspeed_kmh': ['mean', 'max', 'std'],
        'full_date': 'count'  # Total days
    }).round(2)

    # Flatten column names
    festival_metrics.columns = [
        'mean_max_temp', 'min_max_temp', 'max_max_temp', 'temp_std_dev',
        'mean_min_temp', 'min_min_temp', 'max_min_temp', 'min_temp_std_dev',
        'avg_daily_rainfall', 'max_daily_rainfall', 'total_rainfall',
        'mean_max_wind', 'overall_max_wind', 'wind_std_dev',
        'total_days'
    ]

    # Calculate rain days (>5mm rainfall)
    rain_days = df[df['rainfall_mm'] > 5].groupby('festival_name').size()
    festival_metrics['total_rain_days'] = rain_days
    festival_metrics['pct_rain_days'] = (rain_days / festival_metrics['total_days'] * 100).round(2)

    return festival_metrics

def calculate_weather_scores(df):
    """
    Calculates standardized weather scores based on temperature, rain, and wind
    Higher scores indicate better weather conditions
    """
    print("Calculating weather scores...")
    
    # Calculate z-scores (inverse for rain and wind where lower is better)
    df['temp_z'] = stats.zscore(df['mean_max_temp'])
    df['rain_z'] = -stats.zscore(df['pct_rain_days'])
    df['wind_z'] = -stats.zscore(df['mean_max_wind'])
    
    # Calculate overall weather score (average of z-scores)
    df['weather_score'] = df[['temp_z', 'rain_z', 'wind_z']].mean(axis=1).round(2)
    
    return df

def main():
    """
    Main function to process weather data and generate festival summaries
    """
    try:
        # Load and process data
        weather_data = load_weather_data()
        
        # Calculate metrics
        festival_metrics = calculate_festival_metrics(weather_data)
        
        # Calculate weather scores
        festival_metrics = calculate_weather_scores(festival_metrics)
        
        # Save results
        print(f"\nSaving results to {OUTPUT_FILE}")
        festival_metrics.to_csv(OUTPUT_FILE)
        print("Analysis complete!")
        
        # Print summary statistics
        print("\nSummary Statistics:")
        print(f"Total festivals analyzed: {len(festival_metrics)}")
        print("\nTop 5 festivals by weather score:")
        print(festival_metrics.nlargest(5, 'weather_score')[['weather_score', 'pct_rain_days', 'mean_max_temp']])
        
    except Exception as e:
        print(f"Error during processing: {e}")

if __name__ == "__main__":
    main()
