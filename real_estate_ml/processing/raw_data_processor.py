import json
import logging
from pathlib import Path
from typing import Dict, List, Literal

from loguru import logger
import pandas as pd


class RawDataProcessor:
    # OLX category codes
    RENT_CATEGORY = "1020"  # Aluguel
    
    def __init__(self, raw_data_dir: Path):
        self.raw_data_dir = raw_data_dir
        
    def process_file(self, file_path: Path) -> List[Dict]:
        """Process a single JSON file and extract relevant listings."""
        clean_listings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for gallery_group in data:
                # Skip "Produtos para sua casa" gallery
                if gallery_group.get("title") == "Produtos para sua casa":
                    continue
                
                gallery_type = gallery_group.get("type")
                
                if gallery_type == "GalleryGroup":
                    for gallery in gallery_group.get("content", []):
                        clean_listings.extend(
                            self._process_listing(item) 
                            for item in gallery.get("content", [])
                            if self._is_valid_listing(item)
                        )
                        
                elif gallery_type == "SingleGallery":
                    clean_listings.extend(
                        self._process_listing(item)
                        for item in gallery_group.get("content", [])
                        if self._is_valid_listing(item)
                    )
                    
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            
        return clean_listings
    
    def _is_valid_listing(self, listing: Dict) -> bool:
        """Check if listing is a rental property."""
        if not listing:
            return False
            
        category = listing.get("category")
        return category == self.RENT_CATEGORY
    
    def _process_listing(self, listing: Dict) -> Dict:
        """Extract and transform relevant fields from a listing."""
        return {
            "listing_id": listing.get("list_id"),
            "title": listing.get("subject"),
            "price": listing.get("price"),
            "url": listing.get("ad_url"),
            "image_url": listing.get("image_url"),
            "neighborhood": listing.get("neighbourhood"),
            "city": listing.get("municipality"),
            "state": listing.get("state_uf", "").upper(),
            "timestamp": listing.get("date_ts"),
        }
    
    def process_all_files(self) -> List[Dict]:
        """Process all JSON files in the raw data directory."""
        all_listings = []
        
        for file_path in self.raw_data_dir.glob("**/*.json"):
            logger.info(f"Processing {file_path}")
            listings = self.process_file(file_path)
            all_listings.extend(listings)
            logger.info(f"Found {len(listings)} valid rental listings in {file_path}")
        
        # Remove duplicates based on listing_id
        unique_listings = {
            listing["listing_id"]: listing 
            for listing in all_listings
        }.values()
        
        logger.info(f"Total unique rental listings after processing: {len(unique_listings)}")
        return list(unique_listings)
    
    def save_processed_data(
        self, 
        output_path: Path,
        format: Literal["json", "csv", "parquet"] = "parquet"
    ):
        """
        Process all files and save clean data in the specified format.
        
        Args:
            output_path: Path where to save the processed data
            format: Output format ("json", "csv", or "parquet")
        """
        clean_data = self.process_all_files()
        df = pd.DataFrame(clean_data)
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # Clean price values
        df['price'] = df['price'].str.replace('R$', '').str.strip()
        df['price'] = pd.to_numeric(df['price'].str.replace('.', '').str.replace(',', '.'), errors='coerce')
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save in the specified format
        if format == "json":
            df.to_json(output_path, orient='records', force_ascii=False, indent=2)
        elif format == "csv":
            df.to_csv(output_path, index=False)
        elif format == "parquet":
            df.to_parquet(output_path, index=False)
            
        logger.info(f"Saved processed data to {output_path} in {format} format")