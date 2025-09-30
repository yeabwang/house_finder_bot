import os
from dataclasses import dataclass
from dotenv import find_dotenv, load_dotenv

_ = find_dotenv()
load_dotenv()


class HouseScraper:
    max_retries: int = 3
    initial_delay = 0.1
    max_delay = 0.1
    multiplier = 0.5
    url_tobe_scraped: str = os.getenv("LINK_TO_SCRAPE", "")
