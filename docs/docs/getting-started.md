Getting Started
===============

This guide will help you set up and run the Titanic ML project from a clean installation.

Prerequisites
------------
- Python 3.10
- pip (Python package manager)
- Make (build automation tool)
- Git
- Kaggle account (for downloading the dataset)

For Windows Users:
- Install Make from [GnuWin32](http://gnuwin32.sourceforge.net/packages/make.htm) or using [Chocolatey](https://chocolatey.org/): `choco install make`
- For Unix-like environment, consider using [Git Bash](https://gitforwindows.org/) or WSL

Initial Setup
------------
1. Clone the repository

2. Create and activate a virtual environment:

   Option 1: Using venv (recommended)
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate the environment
   # On Windows:
   .venv\Scripts\activate
   # On Unix or MacOS:
   source .venv/bin/activate
   ```

   Option 2: Using virtualenvwrapper (requires additional setup)
   ```bash
   # First install virtualenvwrapper
   pip install virtualenvwrapper
   
   # Then create and activate environment
   make create_environment
   workon titanic-ml
   ```

3. Install dependencies:
   ```bash
   make requirements
   ```

Data Setup
----------
1. Download the Titanic dataset from Kaggle:
   - Visit [Kaggle's Titanic Competition](https://www.kaggle.com/c/titanic/data?select=test.csv)
   - Sign in to your Kaggle account
   - Download `train.csv` and `test.csv`

2. Place the downloaded files in `data/raw/`:
   ```
   data/
   └── raw/
       ├── train.csv
       └── test.csv
   ```

3. Process the raw data into cleaned datasets:
   ```bash
   make data
   ```
   This command runs the data processing pipeline defined in `titanic_ml/dataset.py`

Running the Pipeline
------------------
Run these commands in sequence:

1. Process the dataset:
   ```bash
   make data
   ```

2. Generate features:
   ```bash
   python titanic_ml/features.py
   ```

3. Train the model:
   ```bash
   python titanic_ml/modeling/train.py
   ```

4. Generate predictions:
   ```bash
   python titanic_ml/modeling/predict.py
   ```

5. Create visualizations:
   ```bash
   python titanic_ml/plots.py
   ```

Documentation
------------
To view the documentation locally:
```bash
mkdocs serve
```
Then visit http://127.0.0.1:8000 in your browser.
