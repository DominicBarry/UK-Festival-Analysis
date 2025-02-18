# UK Festival Analysis

## Overview
An analysis of UK festivals in 2025, a Tableau dashboard project for my data portfolio to demonstrate the skills I've acquired during my data training. I scraped the details for 206 UK festivals from the internet, cleaned, augmented & geocoded them. I then built a Tableau dashboard that shows insights into music genre, country, region, month and duration by capacity/festival count. For fun I augmented my festival dataset with 30 years worth of historical weather data for each location to attempt to show at a top level which festivals are likely to have the best weather. 

## Tools Used
- Screaming Frog
- Google Sheets
  - Geocoding by SmartMonkey
  - Regex
- R Studio
- Python
  - Pandas
  - Requests
  - Time
  - Numpy
  - Spciy.stats
- Tableau

## Project Structure
- **Data cleaning and preparation**
  - Scrape festival details from efestivals.co.uk with Screaming Frog using custom extracts
  - Export crawl data as CSV
  - Import to Google Sheets
  - Use regex to extract the following data points:
    - Title
    - Venue
    - streetAddress
    - addressLocality
    - postalCode
    - Country
    - Capacity
    - Start/end dates
  - Clean using 'data clean up' in Google Sheets (trim white space)
  - Manual review & filter down to just outdoor festivals in England, Wales, Scotland & Northern Ireland
  - Augment data by adding the following fields to support analysis:
    - Category (claude.ai used followed by manual review to check & fill any gaps)
    - Duration (google sheets formula)
    - Camping (manual checks)
    - Region (Google Apps Script)
    - Music genre (claude.ai used followed by manual review to check & fill any gaps)
  - Review for gaps, outliers & duplicates
    - Geocode lat, long values based on postcode using "Geocoding by SmartMonkey" extension for Google Sheets
    - Export as CSV festivals_25_cleaned.csv
  - Weather Data
    - Create historical-weather.py python script to pull 30 years of weather data for each festival 206 festivals:
      - Script input data added to festivals.csv:
        - ID
        - Title
        - startDate
        - endDate
        - lat
        - long
      - Data Collection Steps:
        - Set up python environment within R Studio
        - Use historical-weather.py script to collect data from Open-Meteo.com API
        - Range: 1995-2024 (30 years)
        - Daily weather data for each festival's dates
      - After Collection:
        - Check data completeness
        - Check for outliers
        - Create festival-weather-summary-5mm.py script to aggregate weather metrics at festival level:
          - 'Festival Weather Score' to represent overall conditions based on standardized measurements (z-scores)
          - pct_rain_days based on days where rainfall per day > 5mm:
        - Export agregated festival data to festival_weather_comparison.csv, containing:
          - festival_name
          - mean_max_temp
          - mean_min_temp
          - overall_max_temp
          - overall_min_temp
          - temp_std_dev
          - total_rain_day
          - total_days
          - pct_rain_days
          - avg_daily_rainfall
          - max_daily_rainfall
          - mean_max_wind
          - overall_max_wind
          - wind_std_dev
          - temp_z
          - rain_z
          - wind_z
          - weather_score
      - Output Files Created:
        - all_festivals_historical_weather.csv (daily details)
        - festival_weather_comparison.csv (aggreated by festival)
          
- **Analysis performed**
  - Analyse music genre, country, region, month, duration by capacity/festival count
  - Analyse top 10 festivals by capacity
  - Analyse top wettest/driest festivals
  - Analyse top windiest/least windy festivals
  - Analyse top Warmest/Coldest festivals
  - Analyse top festivals Weather Score

- **Key findings**
  - Mixed/general is most the popular music genre by count of festivals (63) & capacity (1.3 million)
  - July is the most popular month by count of festival (76) however August is the most popular by capacity (885k)
  - The South East of England is the most popular region by count of festivals (34) & capacity (580k)
  - 3 days is the most popular length by count of festivals & capacity
  - Based on 30 years of weather data:
    - Cross the Tacks is the driest festival with a 3.3% chance of > 5mm rain per day
    - Home of the Drum is the least windy festival with an avg. max wind speed of 16.8kmh
    - Jazz Cafe Festival is the warmest festival with avg. min/max temperature range of 14.3C to 22.4C
    - Tolpuddle Martyrs Festival and Rally has the best weather score of all 206 festivala
## Visualizations
Two interactive Tableau dashboards were created to present the analysis:
![Festivals Overview Dashboard](visualizations/festivals-dashboard.png)
*Dashboard 1: Overview of UK festival market in 2025*

![Weather Analysis Dashboard](visualizations/weather-dashboard.png)
*Dashboard 2: Top level festival weather analysis based 30 years worth of historical weather data for each location*
## Results
Summary of your key findings and link to your Tableau dashboard
