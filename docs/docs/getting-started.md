Getting Started
===============

This guide will help you set up and run the Real Estate ML project from a clean installation.

Prerequisites
------------
- Anaconda or Miniconda (recommended)
- Git
- Make (build automation tool)

Initial Setup
------------
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd real-estate-ml
   ```

2. Create and activate Conda environment:
   ```bash
   make create_environment
   conda activate real-estate-ml
   ```

3. Install Python dependencies:
   ```bash
   make requirements
   ```

4. Set up environment variables if needed:
   - Copy `.env.example` to `.env`
   - Edit `.env` with your configuration

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

## Data Collection and Processing

### 1. Collecting OLX Listing IDs
Before running the scraper, you need to manually collect some listing IDs:

1. Go to OLX's real estate section: https://www.olx.com.br/imoveis
2. Open any property listing that interests you
3. In the URL, locate the 10-digit listing ID. For example:
   ```
   https://www.olx.com.br/d/imoveis/apartamento-exemplo-1387432094
                                                       └─── ID ───┘
   ```
4. Open `real_estate_ml/scraping/collectors/olx_collector.py`
5. Update the `listing_ids` list with your collected IDs:
   ```python
   listing_ids = [
       "1387432094",  # Your first listing ID
       "1367766557",  # Another listing ID
       # Add more IDs...
   ]
   ```

### 2. Running the Scraper
After collecting listing IDs:

1. Collect data from OLX:
   ```bash
   make scrape-olx
   ```
   This will save raw data in `data/raw/olx/YYYYMMDD_HHMMSS/listings/`

2. Process the collected data:
   ```bash
   make process-olx
   ```
   This creates processed files in `data/processed/olx/YYYYMMDD/`

3. View the processed data:
   - Use `listings.csv` for quick data inspection
   - Use `listings.parquet` for ML pipelines

### Tips
- Collect IDs from different neighborhoods to get a diverse dataset
- The scraper will automatically collect related listings from each ID you provide
- Avoid collecting too many IDs at once to prevent rate limiting
- Space out your collection runs to avoid detection

Development
----------
- Format code:
  ```bash
  make format
  ```

- Check code style:
  ```bash
  make lint
  ```

- Clean compiled Python files:
  ```bash
  make clean
  ```

- Update conda environment:
  ```bash
  make update_environment
  ```

Documentation
------------
To view the documentation locally:
```bash
mkdocs serve
```
Then visit http://127.0.0.1:8000 in your browser.

Available Commands
----------------
View all available make commands:
```bash
make help
Then visit http://127.0.0.1:8000 in your browser.
