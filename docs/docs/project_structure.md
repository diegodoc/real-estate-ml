# Project Structure

This project follows the [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/) template for better organization and reproducibility.

## Directory Structure
- `data/` - Data files separated into raw, processed, interim, and external
- `titanic_ml/` - Source code package
- `notebooks/` - Jupyter notebooks for exploration
- `models/` - Trained model files
- `reports/` - Generated analysis reports and figures
- `docs/` - Project documentation

## Code Organization
- `dataset.py` - Data processing pipeline
- `features.py` - Feature engineering functions
- `modeling/` - Model training and prediction
- `plots.py` - Visualization utilities

## Workflow
1. Process raw data with `dataset.py`
2. Engineer features with `features.py`
3. Train models with `modeling/train.py`
4. Generate predictions with `modeling/predict.py`
5. Visualize results with `plots.py`