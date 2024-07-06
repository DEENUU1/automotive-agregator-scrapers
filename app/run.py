from datetime import datetime

from scrapers.olx import OLXScraper
from scrapers.otomoto import OtomotoScraper
from scrapers.strategy import Context as ScraperContext
import logging
from service.raw_service import get_raw_list, delete_raw_by_id
import asyncio
from parsers.otomoto import OtomotoParser
from parsers.strategy import Context as ParserContext
from parsers.olx import OLXParser
from service.statistic_service import create_parser_statistic_object, create_scraper_statistic_object
from models.statistics import ScraperStatistic, ParserStatistic
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    def _run_scrapers() -> None:

        logger.info('Starting the scraper')
        scrapers = [OLXScraper()]  # OtomotoScraper(),

        for scraper in scrapers:
            start, run_date = time.time(), datetime.now()

            context = ScraperContext(scraper)
            total_page = context.run_strategy()

            end, end_date = time.time(), datetime.now()

            scraper_statistic = ScraperStatistic(
                total_time=end - start,
                scraper_name=scraper.__class__.__name__,
                run_date=str(run_date),
                end_date=str(end_date),
                visited_pages=total_page
            )

            asyncio.run(create_scraper_statistic_object(scraper_statistic.dict(by_alias=True)))

        logger.info('Stopping the scraper')


    _run_scrapers()

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
