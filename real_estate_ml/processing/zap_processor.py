import json
from pathlib import Path

from loguru import logger
import pandas as pd


class ZapDataProcessor:
    def __init__(self, raw_data_dir: Path):
        self.raw_data_dir = raw_data_dir
        self.processed_data = None

    def process_listing(self, data: dict) -> dict:
        """Process a single listing data"""
        try:
            return {
                "listing_id": data.get("id"),
                "title": data.get("title"),
                "price": data.get("price"),
                "address": data.get("address", {}).get("full"),
                "neighborhood": data.get("address", {}).get("neighborhood"),
                "city": data.get("address", {}).get("city"),
                "state": data.get("address", {}).get("state"),
                "area": data.get("usableArea"),
                "bedrooms": data.get("bedrooms"),
                "bathrooms": data.get("bathrooms"),
                "parking_spaces": data.get("parkingSpaces"),
                "property_type": data.get("propertyType"),
                "listing_type": data.get("listingType"),  # sale or rent
                "created_at": data.get("createdAt"),
                "updated_at": data.get("updatedAt"),
            }
        except Exception as e:
            logger.error(f"Error processing listing: {e}")
            return None

    def process_raw_data(self):
        """Process all raw data files"""
        processed_listings = []

        # Find all JSON files in raw data directory
        json_files = list(self.raw_data_dir.rglob("*.json"))
        logger.info(f"Found {len(json_files)} JSON files to process")

        for json_file in json_files:
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                processed_listing = self.process_listing(data)
                if processed_listing:
                    processed_listings.append(processed_listing)

            except Exception as e:
                logger.error(f"Error processing file {json_file}: {e}")

        # Convert to DataFrame
        self.processed_data = pd.DataFrame(processed_listings)
        logger.info(f"Processed {len(processed_listings)} listings successfully")

    def save_processed_data(self, output_path: Path, format: str = "parquet"):
        """Save processed data to file"""
        if self.processed_data is None:
            logger.error("No processed data available. Run process_raw_data first.")
            return

        try:
            if format == "parquet":
                self.processed_data.to_parquet(output_path)
            elif format == "csv":
                self.processed_data.to_csv(output_path, index=False)

            logger.info(f"Saved processed data to {output_path}")
        except Exception as e:
            logger.error(f"Error saving processed data: {e}")
