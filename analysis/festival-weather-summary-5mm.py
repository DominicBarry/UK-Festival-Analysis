import pandas as pd
import numpy as np
from scipy import stats

def create_festival_summary():
    """
    Creates festival weather summary with 5mm threshold for rain days
    """
    print("Loading weather data...")
    df = pd.read_csv('all_festivals_weather_cleaned.csv')
    
    print("Calculating festival-level metrics...")
    festival_metrics = df.groupby('festival_name').agg({
        'max_temp_c': ['mean', 'max', 'std'],
        'min_temp_c': ['mean', 'min'],
        'rainfall_mm': [
            lambda x: (x >= 5).sum(),  # Changed to count days with 5mm or more rain
            'count',
            'mean',
            'max'
        ],
        'max_windspeed_kmh': ['mean', 'max', 'std']
    }).reset_index()
    
    festival_metrics.columns = [
        'festival_name',
        'mean_max_temp', 'overall_max_temp', 'temp_std_dev',
        'mean_min_temp', 'overall_min_temp',
        'total_rain_days', 'total_days', 'avg_daily_rainfall', 'max_daily_rainfall',
        'mean_max_wind', 'overall_max_wind', 'wind_std_dev'
    ]
    
    festival_metrics['pct_rain_days'] = (festival_metrics['total_rain_days'] / 
                                       festival_metrics['total_days'] * 100)
    
    print("Calculating z-scores...")
    festival_metrics['temp_z'] = stats.zscore(festival_metrics['mean_max_temp'])
    festival_metrics['rain_z'] = stats.zscore(festival_metrics['avg_daily_rainfall'])
    festival_metrics['wind_z'] = stats.zscore(festival_metrics['mean_max_wind'])
    
    print("Calculating weather scores...")
    festival_metrics['weather_score'] = (
        festival_metrics['temp_z'] - 
        festival_metrics['rain_z'] - 
        festival_metrics['wind_z']
    )
    
    numeric_columns = festival_metrics.select_dtypes(include=['float64']).columns
    festival_metrics[numeric_columns] = festival_metrics[numeric_columns].round(2)
    
    columns_order = [
        'festival_name',
        'mean_max_temp',
        'mean_min_temp',
        'overall_max_temp',
        'overall_min_temp',
        'temp_std_dev',
        'total_rain_days',
        'total_days',
        'pct_rain_days',
        'avg_daily_rainfall',
        'max_daily_rainfall',
        'mean_max_wind',
        'overall_max_wind',
        'wind_std_dev',
        'temp_z',
        'rain_z',
        'wind_z',
        'weather_score'
    ]
    
    festival_metrics = festival_metrics[columns_order]
    
    output_file = 'festival_weather_comparison.csv'
    festival_metrics.to_csv(output_file, index=False)
    print(f"\nSaved festival weather comparison to {output_file}")
    
    print("\nSummary Statistics:")
    print(f"Number of festivals analyzed: {len(festival_metrics)}")
    print("\nTop 5 festivals by weather score:")
    print(festival_metrics.nlargest(5, 'weather_score')[['festival_name', 'weather_score']])

if __name__ == "__main__":
    create_festival_summary()
