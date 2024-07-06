from typing import List, Optional

from models.raw import Raw
from parsers.strategy import ParserStrategy
import logging
from models.offer import Offer, Location, Price


logger = logging.getLogger(__name__)


class OLXParser(ParserStrategy):
    def __init__(self):
        super().__init__()
        self._parsed_data = []

    @staticmethod
    def _parse_publication_time(value: Optional[str]) -> Optional[str]:
        if not value:
            return None

        return value[:10]

    def run(self, data: Raw) -> Optional[List[Offer]]:
        for offer in data.raw_json.get("data", []):
            try:

                offer_url = offer.get("url")
                title = offer.get("title")

                if not offer_url or not title:
                    continue

                description = offer.get("description")
                created_time = offer.get("created_time")

                location_object = offer.get("location", {})
                city = location_object.get("city", {}).get("name")
                region = location_object.get("region", {}).get("name")

                images_object = offer.get("photos", [])
                image_urls = [image.get("link") for image in images_object]

                params = offer.get("params", [])

                price_val, price_cur, engine_size, production_year, engine_power, fuel_type, car_body, milage, color, condition, gearbox, drive, vin = (
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None
                )

                for param in params:
                    key = param.get("key")

                    if key == "price":
                        price_val = param.get("value", {}).get("value")
                        price_cur = param.get("value", {}).get("currency")

                    if key == "enginesize":
                        engine_size = param.get("value", {}).get("key")

                    if key == "year":
                        production_year = param.get("value", {}).get("key")

                    if key == "enginepower":
                        engine_power = param.get("value", {}).get("key")

                    if key == "petrol":
                        fuel_type = param.get("value", {}).get("key")

                    if key == "car_body":
                        car_body = param.get("value", {}).get("key")

                    if key == "milage":
                        milage = param.get("value", {}).get("key")

                    if key == "color":
                        color = param.get("value", {}).get("key")

                    if key == "condition":
                        condition = param.get("value", {}).get("key")

                    if key == "transmission":
                        gearbox = param.get("value", {}).get("key")

                    if key == "drive":
                        drive = param.get("value", {}).get("key")

                    if key == "vin":
                        vin = param.get("value", {}).get("key")

                price_obj, location_obj = None, None
                if price_val and price_cur:
                    price_obj = Price(value=price_val, currency=price_cur)

                if city and region:
                    location_obj = Location(city=city, region=region, country="PL")

                offer = Offer(
                    title=title,
                    offer_url=offer_url,
                    description=description,
                    mileage=int(milage) if milage else None,
                    fuel_type=fuel_type,
                    gearbox=gearbox,
                    production_year=int(production_year) if production_year else None,
                    location=location_obj,
                    publication_time=self._parse_publication_time(created_time),
                    price=price_obj,
                    image_url=image_urls[0],
                    category=data.category,
                    engine_size=int(engine_size) if engine_size else None,
                    engine_power=int(engine_power) if engine_power else None,
                    car_body=car_body,
                    color=color,
                    condition=condition,
                    drive=drive,
                    vin=vin,
                    source="olx",
                )
                self._parsed_data.append(offer)

            except Exception as e:
                logger.error(e)
                continue

        return self._parsed_data
