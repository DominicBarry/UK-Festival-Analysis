# Data preparation and cleaning

## Data source & summary

- Festival info scraped from the internet, extracted, cleaned, augmented, geocoded
- Geocoded weather data sourced from Open-Meteo.com

## Data Processing Methodology

1. **Data Collection & Cleaning**
   - Scraped festival details using Screaming Frog with custom extracts
   - Processed raw data using regex to extract key data points
   - Geocoded locations using SmartMonkey
   - Augmented dataset with AI-assisted categorization (validated manually)

2. **Weather Data Integration**
   - Developed Python scripts to collect 30 years of historical weather data
   - Created aggregated weather metrics and scoring system
   - Generated comprehensive weather analysis per festival

### Data Processing Scripts

The analysis folder contains Python scripts to be run in RStudio in the following sequence:

1. [`historical-weather.py`](../analysis/historical-weather.py)
   - Input: festivals.csv (contains festival details with lat/long)
   - Output: Output: Checkpoint files and combined weather data
   - Purpose: Collects 30 years of weather data for each festival location via Open-Meteo API

2. [`weather-data-validator-detailed.py`](../analysis/weather-data-validator-detailed.py) (optional, for data validation)
   - Input: all_festivals_historical_weather.csv
   - Output: Validation report (console output)
   - Purpose: Checks for missing data, duplicates, and other data quality issues
   
3. [`weather-outlier-checker.py`](../analysis/weather-outlier-checker.py) (optional, for outlier detection)
   - Input: all_festivals_historical_weather.csv
   - Output: Outlier reports and CSV files
   - Purpose: Identifies statistical outliers in weather metrics   

4. [`festival-weather-summary-5mm.py`](../analysis/festival-weather-summary-5mm.py)
   - Input: Processed weather data
   - Output: festival_weather_comparison.csv
   - Purpose: Creates final weather metrics, including:
     - Festival Weather Score based on standardized measurements
     - Rainfall analysis (counting days with >5mm as rain days)
     - Temperature and wind statistics
   
### Prerequisites

- RStudio
- Python 3.12.7
- pip (Python package installer)
- reticulate (R package for Python integration)

### Environment Setup

1. Clone the repository
   ```bash
   git clone https://github.com/DominicBarry/UK-Festival-Analysis.git
   ```
2. Open RStudio
3. Configure Python within RStudio:
   - Tools → Global Options → Python
   - RStudio uses reticulate virtual environment at:
     `/Users/DomBarry/.virtualenvs/r-reticulate/bin/python3`
   - Install required packages:
     ```bash
     pip install -r requirements.txt
     ```

## Sample Data ?????

- [Sample Cleaned Dataset (100 rows)](../data-cleaning/cleaned-data/leeds_cycle_counts_sample.csv) - Representative sample of the full cleaned dataset


## Summary & Caveats

- 30 years of geocoded weather data sourced from from Open-Meteo.com for 206 UK festivals due to take place in 2025.
- Aggregate Rainfall, Wind and Temperature calculated for each festival based on historical data for each location.
- Festival Weather Score represents overall conditions based on standardized measurements (z-scores) of key weather factors.
- It combines temperature favorability while accounting for disruptive elements: Score = Temperature Z-score - (Wind Z-score + Rain Z-score).
- Higher scores indicate better festival weather conditions.
