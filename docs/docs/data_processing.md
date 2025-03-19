# Data Processing

This document outlines the steps taken to process the real estate dataset.

## Data Acquisition
The real estate dataset is collected from various sources and stored in the `data/raw/` directory.

## Data Cleaning
The following cleaning steps are performed:
- Handling missing values in property features
- Converting categorical variables to numerical format
- Standardizing price formats and currencies
- Normalizing area measurements
- Cleaning and standardizing location data

## Feature Engineering
New features created include:
- Price per square meter/foot
- Property age (from year built)
- Location-based features (neighborhood scores, proximity to amenities)
- Text features from descriptions (keyword extraction, sentiment analysis)
- Image features (architectural style, condition assessment)
- Amenity counts and categories
