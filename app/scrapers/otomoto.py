from scrapers.strategy import ScraperStrategy
import requests
from bs4 import BeautifulSoup
import logging

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

    def run(self):

        category = self.categories[0]

        url = f"{self.base_url}{category}"
        response = requests.get(url)

        soup = BeautifulSoup(response.content, "html.parser")

        search_result = soup.find("div", {"data-testid": "search-results"})

        articles = search_result.find_all("article", class_="ooa-yca59n e1vic7eh0")

        logger.info(f"Found {len(articles)} articles")

