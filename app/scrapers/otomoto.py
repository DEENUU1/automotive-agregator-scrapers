from models.raw import Raw
from scrapers.strategy import ScraperStrategy
import requests
import logging
from datetime import datetime
import asyncio
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


class OtomotoScraper(ScraperStrategy):
    def __init__(self):
        super().__init__()
        self.categories = [
            "osobowe",
            "motocykle-i-quady",
            "dostawcze",
            "ciezarowe",
            "maszyny-budowlane",
            "przyczepy",
            "maszyny-rolnicze"
        ]
        self.base_url = "https://www.otomoto.pl/"
        self.site_name = "otomoto"
        self.next_page = True
        self.page_number = 1

    @staticmethod
    def is_next_page(data: str) -> bool:
        try:
            soup = BeautifulSoup(data, 'html.parser')
            next_page_object = soup.find("li", {"title": "Next Page"})
            if not next_page_object:
                return False
            return True
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return False

    def run(self):

        for category in self.categories:
            while self.next_page:
                url = f"{self.base_url}{category}?search[order]=created_at_first%3Adesc&page={self.page_number}"
                logger.info(f"Scraping {url}")

                try:
                    response = requests.get(url)
                except Exception as e:
                    logger.error(f"Error fetching {url}: {e}")
                    return

                self.next_page = self.is_next_page(response.text)
                self.page_number += 1

                raw = Raw(
                    category=category,
                    site=self.site_name,
                    raw_text=response.text,
                    created_at=datetime.utcnow().isoformat()
                )

                asyncio.run(self.save_raw(raw.dict(by_alias=True)))
