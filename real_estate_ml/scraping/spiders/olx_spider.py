from loguru import logger
import scrapy

from real_estate_ml.scraping.items import RealEstateItem  # type: ignore


class OlxSpider(scrapy.Spider):
    name = "olx"
    allowed_domains=["olx.com.br"]
    start_urls = [
        "https://www.olx.com.br/imoveis/aluguel/estado-pe?lis=home_body_search_bar_1002"  # Target URL specifically in my state
    ]

    def parse(self, response):
        
        logger.info(f"Parsing page: {response.url}")
        ads = response.css('ul#ad-list li a::attr(href)').getall()
        logger.info(f"Found {len(ads)} ads on this page")
        
        for ad in ads:
            logger.info(f"Following ad link: {ad}")
            yield response.follow(ad, self.parse_ad)

        # Pagination: follow to next page
        next_page = response.css('a[data-lurker-detail="next_page"]::attr(href)').get()
        if next_page:
            logger.info(f"Found next page: {next_page}")
            yield response.follow(next_page, self.parse)
        else:
            logger.info("No next page found")

    def parse_ad(self, response):
        logger.info(f"Parsing ad: {response.url}")
        item = RealEstateItem()
        
        # Basic information
        item['title'] = response.css('h1::text').get()
        if item['title']:
            item['title'] = item['title'].strip()
            logger.info(f"Found title: {item['title']}")
        else:
            logger.warning(f"No title found for {response.url}")

        item['description'] = " ".join(response.css('div#ad-description::text').getall()).strip()
        item['price'] = response.css('h2.ad__sc-12l420o-1::text').get().strip()
        item['location'] = response.css('div.ad__sc-1f2ug0x-3::text').get().strip()
        
        # Additional details commonly found in OLX real estate listings
        details = response.css('div.ad__sc-1f2ug0x-1 dt::text, div.ad__sc-1f2ug0x-1 dd::text').getall()
        details_dict = {details[i].strip(): details[i+1].strip() for i in range(0, len(details), 2) if i+1 < len(details)}
        
        # Property specific information
        item['property_type'] = details_dict.get('Tipo')  # house, apartment, etc
        item['area_total'] = details_dict.get('Área total')  # total area
        item['area_util'] = details_dict.get('Área útil')  # usable area
        item['bedrooms'] = details_dict.get('Quartos')  # number of bedrooms
        item['bathrooms'] = details_dict.get('Banheiros')  # number of bathrooms
        item['parking_spots'] = details_dict.get('Vagas na garagem')  # parking spots
        item['condo_fee'] = details_dict.get('Condomínio')  # condominium fee
        item['iptu'] = details_dict.get('IPTU')  # property tax
        
        # Additional features
        item['accept_pets'] = details_dict.get('Aceita animais')  # accepts pets
        item['furnished'] = details_dict.get('Mobiliado')  # is furnished
        item['property_condition'] = details_dict.get('Condição do item')  # property condition
        
        # Categories and subcategories
        item['category'] = response.css('span[data-testid="breadcrumb-title"]::text').getall()
        
        # Images
        item['image_urls'] = response.css('img.image__image-thumbnail::attr(src)').getall()
        
        # Publication details
        item['ad_id'] = response.css('span[data-testid="ad-identifier"]::text').get()
        item['published_date'] = response.css('span.ad__sc-1oq8jzc-0::text').get()
        
        # Seller information
        item['seller_name'] = response.css('span[data-testid="seller-name"]::text').get()
        item['seller_since'] = response.css('span.sc-bZQynM::text').get()
        
        yield item
