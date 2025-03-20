# Project Structure

This project follows the [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/) template for better organization and reproducibility.

## Directory Structure
- `data/` - Data files separated into raw, processed, interim, and external
  - `raw/` - Original, immutable data
    - `olx/` - Raw data from OLX
      - `YYYYMMDD_HHMMSS/` - Timestamped collection runs
        - `listings/` - JSON files for each listing
  - `processed/` - Cleaned, transformed data ready for analysis
    - `olx/` - Processed OLX data
      - `YYYYMMDD/` - Date-organized processed data
        - `listings.parquet` - Parquet format for ML pipelines
        - `listings.csv` - CSV format for easy viewing
- `real_estate_ml/` - Source code package
  - `scraping/` - Web scraping modules
    - `olx_api_collector.py` - OLX API data collector
  - `processing/` - Data processing modules
  - `config.py` - Configuration and path settings
- `notebooks/` - Jupyter notebooks for exploration
- `models/` - Trained model files
- `reports/` - Generated analysis reports and figures
- `docs/` - Project documentation

## Data Pipeline
1. Raw data collection (`make scrape-olx`)
2. Initial processing (`make process-olx`)
3. Feature engineering (`features.py`)
4. Model training (`modeling/train.py`)
5. Predictions (`modeling/predict.py`)
6. Visualize results with `plots.py`


