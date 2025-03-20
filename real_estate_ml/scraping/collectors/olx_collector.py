from datetime import datetime
import json
import os
from pathlib import Path
import random
import time
import uuid

from curl_cffi import requests as cureq
from loguru import logger


class OlxApiCollector:
    def __init__(self):
        # Create timestamped output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path("data/raw/olx") / timestamp / "listings"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.lurker_id = str(uuid.uuid4())
        self.processed_listings = set()
        
        # Base API URL
        self.api_base_url = "https://apigw.olx.com.br/api/v2/rec"
        
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
        
        # Add headers as a class attribute
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Origin': 'https://www.olx.com.br',
            'Referer': 'https://www.olx.com.br/',
        }
        
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
    
    def get_search_results(self, page=1, state="pe", region_id="81"):
        """Get paginated search results"""
        try:
            # Search API endpoint
            search_url = "https://apigw.olx.com.br/v2/listings"
            
            # Search parameters
            params = {
                "offset": (page - 1) * 50,  # 50 items per page
                "limit": 50,
                "sf": 1,  # Sort by most recent
                "sf_ur": 0,
                "region_id": region_id,
                "state": state,
                "category_id": "1020",  # Real estate category
            }
            
            # Make the request
            response = cureq.get(
                search_url,
                params=params,
                headers=self.headers,
                impersonate="chrome110"
            )
            
            if response.status_code == 200:
                data = response.json()
                total_pages = data.get("total_count", 0) // 50 + 1
                logger.info(f"Got page {page}/{total_pages} of search results")
                return data.get("listings", []), total_pages
            else:
                logger.error(f"Search API request failed: {response.status_code}")
                return [], 0
                
        except Exception as e:
            logger.error(f"Error getting search results: {e}")
            return [], 0
    
    def collect_listings_from_urls(self, listing_ids):
        """Collect listings from a list of manually provided listing IDs"""
        try:
            collected_count = 0
            
            for list_id in listing_ids:
                if list_id not in self.processed_listings:
                    # Get recommendations for this listing
                    response_data = self.get_api_response(list_id)
                    
                    if response_data:
                        self.save_api_response(response_data, list_id)
                        
                        # Extract and process listings from response
                        new_listings = self.extract_listings_from_response(response_data)
                        collected_count += len(new_listings)
                    
                    # Add a random delay between requests
                    delay = random.uniform(2, 5)
                    time.sleep(delay)
            
            logger.info(f"Data collection completed. Total listings processed: {collected_count}")
            
        except Exception as e:
            logger.error(f"Error during data collection: {e}")

if __name__ == "__main__":
    # Configure logger
    logger.add("c:/Users/Diego/Documents/Projetos/Python/real-estate-ml/real-estate-ml/logs/olx_collector_{time}.log")
    
    
    # List of manually collected listing IDs
    listing_ids = [
        "1387432094",  # Example listing ID
        "1367766557", 
        "1359633911",
        "1361278216",
        "1388094485",
        "1388094441",
        "1347778773",
        "1388083361",
        "1388085740",
        "1388084424",
        "1388077714",
        "1388076547",
        "1388075073",
        "1388074892",
        "1388073444",
        "1388073442",
        "1388073004",
        "1388072631",
        "1388072634",
        "1388071210",
        "1388070592",
        "1388070947",
        "1388065611",
        "1386097750",
        "1388072634",
        "1388070947",
        "1388070592",
        "1387655158",
        "1387351167",
        "1387870189",
        "1386465326",
        "1386271030",
        "1387344472",
        "1388061645",
        "1388059814",
        "1388058538",
        "1388058539",
        "1360035880",
        "1387432094",
        "1386303652",
        "1387978206",
        "1388058539",
        "1388058230",
        "1388058164",
        "1388058135",
        "1388058132",
        "1388058058",
        "1377268092",
        "1388054300",
        "1388053807",
        "1388053521",
        "1354407372",
        "1388051289",
        "1388051291",
        "1388051239",
        "1388051224",
        "1386388042",
        "1388050487",
        "1388050351",
        "1388050231",
        "1388049609",
        "1388049546",
        "1388049314",
        "1388049290",
        "1388049186",
        "1388049146",
        "1378029650",
        "1366637826",
        "1386288551",
        "1381286386",
    ]
    
    # Run the collector
    collector = OlxApiCollector()
    collector.collect_listings_from_urls(listing_ids)
