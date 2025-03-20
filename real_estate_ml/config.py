from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file if it exists
load_dotenv()

# Get project root directory
PROJ_ROOT = Path(__file__).resolve().parents[1]

# Define data directories
DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Get current date for organizing processed data
CURRENT_DATE = datetime.now().strftime("%Y%m%d")


# Define source-specific directories
def get_processed_dir(source: str) -> Path:
    """Get the processed directory for a specific source and date"""
    return PROCESSED_DATA_DIR / source / CURRENT_DATE


MODELS_DIR = PROJ_ROOT / "models"

REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass
