# Data Processing

This document outlines the steps taken to process the raw Titanic dataset.

## Data Acquisition
The Titanic dataset is obtained from [source] and stored in the `data/raw/` directory.

## Data Cleaning
The following cleaning steps are performed:
- Handling missing values in Age, Cabin, and Embarked columns
- Converting categorical variables to numerical format
- Feature engineering (e.g., extracting titles from names)

## Feature Engineering
New features created include:
- Family size (combining siblings/spouses and parents/children)
- Age groups
- Fare categories
- Title extraction from passenger names

## Data Transformation
The processed dataset is stored in `data/processed/` and includes:
- Normalized numerical features
- One-hot encoded categorical features
- Train/test split for model evaluation