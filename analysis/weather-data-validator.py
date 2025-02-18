import pandas as pd
from datetime import datetime

def check_data_completeness():
    """
    Validates completeness of weather data against festival list
    """
    print("Loading data files...")
    # Load both datasets
    festivals = pd.read_csv('festivals.csv')
    weather = pd.read_csv('all_festivals_weather_cleaned.csv')
    
    print(f"\nChecking completeness for {len(festivals)} festivals...")
    
    # Initialize results storage
    missing_data = []
    duplicate_data = []
    other_issues = []
    
    # Check each festival
    for _, festival in festivals.iterrows():
        festival_id = festival['ID']
        festival_name = festival['Title']
        
        # Get festival's weather data
        festival_weather = weather[weather['festival_id'] == festival_id]
        
        # Check for each year (1995-2024)
        years_present = festival_weather['historical_year'].unique()
        if len(years_present) != 30:
            missing_years = set(range(1995, 2025)) - set(years_present)
            if missing_years:
                missing_data.append({
                    'festival_id': festival_id,
                    'festival_name': festival_name,
                    'issue': f"Missing years: {sorted(missing_years)}"
                })
        
        # Check for duplicates
        duplicates = festival_weather.groupby(['historical_year', 'calendar_date']).size()
        duplicate_dates = duplicates[duplicates > 1]
        if not duplicate_dates.empty:
            duplicate_data.append({
                'festival_id': festival_id,
                'festival_name': festival_name,
                'issue': f"Duplicate dates found: {duplicate_dates.index.tolist()}"
            })
        
        # Check data completeness
        start_date = pd.to_datetime(festival['startDate'], format='%d/%m/%Y')
        end_date = pd.to_datetime(festival['endDate'], format='%d/%m/%Y')
        expected_days = (end_date - start_date).days + 1
        
        # Check each year has the correct number of days
        for year in years_present:
            year_data = festival_weather[festival_weather['historical_year'] == year]
            if len(year_data) != expected_days:
                other_issues.append({
                    'festival_id': festival_id,
                    'festival_name': festival_name,
                    'issue': f"Year {year}: Found {len(year_data)} days, expected {expected_days}"
                })
    
    # Print results
    print("\nData Completeness Check Results:")
    print("-" * 50)
    
    if missing_data:
        print("\nFestivals with Missing Years:")
        for issue in missing_data:
            print(f"Festival {issue['festival_id']} ({issue['festival_name']}): {issue['issue']}")
    else:
        print("\nNo missing years found!")
        
    if duplicate_data:
        print("\nFestivals with Duplicate Data:")
        for issue in duplicate_data:
            print(f"Festival {issue['festival_id']} ({issue['festival_name']}): {issue['issue']}")
    else:
        print("\nNo duplicate data found!")
        
    if other_issues:
        print("\nOther Data Issues:")
        for issue in other_issues:
            print(f"Festival {issue['festival_id']} ({issue['festival_name']}): {issue['issue']}")
    else:
        print("\nNo other issues found!")
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Total festivals checked: {len(festivals)}")
    print(f"Total weather records: {len(weather)}")
    print(f"Festivals with missing data: {len(missing_data)}")
    print(f"Festivals with duplicates: {len(duplicate_data)}")
    print(f"Festivals with other issues: {len(other_issues)}")
    
    # Check for any null values in important columns
    null_counts = weather.isnull().sum()
    if null_counts.any():
        print("\nNull Values Found:")
        print(null_counts[null_counts > 0])
    else:
        print("\nNo null values found in the dataset!")

if __name__ == "__main__":
    check_data_completeness()
