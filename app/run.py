from scrapers.olx import OLXScraper
from scrapers.otomoto import OtomotoScraper
from scrapers.strategy import Context as ScraperContext
import logging
from service.raw_service import get_raw_list, delete_raw_by_id
import asyncio
from parsers.otomoto import OtomotoParser
from parsers.strategy import Context as ParserContext
from parsers.olx import OLXParser

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    def _run_scrapers() -> None:
        logger.info('Starting the scraper')
        scrapers = [OtomotoScraper(), OLXScraper()]

        for scraper in scrapers:
            context = ScraperContext(scraper)
            context.run_strategy()
        logger.info('Stopping the scraper')


    def _run_parsers() -> None:
        logger.info("Start parsing")

        raw_data = asyncio.run(get_raw_list())

        for idx, raw in enumerate(raw_data):
            logger.info(f"Parsing {idx + 1} / {len(raw_data)}")

            if raw.site == "otomoto":
                context = ParserContext(OtomotoParser())
                context.run_strategy(raw)

            elif raw.site == "olx":
                context = ParserContext(OLXParser())
                context.run_strategy(raw)

            else:
                logger.info("No scraper for this site")
                continue

            delete_raw_by_id(str(raw.id))

        logger.info("End parsing")
