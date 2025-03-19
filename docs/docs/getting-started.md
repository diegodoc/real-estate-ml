Getting Started
===============

This guide will help you set up and run the Real Estate ML project from a clean installation.

Prerequisites
------------
- Python 3.10
- pip (Python package manager)
- Make (build automation tool)
- Git

Initial Setup
------------
1. Clone the repository
2. Install dependencies: `make requirements`
3. Set up environment variables if needed

Data Setup
----------
1. Prepare your real estate dataset:
   - Collect property listings data
   - Gather property images
   - Download or scrape property descriptions
   - Organize location data

2. Place the data files in `data/raw/`:
   ```
   data/
   └── raw/
       ├── listings.csv
       ├── images/
       └── descriptions.csv
   ```

3. Process the raw data:
   ```bash
   make data
   ```

Running the Pipeline
------------------
Run these commands in sequence:

1. Process the dataset:
   ```bash
   make data
   ```

2. Generate features:
   ```bash
   python real_estate_ml/features.py
   ```

3. Train the model:
   ```bash
   python real_estate_ml/modeling/train.py
   ```

4. Generate predictions:
   ```bash
   python real_estate_ml/modeling/predict.py
   ```

5. Create visualizations:
   ```bash
   python real_estate_ml/plots.py
   ```

Documentation
------------
To view the documentation locally:
```bash
mkdocs serve
```
Then visit http://127.0.0.1:8000 in your browser.
