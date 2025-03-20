import json
import time
import random
import uuid
from urllib.parse import urlencode
from loguru import logger
import scrapy


class OlxApiSpider(scrapy.Spider):
    name = "olx_api"
    allowed_domains = ["olx.com.br", "apigw.olx.com.br"]
    
    # Base API URL
    api_base_url = "https://apigw.olx.com.br/api/v2/rec"
    
    # Regions in Pernambuco
    regions = {
        "pernambuco": "81",
        "recife": "3744",
        "boa_viagem": "29748"
    }
    
    # Property category IDs
    categories = {
        "aluguel": "1020"
    }
    
    # Common headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Origin': 'https://www.olx.com.br',
        'Referer': 'https://www.olx.com.br/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
    }
    
    def __init__(self, region="pernambuco", category="aluguel", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.region_id = self.regions.get(region, "81")  # Default to Pernambuco
        self.category_id = self.categories.get(category, "1020")  # Default to aluguel
        self.lurker_id = str(uuid.uuid4())  # Generate a random UUID for each session
        self.processed_ads = set()  # Keep track of processed ads
        
        # Update referer to match the region and category
        self.headers['Referer'] = f'https://www.olx.com.br/imoveis/{category}/estado-{region}'
    
    def start_requests(self):
        """Generate initial API requests"""
        # First, we need to visit the main site to get cookies
        yield scrapy.Request(
            url='https://www.olx.com.br/imoveis/aluguel/estado-pe',
            callback=self.parse_main_site,
            headers=self.headers,
            meta={'dont_redirect': True, 'handle_httpstatus_list': [302, 403]}
        )
    
    def parse_main_site(self, response):
        """Parse the main site to get cookies and then make API request"""
        # Now make the API request with cookies from the main site
        params = {
            "custom_tag": "vi_web",
            "list_id": "1387432094",  # Use a known listing ID
            "lurker_id": self.lurker_id,
            "object_name": "ad_detail",  # Start with ad_detail which seems to work
            "platform": "web",
            "region_id": self.region_id,
            "subcategory_id": self.category_id,
            "test_id": "hold"
        }
        
        url = f"{self.api_base_url}?{urlencode(params)}"
        
        # Add a random delay to mimic human behavior
        time.sleep(random.uniform(2, 5))
        
        yield scrapy.Request(
            url=url,
            callback=self.parse_detail_api,
            headers=self.headers,
            meta={
                'dont_redirect': True, 
                'handle_httpstatus_list': [302, 403],
                'list_id': "1387432094"
            }
        )
    
    def parse_detail_api(self, response):
        """Parse the API response for a specific listing detail"""
        list_id = response.meta.get("list_id")
        
        # Check if we got a successful response
        if response.status != 200:
            logger.error(f"Failed to get API response: {response.status}")
            return
        
        try:
            data = json.loads(response.text)
            logger.info(f"Successfully parsed API response for listing {list_id}")
            
            # Extract listings from the response
            listings = []
            
            # Process each gallery group
            for gallery_group in data:
                if gallery_group.get("type") == "GalleryGroup":
                    for gallery in gallery_group.get("content", []):
                        for listing in gallery.get("content", []):
                            # Extract listing ID
                            new_list_id = listing.get("list_id")
                            
                            if new_list_id and new_list_id not in self.processed_ads:
                                self.processed_ads.add(new_list_id)
                                listings.append(listing)
            
            logger.info(f"Found {len(listings)} new listings")
            
            # Process each listing
            for listing in listings:
                # Extract basic information
                list_id = listing.get("list_id")
                
                # Create item with basic data
                item = {
                    'ad_id': str(list_id),
                    'title': listing.get("subject"),
                    'price': listing.get("price"),
                    'location': f"{listing.get('neighbourhood', '')}, {listing.get('municipality', '')}, {listing.get('state_uf', '').upper()}",
                    'neighbourhood': listing.get('neighbourhood'),
                    'municipality': listing.get('municipality'),
                    'state': listing.get('state_uf', '').upper(),
                    'image_url': listing.get('image_url'),
                    'ad_url': listing.get('ad_url'),
                    'date_ts': listing.get('date_ts')
                }
                
                # Make a request to the actual ad page to get more details
                ad_url = f"https://www.olx.com.br/vi/{list_id}"
                
                # Add random delay
                time.sleep(random.uniform(2, 5))
                
                yield scrapy.Request(
                    url=ad_url,
                    callback=self.parse_ad_page,
                    headers=self.headers,
                    meta={'item': item}
                )
                
            # Get more listings using the same API endpoint with different list_id
            if listings:
                # Use the last listing ID for the next request
                next_list_id = listings[-1].get("list_id")
                
                params = {
                    "custom_tag": "vi_web",
                    "list_id": next_list_id,
                    "lurker_id": self.lurker_id,
                    "object_name": "ad_detail",
                    "platform": "web",
                    "region_id": self.region_id,
                    "subcategory_id": self.category_id,
                    "test_id": "hold"
                }
                
                next_url = f"{self.api_base_url}?{urlencode(params)}"
                
                # Add random delay
                time.sleep(random.uniform(3, 7))
                
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse_detail_api,
                    headers=self.headers,
                    meta={'list_id': next_list_id}
                )
                
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON from API response: {response.text[:100]}...")
        except Exception as e:
            logger.error(f"Error parsing detail API: {e}")
    
    def parse_ad_page(self, response):
        """Parse the actual ad page to get additional details"""
        item = response.meta["item"]
        
        try:
            # Extract description
            description = response.css("div[data-testid='ad-description']::text").get()
            if description:
                item['description'] = description.strip()
            
            # Extract property details
            property_details = {}
            detail_sections = response.css("div[data-testid='ad-properties']")
            
            if detail_sections:
                detail_items = detail_sections.css("div[data-testid='ad-property']")
                for detail in detail_items:
                    label = detail.css("div[data-testid='ad-property-label']::text").get()
                    value = detail.css("div[data-testid='ad-property-value']::text").get()
                    if label and value:
                        property_details[label.strip()] = value.strip()
            
            # Map details to item fields
            item['property_type'] = property_details.get('Tipo')
            item['area_total'] = property_details.get('Área total')
            item['area_util'] = property_details.get('Área útil')
            item['bedrooms'] = property_details.get('Quartos')
            item['bathrooms'] = property_details.get('Banheiros')
            item['parking_spots'] = property_details.get('Vagas na garagem')
            item['condo_fee'] = property_details.get('Condomínio')
            item['iptu'] = property_details.get('IPTU')
            
            # Additional features
            item['accept_pets'] = property_details.get('Aceita animais')
            item['furnished'] = property_details.get('Mobiliado')
            
            # Images
            image_urls = response.css("img[data-testid='ad-image']::attr(src)").getall()
            item['image_urls'] = image_urls
            
            # Publication date
            published_date = response.css("span[data-testid='ad-posted-date']::text").get()
            item['published_date'] = published_date
            
            # Seller information
            seller_name = response.css("div[data-testid='seller-name']::text").get()
            item['seller_name'] = seller_name
            
            seller_since = response.css("div[data-testid='seller-member-since']::text").get()
            item['seller_since'] = seller_since
            
            yield item
            
        except Exception as e:
            logger.error(f"Error parsing ad page: {e}")