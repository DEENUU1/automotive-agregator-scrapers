import asyncio
import logging
from datetime import datetime

from celery import Celery
# from celery.schedules import crontab

from config.config import settings
from models.statistics import ScraperStatistic, ParserStatistic
from parsers.olx import OLXParser
from parsers.otomoto import OtomotoParser
from scrapers.olx import OLXScraper
# from scrapers.otomoto import OtomotoScraper
from scrapers.strategy import Context as ScraperContext
from service.raw_service import get_raw_list, delete_raw_by_id
from parsers.strategy import Context as ParserContext
import time

from service.statistic_service import create_scraper_statistic_object, create_parser_statistic_object

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


@celery_app.task(name="task_parsers")
def task_parsers() -> None:
    logger.info("Start parsing")

    raw_data = asyncio.run(get_raw_list())

    for idx, raw in enumerate(raw_data):
        logger.info(f"Parsing {idx + 1} / {len(raw_data)}")

        if raw.site == "otomoto":
            class_ = ParserContext(OtomotoParser())

        elif raw.site == "olx":
            class_ = (OLXParser())

        else:
            logger.info("No scraper for this site")
            continue

        start, run_date = time.time(), datetime.now()

        data = ParserContext(class_).run_strategy(raw)

        end, end_date = time.time(), datetime.now()

        parser_statistic = ParserStatistic(
            total_time=end - start,
            parser_name=class_.__class__.__name__,
            run_date=str(run_date),
            end_date=str(end_date),
            parsed_elements=len(data),
            saved_elements=0  # TODO update this value
        )
        asyncio.run(create_parser_statistic_object(parser_statistic.dict(by_alias=True)))
        asyncio.run(delete_raw_by_id(str(raw.id)))

    logger.info("End parsing")
