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
