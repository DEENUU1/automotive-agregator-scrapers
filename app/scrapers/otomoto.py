from models.raw import Raw
from scrapers.strategy import ScraperStrategy
import requests
from bs4 import BeautifulSoup
import logging
from service.raw_service import create_object
from datetime import datetime
import asyncio


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

    def run(self):

        category = self.categories[0]

        url = f"{self.base_url}{category}"
        response = requests.get(url)

        page = response.text

        raw = Raw(
            category=category,
            site=self.site_name,
            raw_text=page,
            created_at=datetime.utcnow().isoformat()
        )

        asyncio.run(self.save_raw(raw.dict(by_alias=True)))
