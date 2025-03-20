import random
import time

from loguru import logger
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium_stealth import stealth

from ..items import RealEstateItem
from .base_selenium_spider import BaseSeleniumSpider


class OlxSeleniumSpider(BaseSeleniumSpider):
    name = "olx_selenium"
    allowed_domains = ["olx.com.br"]
    start_urls = ["https://www.olx.com.br/imoveis/aluguel/estado-pe"]

    def __init__(self, max_pages=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_pages = int(max_pages) if max_pages else None
        self.pages_scraped = 0
        self.start_selenium()
        self.setup_stealth()

    def setup_stealth(self):
        """Setup stealth measures to avoid detection"""
        try:
            # Apply stealth techniques
            stealth(
                self.driver,
                languages=["pt-BR", "pt", "en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )

            # Disable webdriver flags
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )

            # Add additional browser fingerprinting evasion
            self.driver.execute_script("""
                // Override properties that detect automation
                const newProto = navigator.__proto__;
                delete newProto.webdriver;
                navigator.__proto__ = newProto;
                
                // Add fake plugins
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                
                // Add fake languages
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['pt-BR', 'pt', 'en-US', 'en']
                });
            """)

            logger.info("Stealth setup complete")
        except Exception as e:
            logger.error(f"Error in stealth setup: {e}")

    def safe_get(self, url):
        """Enhanced safe navigation with human-like behavior"""
        try:
            # Navigate to the page
            self.driver.get(url)

            # Wait for page to load
            time.sleep(random.uniform(3, 5))

            # Simulate human-like scrolling
            self.simulate_human_behavior()

            # Check for blocking
            if any(
                x in self.driver.page_source.lower()
                for x in ["403", "blocked", "captcha", "security check"]
            ):
                logger.warning("Detected blocking, taking screenshot for debugging")
                self.take_screenshot(f"blocked_{int(time.time())}.png")
                return False

            return True
        except Exception as e:
            logger.error(f"Failed to load URL {url}: {e}")
            return False

    def simulate_human_behavior(self):
        """Simulate realistic human browsing behavior"""
        try:
            # Random scrolling
            scroll_amount = 0
            max_scroll = self.driver.execute_script("return document.body.scrollHeight")

            # Scroll down in a human-like pattern with pauses
            while scroll_amount < max_scroll:
                # Random scroll step (humans don't scroll uniformly)
                step = random.randint(100, 300)
                scroll_amount += step

                # Scroll to new position
                self.driver.execute_script(f"window.scrollTo(0, {scroll_amount})")

                # Random pause (humans pause to read)
                time.sleep(random.uniform(0.5, 2.0))

                # Sometimes move mouse (if not in headless mode)
                if random.random() < 0.3 and not self.driver.capabilities.get("headless", True):
                    actions = ActionChains(self.driver)
                    x, y = random.randint(0, 500), random.randint(0, 500)
                    actions.move_by_offset(x, y).perform()

            # Sometimes scroll back up a bit (humans do this)
            if random.random() < 0.5:
                up_amount = random.randint(100, 500)
                self.driver.execute_script(f"window.scrollTo(0, {scroll_amount - up_amount})")
                time.sleep(random.uniform(0.5, 1.5))

        except Exception as e:
            logger.error(f"Error during human simulation: {e}")

    def take_screenshot(self, filename):
        """Take a screenshot for debugging"""
        try:
            from pathlib import Path

            screenshots_dir = Path(
                "c:/Users/Diego/Documents/Projetos/Python/real-estate-ml/real-estate-ml/debug"
            )
            screenshots_dir.mkdir(exist_ok=True)

            screenshot_path = screenshots_dir / filename
            self.driver.save_screenshot(str(screenshot_path))
            logger.info(f"Screenshot saved to {screenshot_path}")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")

    def parse(self, response):
        """Entry point for the spider"""
        for url in self.start_urls:
            # Add random delay between requests
            time.sleep(random.uniform(5, 10))

            if self.safe_get(url):
                # Wait for page to load completely
                time.sleep(random.uniform(3, 7))

                try:
                    # Check for any popup/overlay and close it if present
                    popup_close_buttons = self.driver.find_elements(
                        By.CSS_SELECTOR, "[data-testid='modal-close-button']"
                    )
                    if popup_close_buttons:
                        popup_close_buttons[0].click()
                        time.sleep(1)

                    # Accept cookies if present
                    cookie_buttons = self.driver.find_elements(
                        By.CSS_SELECTOR, "button[data-testid='cookie-policy-accept-all']"
                    )
                    if cookie_buttons:
                        cookie_buttons[0].click()
                        time.sleep(1)

                    yield from self.parse_listing_page()
                except Exception as e:
                    logger.error(f"Error parsing page: {e}")
                    self.take_screenshot(f"error_{int(time.time())}.png")

    def parse_listing_page(self):
        """Parse the listing page and extract ad links"""
        try:
            # Wait longer for the ad list to load
            self.wait_for_element(By.CSS_SELECTOR, "[data-testid='listing-main']", timeout=20)

            # Get all ad links using updated selectors
            ad_links = self.driver.find_elements(
                By.CSS_SELECTOR, "[data-testid='listing-card-link']"
            )
            logger.info(f"Found {len(ad_links)} ads on page")

            if not ad_links:
                logger.warning("No ads found on page - might be blocked")
                return

            # Extract hrefs
            urls = [link.get_attribute("href") for link in ad_links]

            # Visit each ad
            for url in urls:
                # Longer random delay between ads
                time.sleep(random.uniform(8, 15))
                if self.safe_get(url):
                    yield self.parse_ad()
                    # Add extra delay after parsing
                    time.sleep(random.uniform(5, 10))

            # Handle pagination with improved method
            if self.handle_pagination():
                yield from self.parse_listing_page()

        except TimeoutException:
            logger.warning("Timeout waiting for listing page to load")
        except Exception as e:
            logger.error(f"Error in parse_listing_page: {e}")

    def handle_pagination(self):
        """Handle pagination and return True if next page is loaded successfully"""
        try:
            # Try to find the next button
            next_button = self.driver.find_elements(
                By.CSS_SELECTOR, "[data-testid='pagination-next']"
            )

            # If next button exists and is enabled
            if next_button and next_button[0].is_enabled():
                next_url = next_button[0].get_attribute("href")

                # Check if we have a valid URL
                if next_url and next_url != self.driver.current_url:
                    logger.info(f"Moving to next page: {next_url}")

                    # Add random delay before clicking
                    time.sleep(random.uniform(5, 10))

                    # Click the button instead of navigating directly
                    next_button[0].click()

                    # Wait for the page to load
                    time.sleep(random.uniform(3, 5))

                    # Check if page loaded successfully
                    if self.wait_for_element(
                        By.CSS_SELECTOR, "[data-testid='listing-main']", timeout=20
                    ):
                        return True
                    else:
                        logger.warning("Next page didn't load properly")
                        return False
                else:
                    logger.info("No valid next URL found")
                    return False
            else:
                logger.info("No next button found or it's disabled - reached last page")
                return False

        except Exception as e:
            logger.error(f"Error in pagination: {e}")
            return False

    def parse_ad(self):
        """Parse individual ad page"""
        item = RealEstateItem()

        # Basic information - Updated selectors
        title_elem = self.wait_for_element(By.CSS_SELECTOR, "h1[data-testid='ad-title']")
        item["title"] = title_elem.text if title_elem else None

        description_elem = self.wait_for_element(
            By.CSS_SELECTOR, "div[data-testid='ad-description']"
        )
        item["description"] = description_elem.text if description_elem else None

        price_elem = self.wait_for_element(By.CSS_SELECTOR, "div[data-testid='ad-price-value']")
        item["price"] = price_elem.text if price_elem else None

        location_elem = self.wait_for_element(By.CSS_SELECTOR, "div[data-testid='ad-address']")
        item["location"] = location_elem.text if location_elem else None

        # Publication date
        published_date_elem = self.wait_for_element(
            By.CSS_SELECTOR, "span[data-testid='ad-posted-date']"
        )
        item["published_date"] = published_date_elem.text if published_date_elem else None

        # Ad ID
        ad_id_elem = self.wait_for_element(By.CSS_SELECTOR, "span[data-testid='ad-identifier']")
        if ad_id_elem:
            # Extract just the number from text like "ID: 12345678"
            ad_id_text = ad_id_elem.text
            item["ad_id"] = ad_id_text.split(":")[-1].strip() if ":" in ad_id_text else ad_id_text

        # Extract details
        details = {}
        detail_sections = self.driver.find_elements(
            By.CSS_SELECTOR, "div[data-testid='ad-properties']"
        )

        if detail_sections:
            detail_items = detail_sections[0].find_elements(
                By.CSS_SELECTOR, "div[data-testid='ad-property']"
            )
            for detail in detail_items:
                # Each property has a label and value
                label_elem = detail.find_element(
                    By.CSS_SELECTOR, "div[data-testid='ad-property-label']"
                )
                value_elem = detail.find_element(
                    By.CSS_SELECTOR, "div[data-testid='ad-property-value']"
                )
                if label_elem and value_elem:
                    key = label_elem.text.strip()
                    value = value_elem.text.strip()
                    details[key] = value

        # Map details to item fields
        item["property_type"] = details.get("Tipo")
        item["area_total"] = details.get("Área total")
        item["area_util"] = details.get("Área útil")
        item["bedrooms"] = details.get("Quartos")
        item["bathrooms"] = details.get("Banheiros")
        item["parking_spots"] = details.get("Vagas na garagem")
        item["condo_fee"] = details.get("Condomínio")
        item["iptu"] = details.get("IPTU")

        # Additional features
        item["accept_pets"] = details.get("Aceita animais")
        item["furnished"] = details.get("Mobiliado")

        # Images - Updated selector
        image_elements = self.driver.find_elements(By.CSS_SELECTOR, "img[data-testid='ad-image']")
        item["image_urls"] = [img.get_attribute("src") for img in image_elements]

        # Seller information
        seller_name_elem = self.wait_for_element(By.CSS_SELECTOR, "div[data-testid='seller-name']")
        item["seller_name"] = seller_name_elem.text if seller_name_elem else None

        seller_since_elem = self.wait_for_element(
            By.CSS_SELECTOR, "div[data-testid='seller-member-since']"
        )
        item["seller_since"] = seller_since_elem.text if seller_since_elem else None

        return item
