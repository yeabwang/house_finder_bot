import logging
import sys
from pathlib import Path
import os

from models import HouseScraper, HouseParser, DataFiller
from house_scrape import HouseScraperService
from house_parser import HouseParserService
from data_filler import DataFillerService


def save_to_env(form_link, scrape_url):
    env_file = Path(".env")
    env_content = f"""FORM_LINK={form_link}
LINK_TO_SCRAPE={scrape_url}
"""
    env_file.write_text(env_content)
    logging.getLogger(__name__).info("URLs saved to .env file")


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("house_bot.log"),
        ],
    )


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("=== House Finder Bot Started ===")
    
    form_link = input("Please enter the Google Form link: ").strip()
    if not form_link:
        logger.error("Form link is required. Exiting.")
        return
        
    scrape_url = input("Please enter the URL to scrape for houses: ").strip()
    if not scrape_url:
        logger.error("Scrape URL is required. Exiting.")
        return
    
    save_to_env(form_link, scrape_url)

    try:
        scraper_config = HouseScraper()
        scraper_config.url_tobe_scraped = scrape_url
        parser_config = HouseParser()
        filler_config = DataFiller()
        filler_config.form_link = form_link

        logger.info("Configurations loaded successfully")

        logger.info("Step 1: Scraping website")
        scraper = HouseScraperService(scraper_config)
        scraped_content = scraper.scrape_url()

        if not scraped_content:
            logger.error("No content scraped. Exiting.")
            return

        logger.info("Step 2: Parsing scraped content")
        parser = HouseParserService()
        parsed_properties = parser.parse_data(scraped_content, parser_config)

        if not parsed_properties:
            logger.warning("No properties found. Exiting.")
            return

        logger.info("Step 3: Filling forms")
        filler = DataFillerService(filler_config)

        try:
            filler.driver.get(filler_config.form_link)
            logger.info(f"Navigated to form: {filler_config.form_link}")

            filler.run_operations(parsed_properties, filler_config)
            logger.info("Form filling completed successfully")

        finally:
            filler.cleanup()

        logger.info("=== House Finder Bot Completed Successfully ===")

    except Exception as e:
        logger.error(f"Application failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
