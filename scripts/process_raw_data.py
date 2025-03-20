from pathlib import Path

from real_estate_ml.config import get_processed_dir
from real_estate_ml.processing.raw_data_processor import RawDataProcessor


def main():
    # Define paths
    project_root = Path(__file__).parents[1]
    raw_data_dir = project_root / "data" / "raw" / "olx"
    
    # Create processor
    processor = RawDataProcessor(raw_data_dir)
    
    # Get processed directory for OLX
    processed_dir = get_processed_dir("olx")
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Save as Parquet (best for ML pipelines)
    processor.save_processed_data(
        processed_dir / "listings.parquet",
        format="parquet"
    )
    
    # Also save as CSV for easy viewing
    processor.save_processed_data(
        processed_dir / "listings.csv",
        format="csv"
    )


if __name__ == "__main__":
    main()
