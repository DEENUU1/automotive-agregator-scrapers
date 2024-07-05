from scrapers.otomoto import OtomotoScraper
from scrapers.strategy import Context as ScraperContext
import logging
from service.raw_service import get_raw_list, delete_raw_by_id
import asyncio
from parsers.otomoto import OtomotoParser
from parsers.strategy import Context as ParserContext

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    # logger.info('Starting the scraper')
    #
    # context = ScraperContext(OtomotoScraper())
    # context.run_strategy()
    #
    # logger.info('Stopping the scraper')

    logger.info("Start parsing")

    raw_data = asyncio.run(get_raw_list())

    for raw in raw_data:
        if raw.site == "otomoto":
            context = ParserContext(OtomotoParser())
            context.run_strategy(raw)
        else:
            logger.info("No scraper for this site")
            continue

    logger.info("End parsing")
