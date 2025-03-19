# real_estate_ml/scraping/items.py
import scrapy

class RealEstateItem(scrapy.Item):
    title = scrapy.Field()  # Título do anúncio
    description = scrapy.Field()  # Descrição do imóvel
    price = scrapy.Field()  # Preço
    location = scrapy.Field()  # Localização
    image_urls = scrapy.Field()  # URLs das imagens
    images = scrapy.Field()  # Informações sobre as imagens baixadas