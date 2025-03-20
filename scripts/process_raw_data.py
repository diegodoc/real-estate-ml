import argparse
from pathlib import Path

from real_estate_ml.config import get_processed_dir
from real_estate_ml.processing.raw_data_processor import RawDataProcessor
from real_estate_ml.processing.zap_processor import ZapDataProcessor


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Process raw data from different sources')
    parser.add_argument('--source', type=str, required=True, choices=['olx', 'zap'],
                      help='Source of the raw data (olx or zap)')
    args = parser.parse_args()
    
    # Define paths
    project_root = Path(__file__).parents[1]
    raw_data_dir = project_root / "data" / "raw" / args.source
    
    # Create appropriate processor based on source
    if args.source == 'olx':
        processor = RawDataProcessor(raw_data_dir)
    else:  # zap
        processor = ZapDataProcessor(raw_data_dir)
    
    # Get processed directory
    processed_dir = get_processed_dir(args.source)
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Process the data
    processor.process_raw_data()
    
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

