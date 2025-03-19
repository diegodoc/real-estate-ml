# Project Structure

This project follows the [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/) template for better organization and reproducibility.

## Directory Structure
- `data/` - Data files separated into raw, processed, interim, and external
- `real_estate_ml/` - Source code package
- `notebooks/` - Jupyter notebooks for exploration
- `models/` - Trained model files
- `reports/` - Generated analysis reports and figures
- `docs/` - Project documentation

## Code Organization
- `dataset.py` - Data processing pipeline
- `features.py` - Feature engineering functions
- `modeling/` - Model training and prediction
- `plots.py` - Visualization utilities
- `config.py` - Configuration and path settings
- `utils/` - Helper functions and utilities

## Data Pipeline
1. Raw data collection (`data/raw/`)
2. Initial processing (`dataset.py`)
3. Feature engineering (`features.py`)
4. Model training (`modeling/train.py`)
5. Predictions (`modeling/predict.py`)
5. Visualize results with `plots.py`
