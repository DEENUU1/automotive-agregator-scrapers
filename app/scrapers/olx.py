from models.raw import Raw
from scrapers.strategy import ScraperStrategy
import requests
import logging
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)


class OLXScraper(ScraperStrategy):
    def __init__(self):
        super().__init__()
        self.categories = {
            "osobowe": "https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=84&filter_refiners=spell_checker&sl=18c34ade124x23bc10a5",
            # "motocykle-i-quady": "https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=81&filter_refiners=spell_checker&sl=18c34ade124x23bc10a5",
            # "dostawcze": "https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=3558&filter_refiners=spell_checker&sl=18c34ade124x23bc10a5",
            # "ciezarowe": "https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=3559&filter_refiners=spell_checker&sl=18c34ade124x23bc10a5",
            # "maszyny-budowlane": "https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=3560&filter_refiners=spell_checker&sl=18c34ade124x23bc10a5",
            # "przyczepy": "https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=3561&filter_refiners=spell_checker&sl=18c34ade124x23bc10a5"
        }
        self.site_name = "olx"

    def run(self):

        for name, url in self.categories.items():
            curr_url: str = url

            while curr_url:
                logger.info(f"Scraping {curr_url}")

                try:
                    response = requests.get(curr_url)
                except Exception as e:
                    logger.error(f"Error fetching {curr_url}: {e}")
                    continue

                data = response.json()

                next_url = data.get("links", {}).get("next", None)
                if not next_url:
                    break

                curr_url = next_url.get("href", None)

                raw = Raw(
                    category=name,
                    site=self.site_name,
                    raw_json=data,
                    created_at=datetime.utcnow().isoformat()
                )
                asyncio.run(self.save_raw(raw.dict(by_alias=True)))
