# Project Overview

## Dataset
This project now uses a public housing dataset instead of scraped data. The original regression dataset has been adapted for classification tasks by:
- Converting continuous price values into discrete categories
- Focusing on property classification rather than price prediction
- Using existing features to predict property categories

## Previous Approach
The project originally used web scraping to collect data from real estate websites. This code has been preserved in the `legacy_scrapers/` directory for reference.

## Current Approach
We now use a public dataset which offers several advantages:
- Reliable, clean data
- No dependency on web scraping
- Faster development cycle
- More focus on model development
