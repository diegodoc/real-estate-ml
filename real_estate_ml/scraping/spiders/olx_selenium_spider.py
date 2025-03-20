import time
import random
from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from ..items import RealEstateItem
from .base_selenium_spider import BaseSeleniumSpider


class OlxSeleniumSpider(BaseSeleniumSpider):
    name = "olx_selenium"
    allowed_domains = ["olx.com.br"]
    start_urls = [
        "https://www.olx.com.br/imoveis/aluguel/estado-pe"
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_selenium()

    def parse(self, response):
        """Entry point for the spider"""
        for url in self.start_urls:
            # Add random delay between requests
            time.sleep(random.uniform(3, 7))
            
            if self.safe_get(url):
                # Wait for page to load completely
                time.sleep(5)
                
                try:
                    # Check for any popup/overlay and close it if present
                    popup_close_buttons = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='modal-close-button']")
                    if popup_close_buttons:
                        popup_close_buttons[0].click()
                        time.sleep(1)
                    
                    yield from self.parse_listing_page()
                except Exception as e:
                    logger.error(f"Error parsing page: {e}")

    def parse_listing_page(self):
        """Parse the listing page and extract ad links"""
        try:
            # Wait longer for the ad list to load
            self.wait_for_element(By.CSS_SELECTOR, "[data-testid='listing-main']", timeout=20)
            
            # Get all ad links using updated selectors
            ad_links = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='listing-card-link']")
            logger.info(f"Found {len(ad_links)} ads on page")

            if not ad_links:
                logger.warning("No ads found on page - might be blocked")
                return

            # Extract hrefs
            urls = [link.get_attribute('href') for link in ad_links]
            
            # Visit each ad
            for url in urls:
                time.sleep(random.uniform(4, 8))  # Random delay between ads
                if self.safe_get(url):
                    yield self.parse_ad()

            # Handle pagination with updated selector
            next_button = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='pagination-next']")
            if next_button and next_button[0].is_enabled():
                next_url = next_button[0].get_attribute('href')
                if next_url and self.safe_get(next_url):
                    time.sleep(random.uniform(5, 10))  # Random delay between pages
                    yield from self.parse_listing_page()

        except TimeoutException:
            logger.warning("Timeout waiting for listing page to load")
        except Exception as e:
            logger.error(f"Error in parse_listing_page: {e}")

    def parse_ad(self):
        """Parse individual ad page"""
        item = RealEstateItem()
        # Basic information
        title_elem = self.wait_for_element(By.CSS_SELECTOR, "h2.olx-ad-card__title::text")
        item['title'] = title_elem.text if title_elem else None

        description_elem = self.wait_for_element(By.CSS_SELECTOR, "div#ad-description")
        item['description'] = description_elem.text if description_elem else None

        price_elem = self.wait_for_element(By.CSS_SELECTOR, "h2.ad__sc-12l420o-1")
        item['price'] = price_elem.text if price_elem else None

        location_elem = self.wait_for_element(By.CSS_SELECTOR, "div.ad__sc-1f2ug0x-3")
        item['location'] = location_elem.text if location_elem else None

        # Extract details
        details = {}
        detail_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.ad__sc-1f2ug0x-1 dt, div.ad__sc-1f2ug0x-1 dd")
        for i in range(0, len(detail_elements), 2):
            if i + 1 < len(detail_elements):
                key = detail_elements[i].text.strip()
                value = detail_elements[i + 1].text.strip()
                details[key] = value

        # Map details to item fields
        item['property_type'] = details.get('Tipo')
        item['area_total'] = details.get('Área total')
        item['area_util'] = details.get('Área útil')
        item['bedrooms'] = details.get('Quartos')
        item['bathrooms'] = details.get('Banheiros')
        item['parking_spots'] = details.get('Vagas na garagem')
        item['condo_fee'] = details.get('Condomínio')
        item['iptu'] = details.get('IPTU')
        
        # Images
        image_elements = self.driver.find_elements(By.CSS_SELECTOR, "img.image__image-thumbnail")
        item['image_urls'] = [img.get_attribute('src') for img in image_elements]

        return item
