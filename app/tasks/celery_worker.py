import asyncio
import logging

from celery import Celery
# from celery.schedules import crontab

from config.config import settings
from parsers.olx import OLXParser
from parsers.otomoto import OtomotoParser
from scrapers.olx import OLXScraper
from scrapers.otomoto import OtomotoScraper
from scrapers.strategy import Context as ScraperContext
from service.raw_service import get_raw_list, delete_raw_by_id
from parsers.strategy import Context as ParserContext


logger = logging.getLogger(__name__)

celery_app: Celery = Celery(
    "tasks",
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_BACKEND,
)
# celery_app.conf.beat_schedule = {
#     "task-scraper": {
#         "task": "scraper",
#         "schedule": crontab(minute="10", hour="12"),
#     },
# }
celery_app.conf.timezone = "UTC"
celery_app.conf.worker_redirect_stdouts = False
celery_app.conf.task_routes = {"tasks.*": {"queue": "celery"}}
celery_app.conf.update(
    result_expires=3600,
)


@celery_app.task(name="task_scrapers")
def task_scrapers() -> None:
    logger.info('Starting the scraper')
    scrapers = [OtomotoScraper(), OLXScraper()]

    for scraper in scrapers:
        context = ScraperContext(scraper)
        context.run_strategy()
    logger.info('Stopping the scraper')


@celery_app.task(name="task_parsers")
def task_parsers() -> None:
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
