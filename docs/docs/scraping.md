# Web Scraping Guide

This document outlines how to use and configure the web scraping functionality in the project.

## Current Scraping Flow

### 1. Data Collection
#### OLX API Collector (`olx_api_collector.py`):
- Uses `curl_cffi` for making requests to OLX's API
- Collects property listing data including:
  - Title
  - Description
  - Price
  - Location
  - Additional property details
- Handles rate limiting and mimics browser behavior
- Saves responses as JSON files in `data/raw/olx/YYYYMMDD_HHMMSS/listings/`

### Dependencies
The scraping functionality requires:
- curl_cffi: For making HTTP requests that bypass anti-bot measures
- loguru: For logging
- pyarrow: For Parquet file support
- Other standard libraries (datetime, json, pathlib, etc.)

### Usage
Run the collector using:
```bash
make scrape-olx
```

### Data Flow
1. **Collection**: Raw data is saved in:
   ```
   data/raw/olx/YYYYMMDD_HHMMSS/listings/*.json
   ```

2. **Processing**: Process the raw data using:
   ```bash
   make process-olx
   ```
   This creates processed files in:
   ```
   data/processed/olx/YYYYMMDD/
   ├── listings.parquet  # Optimized for ML pipelines
   └── listings.csv      # Easy to view and analyze
   ```

### 2. Data Structure
The collected data follows this structure:
```json
{
    "title": "House for sale downtown",
    "description": "House with 3 bedrooms, 2 bathrooms...",
    "price": 500000.0,
    "location": "São Paulo, SP",
    "image_urls": ["http://example.com/image1.jpg", "http://example.com/image2.jpg"]
}
```

## Customization Guide

### 1. Define Required Data
Before adjusting the spider, clearly define what data you need to collect:

#### Basic Data:
- Listing title
- Property description
- Price
- Location

#### Additional Data:
- Property area
- Number of rooms, bathrooms, parking spaces
- Property type (house, apartment, land)
- Extra features (pool, leisure area, etc.)

#### Images:
- Image URLs or direct image downloads

### 2. Adjust Spider for Additional Data
Modify `olx_spider.py` to add CSS or XPath selectors for additional data:

```python
def parse_ad(self, response):
    item = RealEstateItem()
    item['title'] = response.css('h1::text').get().strip()
    item['description'] = " ".join(response.css('div#ad-description::text').getall()).strip()
    item['price'] = response.css('h2::text').get().strip()
    item['location'] = response.css('div.location::text').get().strip()
    item['area'] = response.css('span.area::text').get().strip()
    item['bedrooms'] = response.css('span.bedrooms::text').get().strip()
    item['bathrooms'] = response.css('span.bathrooms::text').get().strip()
    item['type'] = response.css('span.property-type::text').get().strip()
    item['image_urls'] = response.css('img::attr(src)').getall()
    yield item
```

Tip: Use browser DevTools to inspect elements and find correct selectors.

### 3. Customize Pipeline Processing
Modify `pipelines.py` to process data as needed:

```python
class RealEstatePipeline:
    def process_item(self, item, spider):
        # Clean and transform price
        if "price" in item:
            item["price"] = float(item["price"].replace("$", "").replace(",", "").strip())

        # Convert area to float
        if "area" in item:
            item["area"] = float(item["area"].replace("m²", "").strip())

        # Convert rooms and bathrooms to integer
        if "bedrooms" in item:
            item["bedrooms"] = int(item["bedrooms"])
        if "bathrooms" in item:
            item["bathrooms"] = int(item["bathrooms"])

        return item
```

### 4. Handle Dynamic Sites (JavaScript)
For JavaScript-rendered sites, use Scrapy-Splash:

1. Install Scrapy-Splash:
```bash
pip install scrapy-splash
```

2. Configure `settings.py`:
```python
SPLASH_URL = 'http://localhost:8050'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
```

3. Use SplashRequest in spider:
```python
from scrapy_splash import SplashRequest

def start_requests(self):
    for url in self.start_urls:
        yield SplashRequest(url, self.parse, args={'wait': 2})
```

### 5. Image Downloads
To enable image downloads, configure in `settings.py`:

```python
ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
    'real_estate_ml.scraping.pipelines.RealEstatePipeline': 300,
}

IMAGES_STORE = 'data/raw/images'
```

### 6. Automation
Use Makefile to automate the scraping process:

```makefile
scrape:
    cd real_estate_ml/scraping && scrapy crawl olx

process:
    python real_estate_ml/dataset.py

train:
    python real_estate_ml/modeling/train.py

all: scrape process train
```

## Testing and Maintenance

1. Run spider and verify data collection:
```bash
scrapy crawl olx --loglevel=INFO
```

2. Monitor and maintain:
- Regularly check if spider still works
- Adjust selectors if website structure changes
- Update processing logic as needed

## Next Steps

1. Expand to Other Sites:
   - Create additional spiders for other real estate platforms
   - Standardize data format across different sources

2. AI Integration:
   - Use collected data for training and evaluating classification models
   - Implement data validation and cleaning pipelines

3. Monitoring:
   - Set up regular checks for spider functionality
   - Implement error notifications
   - Track data quality metrics
