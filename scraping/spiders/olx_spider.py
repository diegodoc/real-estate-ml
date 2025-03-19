# real_estate_ml/scraping/spiders/olx_spider.py
import scrapy

from real_estate_ml.scraping.items import RealEstateItem # type: ignore


class OlxSpider(scrapy.Spider):
    name = "olx"  # Nome único do spider
    start_urls = [
        "https://www.olx.com.br/imoveis"  # URL inicial
    ]

    def parse(self, response):
        # Extrair links para os anúncios
        for ad in response.css('ul#ad-list li a::attr(href)').getall():
            yield response.follow(ad, self.parse_ad)

        # Paginação: seguir para a próxima página
        next_page = response.css('a[data-lurker-detail="next_page"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_ad(self, response):
        item = RealEstateItem()
        item['title'] = response.css('h1::text').get().strip()
        item['description'] = " ".join(response.css('div#ad-description::text').getall()).strip()
        item['price'] = response.css('h2::text').get().strip()
        item['location'] = response.css('div.location::text').get().strip()
        item['image_urls'] = response.css('img::attr(src)').getall()
        yield item