from datetime import datetime
import json
from pathlib import Path
import random
import time
import uuid

from curl_cffi import requests as cureq
from loguru import logger


class ZapApiCollector:
    def __init__(self):
        # Create timestamped output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path("data/raw/zap") / timestamp / "listings"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.session_id = str(uuid.uuid4())
        self.processed_listings = set()

        # Base API URL
        self.api_base_url = "https://glue-api.zapimoveis.com.br/v2/listings"

        # Regions in Pernambuco
        self.regions = {"recife": "pe+recife", "boa_viagem": "pe+recife+boa-viagem"}

        # Property types
        self.property_types = {"apartment": "apartamento", "house": "casa"}

        # Headers for API requests
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://www.zapimoveis.com.br",
            "Referer": "https://www.zapimoveis.com.br/",
            "x-domain": "www.zapimoveis.com.br",
        }

        logger.info("ZAP API Collector initialized")

    def get_api_response(self, listing_id):
        """Get API response for a specific listing ID"""
        try:
            url = f"{self.api_base_url}/{listing_id}"
            logger.info(f"Making API request for listing ID: {listing_id}")

            response = cureq.get(url, headers=self.headers, impersonate="chrome110")

            if response.status_code == 200:
                logger.info(f"Successfully retrieved API response for listing ID: {listing_id}")
                return response.json()
            else:
                logger.error(f"Failed to get API response: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error getting API response: {e}")
            return None

    def save_api_response(self, data, listing_id):
        """Save API response to a JSON file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"listing_{listing_id}_{timestamp}.json"
            filepath = self.output_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return filepath
        except Exception as e:
            logger.error(f"Error saving API response: {e}")
            return None

    def collect_listings(self, listing_ids):
        """Collect data for a list of listing IDs"""
        for listing_id in listing_ids:
            if listing_id in self.processed_listings:
                logger.info(f"Listing {listing_id} already processed, skipping...")
                continue

            response_data = self.get_api_response(listing_id)
            if response_data:
                self.save_api_response(response_data, listing_id)
                self.processed_listings.add(listing_id)

            # Random delay between requests
            time.sleep(random.uniform(2, 5))


if __name__ == "__main__":
    # Example listing IDs - to be replaced with actual IDs
    listing_ids = [
        # Add ZAP listing IDs here
    ]

    collector = ZapApiCollector()
    collector.collect_listings(listing_ids)
