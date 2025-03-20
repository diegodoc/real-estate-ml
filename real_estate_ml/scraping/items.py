# real_estate_ml/scraping/items.py
import scrapy


class RealEstateItem(scrapy.Item):
    # Basic information
    title = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    location = scrapy.Field()

    # Property specific information
    property_type = scrapy.Field()
    area_total = scrapy.Field()
    area_util = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    parking_spots = scrapy.Field()
    condo_fee = scrapy.Field()
    iptu = scrapy.Field()

    # Additional features
    accept_pets = scrapy.Field()
    furnished = scrapy.Field()
    property_condition = scrapy.Field()

    # Categories
    category = scrapy.Field()

    # Images
    image_urls = scrapy.Field()
    images = scrapy.Field()

    # Publication details
    ad_id = scrapy.Field()
    published_date = scrapy.Field()

    # Seller information
    seller_name = scrapy.Field()
    seller_since = scrapy.Field()
