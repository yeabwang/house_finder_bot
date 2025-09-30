from bs4 import BeautifulSoup
from models import HouseParser, ParsedResults


class HouseParserService:
    def __init__(self) -> None:
        self.scraped_data = ""
        self.property_price = 0
        self.property_address = ""
        self.link_to_property = ""
        self.all_houses = []

    def parse_data(self, scraped_data, house_parser: HouseParser):
        self.scraped_data = scraped_data
        soup = BeautifulSoup(self.scraped_data, "lxml")
        property_cards = soup.find_all("div", class_=house_parser.card_tag)

        for property in property_cards:
            anchor_tag = property.find("a", class_=house_parser.anchor_tag)
            if anchor_tag and anchor_tag.has_attr("href"):
                self.link_to_property = str(anchor_tag["href"])
            else:
                self.link_to_property = ""

            main_address = property.find(
                "address", attrs={"data-test": house_parser.address_tag}
            )

            if main_address:
                self.property_address = main_address.text.strip()
            else:
                self.property_address = ""
            main_price = property.find("span", class_=house_parser.price_tag)
            if main_price and main_price.text:
                self.property_price = float(
                    "".join(
                        filter(lambda char: char.isdigit(), main_price.text.strip())
                    )
                )
            else:
                self.property_price = 0

            full_house_detail = ParsedResults(
                property_address=self.property_address,
                property_price=self.property_price,
                link_to_property=self.link_to_property,
            )

            self.all_houses.append(full_house_detail)
