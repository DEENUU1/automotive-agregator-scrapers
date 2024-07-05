from scrapers.otomoto import OtomotoScraper
from scrapers.strategy import Context
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.info('Starting the scraper')

    context = Context(OtomotoScraper())
    context.run_strategy()

    logger.info('Stopping the scraper')
