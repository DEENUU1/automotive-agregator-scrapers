from typing import List, Optional

from models.raw import Raw
from parsers.strategy import ParserStrategy
import logging
from bs4 import BeautifulSoup
from models.offer import Offer, Price, Location

logger = logging.getLogger(__name__)


class OtomotoParser(ParserStrategy):
    def __init__(self):
        super().__init__()
        self._parsed_data = []

    @staticmethod
    def _get_soup(data: str):
        try:
            return BeautifulSoup(data, 'html.parser')
        except Exception as e:
            logger.error(f"Error while creating soup: {e}")
            return None

    @staticmethod
    def _change_image_size(image_url: Optional[str] = None) -> Optional[str]:
        if not image_url:
            return None
        return image_url.replace("320x240", "1500x1500")

    @staticmethod
    def _parse_mileage(mileage: Optional[str] = None) -> Optional[int]:
        if not mileage:
            return None
        return int(mileage.replace(" km", "").replace(" ", ""))

    @staticmethod
    def _get_normalized_fuel_type(fuel_type: Optional[str] = None) -> Optional[str]:
        if not fuel_type:
            return None

        fuel_type_mapping = {
            "Benzyna+LPG": "lpg",
            "Diesel": "diesel",
            "Benzyna": "petrol",
            "Elektryczny": "electric",
            "Hybryda": "plugin-hybrid",
        }

        return fuel_type_mapping.get(fuel_type, None)

    @staticmethod
    def _get_normalized_gearbox(gearbox: Optional[str] = None) -> Optional[str]:
        if not gearbox:
            return None

        gearbox_mapping = {
            "Automatyczna": "automatic",
            "Manualna": "manual",
        }

        return gearbox_mapping.get(gearbox, None)

    @staticmethod
    def _parse_location(location: Optional[str] = None) -> Optional[Location]:
        if not location:
            return None

        if "(" not in location and  ")" not in location:
            return None

        city, region = location.split(' (')
        region = region.rstrip(')')

        return Location(
            country="PL",
            city=city,
            region=region
        )

    def run(self, data: Raw) -> Optional[List[Offer]]:
        soup = self._get_soup(data.raw_text)
        if not soup:
            return

        try:
            search_result = soup.find("div", {"data-testid": "search-results"})
            offers = search_result.find_all("article")

            if not offers:
                logger.warning("No offers found.")
                return

            for offer in offers:
                try:
                    title = offer.find("h1")
                    if not title:
                        continue

                    offer_url = title.find("a")
                    description = offer.find("p", class_="e1vic7eh10 ooa-1tku07r er34gjf0")

                    details_data = offer.find("dl", class_="ooa-1uwk9ii e1vic7eh11")

                    mileage = details_data.find("dd", {"data-parameter": "mileage"})
                    fuel_type = details_data.find("dd", {"data-parameter": "fuel_type"})
                    gearbox = details_data.find("dd", {"data-parameter": "gearbox"})
                    production_year = details_data.find("dd", {"data-parameter": "year"})

                    details_data_2 = offer.find("dl", class_="ooa-1o0axny e1vic7eh14")
                    p_tags = details_data_2.find_all("p")

                    location = p_tags[0].text.strip()

                    price = offer.find("h3", class_="e1vic7eh16 ooa-1n2paoq er34gjf0")

                    image = offer.find("img")

                    price_val = price.text.strip() if price else None
                    price_obj = None
                    if price_val:
                        price_obj = Price(
                            value=float(price_val.replace(" ", "")),
                            currency="PLN",
                        )

                    parsed_data = Offer(
                        title=title.text.strip(),
                        offer_url=offer_url["href"] if offer_url else None,
                        description=description.text.strip() if description else None,
                        mileage=self._parse_mileage(mileage.text.strip() if mileage else None),
                        fuel_type=self._get_normalized_fuel_type(fuel_type.text.strip() if fuel_type else None),
                        gearbox=self._get_normalized_gearbox(gearbox.text.strip() if gearbox else None),
                        production_year=int(production_year.text.strip()) if production_year else None,
                        location=self._parse_location(location),
                        price=price_obj,
                        image_url=self._change_image_size(image.get("src")) if image else None,
                        category=data.category,
                        source="otomoto"
                    )
                    self._parsed_data.append(parsed_data)

                except Exception as e:
                    logger.error(f"Error while parsing offer: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error while creating soup: {e}")
            return

        return self._parsed_data
