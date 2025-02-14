# UK-Festival-Analysis
Analysis of the UK festival market &amp; weather

## Overview
Brief description of your data analysis project

## Tools Used
- Screaming Frog
- Google Sheets
- Geocoding by SmartMonkey
- Claude.ai
- R
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
  - Use regex to extractthe following data points:
      - Title
      - Venue
      - streetAddress
      - addressLocality
      - postalCode
      - Country
      - Capacity
      - Start/end dates
  - Clean using 'data clean up' in Google Sheets (trim white space)
  - Augment data by adding the following fields to support analysis:
      - Category (claude.ai used followed by manual review to check & fill any gaps)
      - Duration (google sheets formula)
      - Camping (manual checks)
      - Region (Google Apps Script)
      - Music genre (claude.ai used followed by manual review to check & fill any gaps)
  - Filter so we only get outdoor festivals in England, Wales, Scotland & Northern Ireland
  - Review for gaps, outliers & duplicates
  - Geo code lat, long values based on postcode using "Geocoding by SmartMonkey" extension for Google Sheets
  - Export as CSV

- **Analysis performed**
- For 206 festivals in 2025:
  - Analyse music genre, country, region, month, duration by capcity/festival count
  - Analyse top 10 festivals by capacity
- For weather

- 
- **Key findings**
  - xxx
  - xxx
  - xxx

- Visualizations created
- 

## Results
Summary of your key findings and link to your Tableau dashboard
