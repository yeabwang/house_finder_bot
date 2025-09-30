import os
from dataclasses import dataclass
from dotenv import find_dotenv, load_dotenv

_ = find_dotenv()
load_dotenv()


@dataclass
class HouseScraper:
    max_retries: int = 3
    initial_delay: float = 0.1
    max_delay: float = 0.1
    multiplier: float = 0.5
    url_tobe_scraped: str = os.getenv("LINK_TO_SCRAPE", "")


@dataclass
class HouseParser:
    card_tag: str = "StyledPropertyCardDataWrapper"
    anchor_tag: str = "StyledPropertyCardDataArea-anchor"
    address_tag: str = "property-card-addr"
    price_tag: str = "PropertyCardWrapper__StyledPriceLine"


@dataclass
class ParsedResults:
    property_address: str
    property_price: str
    link_to_property: str
