import os
from pathlib import Path

# Spider settings
SPIDER_MODULES = ['real_estate_ml.scraping.spiders']
NEWSPIDER_MODULE = 'real_estate_ml.scraping.spiders'

# Project structure settings
PROJECT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_DIR / "data" / "raw"

# Output settings
FEEDS = {
    os.path.join(DATA_DIR, "olx_data.json"): {
        "format": "json",
        "encoding": "utf8",
    }
}

# Pipeline settings
ITEM_PIPELINES = {
    'real_estate_ml.scraping.pipelines.RealEstatePipeline': 300,
}

# Additional settings
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOAD_DELAY = 3

# Respect robots.txt
ROBOTSTXT_OBEY = True

# Enable cookies
COOKIES_ENABLED = True

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 8

# Add retry middleware
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]

# Enable the default spider middleware
SPIDER_MIDDLEWARES = {
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': True,
}
