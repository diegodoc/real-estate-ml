import json
import time
import random
import os
import uuid
from pathlib import Path
from datetime import datetime
from curl_cffi import requests as cureq
from loguru import logger

class OlxApiCollector:
    def __init__(self, output_dir="data/raw/olx"):
        self.output_dir = Path(os.path.join("c:/Users/Diego/Documents/Projetos/Python/real-estate-ml/real-estate-ml", output_dir))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Base API URL
        self.api_base_url = "https://apigw.olx.com.br/api/v2/rec"
        
        # Generate a random UUID for lurker_id
        self.lurker_id = str(uuid.uuid4())
        
        # Regions in Pernambuco
        self.regions = {
            "pernambuco": "81",
            "recife": "3744",
            "boa_viagem": "29748"
        }
        
        # Property category IDs
        self.categories = {
            "aluguel": "1020"
        }
        
        # Track processed listings
        self.processed_listings = set()
        
        logger.info("OLX API Collector initialized")
    
    def get_api_response(self, list_id, region_id="81", category_id="1020"):
        """Get API response for a specific listing ID"""
        try:
            # Prepare API parameters
            params = {
                "custom_tag": "vi_web",
                "list_id": list_id,
                "lurker_id": self.lurker_id,
                "object_name": "ad_detail",
                "platform": "web",
                "region_id": region_id,
                "subcategory_id": category_id,
                "test_id": "hold"
            }
            
            # Prepare headers to mimic a browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                'Origin': 'https://www.olx.com.br',
                'Referer': 'https://www.olx.com.br/',
            }
            
            # Make the request using curl_cffi
            url = f"{self.api_base_url}"
            logger.info(f"Making API request for listing ID: {list_id}")
            
            response = cureq.get(
                url, 
                params=params, 
                headers=headers,
                impersonate="chrome110"
            )
            
            # Check if request was successful
            if response.status_code == 200:
                logger.info(f"Successfully retrieved API response for listing ID: {list_id}")
                return response.json()
            else:
                logger.error(f"Failed to get API response: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting API response: {e}")
            return None
    
    def save_api_response(self, data, list_id):
        """Save API response to a JSON file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"listing_{list_id}_{timestamp}.json"
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved API response to: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving API response: {e}")
            return None
    
    def extract_listings_from_response(self, response_data):
        """Extract listing IDs from API response"""
        listings = []
        
        try:
            # Process each gallery group
            for gallery_group in response_data:
                # Skip galleries with title "Produtos para sua casa"
                if gallery_group.get("title") == "Produtos para sua casa":
                    logger.info("Skipping 'Produtos para sua casa' gallery")
                    continue
                
                gallery_type = gallery_group.get("type")
                if gallery_type == "GalleryGroup":
                    for gallery in gallery_group.get("content", []):
                        for listing in gallery.get("content", []):
                            # Extract listing ID
                            list_id = listing.get("list_id")
                            category = listing.get("category")
                            
                            # Skip if not a real estate listing
                            if category and category not in ["1020", "1010"]:
                                continue
                            
                            if list_id and list_id not in self.processed_listings:
                                self.processed_listings.add(list_id)
                                listings.append({
                                    "list_id": list_id,
                                    "subject": listing.get("subject"),
                                    "price": listing.get("price"),
                                    "neighbourhood": listing.get("neighbourhood"),
                                    "municipality": listing.get("municipality"),
                                    "state_uf": listing.get("state_uf"),
                                    "ad_url": listing.get("ad_url"),
                                    "category": category
                                })
                elif gallery_type == "SingleGallery":
                    # Skip if this is a "Produtos para sua casa" gallery
                    for listing in gallery_group.get("content", []):
                        list_id = listing.get("list_id")
                        category = listing.get("category")
                        
                        # Skip if not a real estate listing
                        if category and category not in ["1020", "1010"]:
                            continue
                        
                        if list_id and list_id not in self.processed_listings:
                            self.processed_listings.add(list_id)
                            listings.append({
                                "list_id": list_id,
                                "subject": listing.get("subject"),
                                "price": listing.get("price"),
                                "neighbourhood": listing.get("neighbourhood"),
                                "municipality": listing.get("municipality"),
                                "state_uf": listing.get("state_uf"),
                                "ad_url": listing.get("ad_url"),
                                "category": category
                            })
            
            logger.info(f"Extracted {len(listings)} new real estate listings (filtered out non-real estate items)")
            return listings
        except Exception as e:
            logger.error(f"Error extracting listings: {e}")
            return []
    
    def collect_listings(self, seed_list_id="1387432094", max_listings=50):
        """Collect listings starting from a seed listing ID"""
        try:
            collected_count = 0
            current_list_id = seed_list_id
            
            while collected_count < max_listings:
                # Get API response for current listing ID
                response_data = self.get_api_response(current_list_id)
                
                if not response_data:
                    logger.warning(f"No data received for listing ID: {current_list_id}")
                    break
                
                # Save the API response
                self.save_api_response(response_data, current_list_id)
                
                # Extract new listings from the response
                new_listings = self.extract_listings_from_response(response_data)
                
                if not new_listings:
                    logger.warning("No new listings found in response")
                    break
                
                collected_count += 1
                
                # Use the last listing ID as the next seed
                current_list_id = new_listings[-1]["list_id"]
                
                # Add a random delay between requests
                delay = random.uniform(2, 5)
                logger.info(f"Waiting {delay:.1f} seconds before next request")
                time.sleep(delay)
                
                # Log progress
                logger.info(f"Collected {collected_count}/{max_listings} listings")
            
            logger.info(f"Data collection completed. Total listings: {collected_count}")
            
        except Exception as e:
            logger.error(f"Error during data collection: {e}")

if __name__ == "__main__":
    # Configure logger
    logger.add("c:/Users/Diego/Documents/Projetos/Python/real-estate-ml/real-estate-ml/logs/olx_collector_{time}.log")
    
    # Run the collector
    collector = OlxApiCollector()
    collector.collect_listings(max_listings=20)