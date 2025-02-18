import pandas as pd
from datetime import datetime
from collections import defaultdict

def check_data_completeness():
    """
    Enhanced validation of weather data completeness with detailed reporting
    """
    print("Loading data files...")
    festivals = pd.read_csv('festivals.csv')
    weather = pd.read_csv('all_festivals_weather_cleaned.csv')
    
    print(f"\nChecking completeness for {len(festivals)} festivals...")
    
    # Initialize results storage
    missing_data = []
    duplicate_data = []
    other_issues = []
    festival_issue_count = defaultdict(int)
    
    # Track specific details about duplicates
    duplicate_details = []
    
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
                festival_issue_count[festival_name] += 1
        
        # Check for duplicates with detailed information
        duplicates = festival_weather.groupby(['historical_year', 'calendar_date']).size()
        duplicate_dates = duplicates[duplicates > 1]
        if not duplicate_dates.empty:
            # Get detailed information about duplicates
            for (year, date), count in duplicate_dates.items():
                duplicate_rows = festival_weather[
                    (festival_weather['historical_year'] == year) & 
                    (festival_weather['calendar_date'] == date)
                ]
                duplicate_details.append({
                    'festival_id': festival_id,
                    'festival_name': festival_name,
                    'year': year,
                    'date': date,
                    'count': count,
                    'records': duplicate_rows.to_dict('records')
                })
            
            duplicate_data.append({
                'festival_id': festival_id,
                'festival_name': festival_name,
                'issue': f"Duplicate dates found: {duplicate_dates.index.tolist()}"
            })
            festival_issue_count[festival_name] += 1
        
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
                    'year': year,
                    'found_days': len(year_data),
                    'expected_days': expected_days,
                    'dates_present': sorted(year_data['calendar_date'].tolist())
                })
                festival_issue_count[festival_name] += 1
    
    # Print detailed results
    print("\nDetailed Data Completeness Check Results:")
    print("=" * 80)
    
    if missing_data:
        print("\nFestivals with Missing Years:")
        print("-" * 50)
        for issue in missing_data:
            print(f"Festival {issue['festival_id']} ({issue['festival_name']}): {issue['issue']}")
    else:
        print("\nNo missing years found!")
        
    if duplicate_data:
        print("\nFestivals with Duplicate Data:")
        print("-" * 50)
        print(f"\nFound {len(duplicate_details)} duplicate date instances across {len(duplicate_data)} festivals:")
        for detail in duplicate_details:
            print(f"\nFestival: {detail['festival_name']} (ID: {detail['festival_id']})")
            print(f"Year: {detail['year']}, Date: {detail['date']}")
            print(f"Number of duplicates: {detail['count']}")
            # Compare duplicate records
            records = detail['records']
            if len(records) > 1:
                print("Duplicate Records Comparison:")
                for field in ['max_temp_c', 'min_temp_c', 'rainfall_mm', 'max_windspeed_kmh']:
                    values = [r[field] for r in records]
                    if len(set(values)) > 1:
                        print(f"  {field}: {values} (Values differ!)")
    else:
        print("\nNo duplicate data found!")
        
    if other_issues:
        print("\nDay Count Issues:")
        print("-" * 50)
        issues_by_pattern = defaultdict(list)
        for issue in other_issues:
            pattern = f"Expected {issue['expected_days']} days, found {issue['found_days']}"
            issues_by_pattern[pattern].append(issue)
        
        print("\nIssues grouped by pattern:")
        for pattern, issues in issues_by_pattern.items():
            print(f"\n{pattern} ({len(issues)} instances):")
            for issue in issues[:5]:  # Show first 5 examples
                print(f"- {issue['festival_name']} (Year: {issue['year']})")
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more instances")
    
    # Print festivals with multiple issues
    print("\nFestivals with Multiple Issues:")
    print("-" * 50)
    multi_issue_festivals = {k: v for k, v in festival_issue_count.items() if v > 1}
    if multi_issue_festivals:
        for festival, count in sorted(multi_issue_festivals.items(), key=lambda x: x[1], reverse=True):
            print(f"{festival}: {count} issues")
    else:
        print("No festivals have multiple issues")
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print("=" * 50)
    print(f"Total festivals checked: {len(festivals)}")
    print(f"Total weather records: {len(weather)}")
    print(f"Festivals with missing data: {len(missing_data)}")
    print(f"Festivals with duplicates: {len(duplicate_data)}")
    print(f"Total duplicate instances: {len(duplicate_details)}")
    print(f"Festivals with day count issues: {len(set(i['festival_name'] for i in other_issues))}")
    print(f"Total day count issues: {len(other_issues)}")
    print(f"Festivals with multiple issues: {len(multi_issue_festivals)}")
    
    # Check for any null values in important columns
    null_counts = weather.isnull().sum()
    if null_counts.any():
        print("\nNull Values Found:")
        print(null_counts[null_counts > 0])
    else:
        print("\nNo null values found in the dataset!")

if __name__ == "__main__":
    check_data_completeness()
