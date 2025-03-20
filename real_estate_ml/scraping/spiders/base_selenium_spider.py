from loguru import logger
from scrapy import Spider
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import random


class BaseSeleniumSpider(Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = None

    def start_selenium(self):
        """Initialize the Selenium WebDriver with optimal settings"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--enable-javascript")
        
        # Rotate between different user agents
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        ]
        chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

        # Add additional headers
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute CDP commands to make detection harder
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                """
            })
            
            logger.info("Selenium WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Selenium WebDriver: {e}")
            raise

    def close_selenium(self):
        """Close the Selenium WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info("Selenium WebDriver closed")

    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            logger.warning(f"Timeout waiting for element {value}: {e}")
            return None

    def safe_get(self, url):
        """Safely navigate to a URL with error handling"""
        try:
            self.driver.get(url)
            return True
        except Exception as e:
            logger.error(f"Failed to load URL {url}: {e}")
            return False

    def closed(self, reason):
        """Spider closed signal handler"""
        self.close_selenium()
