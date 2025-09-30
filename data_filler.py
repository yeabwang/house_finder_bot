import tempfile
import shutil
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from typing import List

from models import DataFiller, ParsedResults

logger = logging.getLogger(__name__)


class DataFillerService:

    def __init__(self, data_filler: DataFiller):
        self.chrome_options = webdriver.ChromeOptions()
        self.user_dir = tempfile.mkdtemp(prefix="chrome_temp_profile_")
        self.time_out = data_filler.default_timeout
        self._setup_chrome_options()
        self.driver = self._initialize_driver()

    def _setup_chrome_options(self):

        opts = self.chrome_options
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument(f"--user-data-dir={self.user_dir}")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--disable-extensions")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_argument("--window-size=1200,800")
        opts.add_argument("--disable-software-rasterizer")
        prefs = {"profile.managed_default_content_settings.images": 2}
        opts.add_experimental_option("prefs", prefs)

    def _initialize_driver(self):
        logger.info("Initializing Chrome WebDriver")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=self.chrome_options)
        driver.set_page_load_timeout(self.time_out)
        logger.info("WebDriver initialized successfully")
        return driver

    def cleanup(self):
        logger.info("Cleaning up WebDriver and temp files")
        if self.driver:
            self.driver.quit()
        shutil.rmtree(self.user_dir, ignore_errors=True)
        logger.info("Cleanup completed")

    def run_operations(
        self, parsed_content: List[ParsedResults], data_filler: DataFiller
    ):
        logger.info(f"Starting form filling for {len(parsed_content)} properties")

        for parsed_data in parsed_content:
            property_link = parsed_data.link_to_property
            property_address = parsed_data.property_address
            property_price = parsed_data.property_price

            try:
                _ = WebDriverWait(
                    driver=self.driver, timeout=data_filler.default_timeout
                ).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, data_filler.card_selector)
                    )
                )
                all_inputs = self.driver.find_elements(
                    By.CSS_SELECTOR, data_filler.card_selector
                )
                logger.info(f"Found {len(all_inputs)} input fields")

                if len(all_inputs) >= 3:
                    for i, input_element in enumerate(all_inputs[:3]):
                        WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable(input_element)
                        )

                        if i == 0:  # Address
                            input_element.clear()
                            input_element.send_keys(property_address)
                        elif i == 1:  # Price
                            input_element.clear()
                            input_element.send_keys(str(property_price))
                        elif i == 2:  # Link
                            input_element.clear()
                            input_element.send_keys(property_link)

                    submit_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, data_filler.button_selector)
                        )
                    )
                    submit_button.click()
                    time.sleep(2)
                    logger.info("Form submitted successfully")

                    logger.info(
                        f"Filled form with: {property_address}, {property_price}, {property_link}"
                    )

                    try:
                        another_response_link = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, data_filler.another_response_selector)
                            )
                        )
                        another_response_link.click()
                        time.sleep(2)
                        logger.info("Clicked 'Submit another response' link")
                    except TimeoutException:
                        logger.info("'Submit another response' link not found")
                        if parsed_data != parsed_content[-1]:  # Not the last property
                            break
                else:
                    logger.error(f"Expected 3 inputs, found {len(all_inputs)}")
                    break

            except TimeoutException as e:
                logger.error(f"Timeout waiting for elements: {e}")
                break
            except Exception as e:
                logger.error(f"Error filling form: {e}")
                break
