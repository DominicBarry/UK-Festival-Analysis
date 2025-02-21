# UK Festival Analysis
A comprehensive analysis of 206 UK festivals combining web scraping, data engineering, and weather analysis to create interactive visualizations.

## Skills Demonstrated
- Web Scraping & Data Collection
- Data Cleaning & Transformation
- API Integration
- Statistical Analysis
- Geographic Data Processing
- Data Visualization

## Overview
An analysis of UK festivals in 2025, demonstrating end-to-end data analysis capabilities. The project combines festival data scraped from the internet with 30 years of historical weather data to provide insights into the UK festival landscape and predict optimal festival experiences based on historical weather patterns.

## Tools Used
- Data Collection: Screaming Frog
- Data Processing: Google Sheets, Python (Pandas, NumPy, SciPy)
- API Integration: Open-Meteo Weather API
- Development: R Studio
- Visualization: Tableau

## Getting Started

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

### Data Processing Scripts
The analysis folder contains Python scripts to be run in RStudio in the following sequence:

1. `historical-weather.py`
   - Input: festivals.csv (contains festival details with lat/long)
   - Output: all_festivals_historical_weather.csv
   - Purpose: Collects 30 years of weather data for each festival location via Open-Meteo API

2. `weather-data-validator-detailed.py'
   - Input: all_festivals_historical_weather.csv
   - Output: Processed weather data ready for analysis
   - Purpose: Initial processing of raw weather data

3. `festival-weather-summary-5mm.py`
   - Input: Processed weather data
   - Output: festival_weather_comparison.csv
   - Purpose: Creates final weather metrics, including:
     - Festival Weather Score based on standardized measurements
     - Rainfall analysis (counting days with >5mm as rain days)
     - Temperature and wind statistics

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

## Key Insights
- Market Analysis:
  - Mixed/general is the leading genre with 63 festivals (1.3 million capacity)
  - July hosts most festivals (76), but August has highest capacity (885k)
  - South East England leads with 34 festivals (580k capacity)
  - Typical festival duration is 3 days

- Weather Analysis:
  - Driest: Cross the Tacks (3.3% chance of significant rainfall)
  - Most Stable Wind: Home of the Drum (16.8kmh avg. max wind)
  - Warmest: Jazz Cafe Festival (14.3C-22.4C temperature range)
  - Best Overall Weather: Tolpuddle Martyrs Festival and Rally

## Visualizations
Interactive Tableau dashboards presenting market and weather insights:

![Festivals Overview Dashboard](visualizations/festivals-dashboard.png)
*Dashboard 1: UK Festival Market Analysis 2025*

![Weather Analysis Dashboard](visualizations/weather-dashboard.png)
*Dashboard 2: Historical Weather Analysis by Festival Location*

[View Interactive Dashboards on Tableau Public ↗](https://public.tableau.com/app/profile/dom.barry/viz/UKFestivalAnalysis2025/FestivalAnalysis)
