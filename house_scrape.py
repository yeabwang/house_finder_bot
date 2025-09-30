from httpx import Client, Timeout, HTTPError
from httpx_retry import RetryPolicy, RetryTransport
from models import HouseScraper
import logging

logger = logging.getLogger(__name__)


class HouseScraperService:

    def __init__(self, house_scraper: HouseScraper) -> None:
        self.time_out = Timeout(connect=30, pool=30, read=30, write=30)
        self.retry_policy = RetryPolicy(
            max_retries=house_scraper.max_retries,
            initial_delay=house_scraper.initial_delay,
            max_delay=house_scraper.max_delay,
            multiplier=house_scraper.multiplier,
            retry_on=lambda x: x >= 500,
        )
        self.url_to_be_scraped = house_scraper.url_tobe_scraped

    def scrape_url(self) -> str:
        logger.info(f"Starting scrape: {self.url_to_be_scraped}")
        try:
            with Client(
                verify=True,
                timeout=self.time_out,
                transport=RetryTransport(policy=self.retry_policy),
            ) as client:
                response = client.get(url=self.url_to_be_scraped)
                response.raise_for_status()
                logger.info(f"Scrape successful: {response.status_code}")
        except HTTPError as e:
            logger.error(f"Scrape failed: {e}")
            raise e
        else:
            logger.info(f"Content size: {len(response.text)} chars")
            return response.text
