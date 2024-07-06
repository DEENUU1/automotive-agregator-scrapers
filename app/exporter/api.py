from typing import List

import requests
from models.offer import Offer
from config.config import settings
import logging


logger = logging.getLogger(__name__)


def save_offers_by_api(offers: List[Offer]) -> None:
    try:
        offers_dict = [offer.dict() for offer in offers]
        response = requests.post(settings.API_URL,  json=offers_dict)
        response.raise_for_status()
        logger.info("Offers saved successfully via API")
        return
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        return
