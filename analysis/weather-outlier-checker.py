import pandas as pd
import numpy as np
from scipy import stats

def check_outliers():
    """
    Checks for outliers in weather metrics using multiple methods:
    1. IQR (Interquartile Range) Method
    2. Z-score Method
    Both methods are used as they have different strengths for outlier detection
    """
    print("Loading weather data...")
    df = pd.read_csv('all_festivals_weather_cleaned.csv')
    
    # Define weather metrics to check
    weather_metrics = ['max_temp_c', 'min_temp_c', 'rainfall_mm', 'max_windspeed_kmh']
    
    # Store results for each metric
    outlier_results = {}
    
    for metric in weather_metrics:
        print(f"\nAnalyzing {metric}:")
        
        # Calculate basic statistics
        mean_val = df[metric].mean()
        median_val = df[metric].median()
        std_val = df[metric].std()
        
        # Method 1: IQR Method
        # Calculate Q1 (25th percentile) and Q3 (75th percentile)
        Q1 = df[metric].quantile(0.25)
        Q3 = df[metric].quantile(0.75)
        IQR = Q3 - Q1
        
        # Define outlier bounds (1.5 * IQR is a common threshold)
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Find outliers using IQR method
        iqr_outliers = df[
            (df[metric] < lower_bound) | 
            (df[metric] > upper_bound)
        ]
        
        # Method 2: Z-score Method
        # Calculate z-scores for the metric
        z_scores = np.abs(stats.zscore(df[metric]))
        
        # Find outliers using z-score method (typically z-score > 3 is considered an outlier)
        z_score_outliers = df[z_scores > 3]
        
        # Store results for this metric
        outlier_results[metric] = {
            'basic_stats': {
                'mean': mean_val,
                'median': median_val,
                'std': std_val,
                'min': df[metric].min(),
                'max': df[metric].max()
            },
            'iqr_bounds': {
                'lower': lower_bound,
                'upper': upper_bound,
                'outliers_count': len(iqr_outliers)
            },
            'z_score_outliers_count': len(z_score_outliers),
            'iqr_outliers': iqr_outliers,
            'z_score_outliers': z_score_outliers
        }
        
        # Print summary for this metric
        print(f"\nBasic Statistics for {metric}:")
        print(f"Mean: {mean_val:.2f}")
        print(f"Median: {median_val:.2f}")
        print(f"Standard Deviation: {std_val:.2f}")
        print(f"Min: {df[metric].min():.2f}")
        print(f"Max: {df[metric].max():.2f}")
        
        print(f"\nIQR Method Results:")
        print(f"Lower bound: {lower_bound:.2f}")
        print(f"Upper bound: {upper_bound:.2f}")
        print(f"Number of outliers: {len(iqr_outliers)}")
        
        print(f"\nZ-score Method Results:")
        print(f"Number of outliers: {len(z_score_outliers)}")
        
        # Print example outliers if any found
        if len(iqr_outliers) > 0:
            print("\nExample IQR outliers:")
            sample_outliers = iqr_outliers.nlargest(5, metric)[
                ['festival_name', 'historical_year', 'calendar_date', metric]
            ]
            print(sample_outliers)
        
        # Save outliers to separate CSV files
        if len(iqr_outliers) > 0:
            iqr_filename = f'outliers_{metric}_iqr.csv'
            iqr_outliers.to_csv(iqr_filename, index=False)
            print(f"\nIQR outliers saved to: {iqr_filename}")
        
        if len(z_score_outliers) > 0:
            z_filename = f'outliers_{metric}_zscore.csv'
            z_score_outliers.to_csv(z_filename, index=False)
            print(f"\nZ-score outliers saved to: {z_filename}")
    
    # Print overall summary
    print("\nOverall Summary:")
    print("=" * 50)
    for metric in weather_metrics:
        print(f"\n{metric}:")
        print(f"IQR Outliers: {outlier_results[metric]['iqr_bounds']['outliers_count']}")
        print(f"Z-score Outliers: {outlier_results[metric]['z_score_outliers_count']}")
        
        # Calculate percentage of outliers
        total_records = len(df)
        iqr_pct = (outlier_results[metric]['iqr_bounds']['outliers_count'] / total_records) * 100
        z_pct = (outlier_results[metric]['z_score_outliers_count'] / total_records) * 100
        print(f"IQR Outlier Percentage: {iqr_pct:.2f}%")
        print(f"Z-score Outlier Percentage: {z_pct:.2f}%")

if __name__ == "__main__":
    check_outliers()
