# UK Festival Analysis
A comprehensive analysis of 206 UK festivals in 2025, combining web scraped festival data with 30 years of historical weather patterns to provide insights and predict optimal festival experiences through interactive visualizations.

## Overview

- Festival info scraped from the internet, extracted, cleaned, augmented, geocoded
- Geocoded weather data sourced from Open-Meteo.com
- Screaming Frog, Google Sheets, Geocoding by SmartMonkey, Claude.ai, R, Python & Tableau used
- It was then imported into Tableau & augmented with calculated fields to support further analysis

## Data Structure

The database structure as seen below consists of 3 tables, 'UK Festivals', 'Weather Data' and 'Weather Comparison':

![ERD Diagram for UK Festival Analysis](visualizations/ERD-diagram.png)

The steps taken to process the data prior to analysis in Tableau can be found [here](documentation/data-prep-summary.md).

## Methodology

- Web Scraping & Data Collection
- Data Cleaning & Transformation
- API Integration
- Statistical Analysis
- Geographic Data Processing
- Data Visualization using Tableau

## Tools Used

- Data Collection: Screaming Frog
- Data Processing: Google Sheets, Python (Pandas, NumPy, SciPy)
- API Integration: Open-Meteo Weather API
- Development: R Studio
- Visualization: Tableau

## Dashboard Structure

### 1. Festival Market Overview Dashboard

#### Key Metrics (BANs)

- **Total festivals** (206)
- **Average duration** (3 days)
- **Average capacity** (14,239)

#### Market Segmentation Visualizations

- **Top Genres** treemap showing distribution by count/capacity
- **UK Map** showing geographic distribution of festivals with size/color indicating capacity
- **Country breakdown** bar chart by count/capacity
- **Top Regions** bar chart by count/capacity
- **Month distribution** bar chart by count/capacity
- **Duration distribution** sbar chart by count/capacity
- **Top Festivals** by capacity bar chart

### 2. Weather Analysis Dashboard

#### Filter Controls
- **Region dropdown** for geographic filtering
- **Music Genre dropdown** for genre-specific analysis
- **Search by Festival Name text field** for festival-specific analysis
- **Month slider** for temporal filtering

#### Weather Metric Comparisons
- **Wettest Festivals** bar chart showing rainfall probability
- **Driest Festivals** bar chart showing minimal rainfall chance
- **Windiest Festivals** bar chart showing average max windspeed
- **Least Windy Festivals** bar chart

#### Temperature Analysis
- **Warmest Festivals** dot plot showing min/max temperature ranges
- **Coldest Festivals** dot plot showing min/max temperature ranges

#### Summary Metrics
- **Festival Weather Score** bar chart ranking overall weather quality
- **Weather Map** showing geographic distribution of festivals with color-coded weather scores

## Key Findings

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

## How to view the dashboard

![Festivals Overview Dashboard](visualizations/festivals-dashboard.png)
*Dashboard 1: UK Festival Market Analysis 2025*

![Weather Analysis Dashboard](visualizations/weather-dashboard.png)
*Dashboard 2: Historical Weather Analysis by Festival Location*

[View Interactive Dashboards on Tableau Public ↗](https://public.tableau.com/app/profile/dom.barry/viz/UKFestivalAnalysis2025/FestivalAnalysis)

## Caveats & Assumptions

Festival specifc information was scraped from 3rd party sites on the internet & is not guaranteed to be reliable but does provide a reasonable data set for analysis. It would be very interesting to repeat this analysis using first party data from industry bodies and/or licensing authorities.