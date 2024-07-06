import asyncio
from pydantic import ValidationError

from config.database import get_collection
from models.statistics import ParserStatistic, ScraperStatistic
from typing import List, Union, Dict
import logging
from config.config import settings

logger = logging.getLogger(__name__)

SCRAPER_COLLECTION_NAME = settings.MONGO_SCRAPER_STATS_COLLECTION
PARSER_COLLECTION_NAME = settings.MONGO_PARSER_STATS_COLLECTION


async def create_scraper_statistic_object(data: Dict) -> Union[ScraperStatistic, None]:
    try:
        document = ScraperStatistic(**data)
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return None

    collection = await get_collection(SCRAPER_COLLECTION_NAME)
    result = await collection.insert_one(document.dict(by_alias=True))
    if result.inserted_id:
        created_document = await collection.find_one({"_id": result.inserted_id})
        return ScraperStatistic(**created_document)
    return None


async def get_all_scraper_statistic_objects() -> List[ScraperStatistic]:
    collection = await get_collection(SCRAPER_COLLECTION_NAME)
    cursor = collection.find()
    documents = await cursor.to_list(length=None)
    return [ScraperStatistic(**doc) for doc in documents]


async def create_parser_statistic_object(data: Dict) -> Union[ParserStatistic, None]:
    try:
        document = ParserStatistic(**data)
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return None

    collection = await get_collection(PARSER_COLLECTION_NAME)
    result = await collection.insert_one(document.dict(by_alias=True))
    if result.inserted_id:
        created_document = await collection.find_one({"_id": result.inserted_id})
        return ParserStatistic(**created_document)
    return None


async def get_all_parser_statistic_objects() -> List[ParserStatistic]:
    collection = await get_collection(PARSER_COLLECTION_NAME)
    documents = await collection.find().to_list(length=None)
    return [ParserStatistic(**doc) for doc in documents]


class ScraperAnalytics:

    def __init__(self):
        self._data = asyncio.run(get_all_scraper_statistic_objects())

    def average_pages_per_scraper(self) -> Dict[str, float]:
        page_counts, run_counts = {}, {}
        for stat in self._data:
            if stat.scraper_name in page_counts:
                page_counts[stat.scraper_name] += stat.visited_pages
                run_counts[stat.scraper_name] += 1
            else:
                page_counts[stat.scraper_name] = stat.visited_pages
                run_counts[stat.scraper_name] = 1
        return {scraper: page_counts[scraper] / run_counts[scraper] for scraper in page_counts}

    def total_runs_per_scraper(self) -> Dict[str, int]:
        run_counts = {}
        for stat in self._data:
            if stat.scraper_name in run_counts:
                run_counts[stat.scraper_name] += 1
            else:
                run_counts[stat.scraper_name] = 1
        return run_counts

    def longest_run_time(self) -> float:
        return round(max(self._data, key=lambda stat: stat.total_time).total_time, 2)

    def average_run_time(self) -> float:
        total_time = sum(stat.total_time for stat in self._data)
        num_runs = len(self._data)
        return round(total_time / num_runs if num_runs > 0 else 0, 2)

    def most_pages_visited(self) -> ScraperStatistic:
        return max(self._data, key=lambda stat: stat.visited_pages)

    def sum_by_run_id(self) -> Dict[str, Dict[str, float]]:
        sums_by_run_id = {}
        for stat in self._data:
            if stat.run_id not in sums_by_run_id:
                sums_by_run_id[stat.run_id] = {
                    "total_time": 0,
                    "visited_pages": 0
                }
            sums_by_run_id[stat.run_id]["total_time"] += stat.total_time
            sums_by_run_id[stat.run_id]["visited_pages"] += stat.visited_pages
        return sums_by_run_id

    def get_last_run(self) -> ScraperStatistic:
        return max(self._data, key=lambda stat: stat.end_date)


class ParserAnalytics:

    def __init__(self):
        self._data = asyncio.run(get_all_parser_statistic_objects())

    def total_runs_per_parser(self) -> Dict[str, int]:
        run_counts = {}
        for stat in self._data:
            if stat.parser_name in run_counts:
                run_counts[stat.parser_name] += 1
            else:
                run_counts[stat.parser_name] = 1
        return run_counts

    def longest_run_time(self) -> float:
        return round(max(self._data, key=lambda stat: stat.total_time).total_time, 2)

    def average_run_time(self) -> float:
        total_time = sum(stat.total_time for stat in self._data)
        num_runs = len(self._data)
        return round(total_time / num_runs if num_runs > 0 else 0, 2)

    def sum_by_run_id(self) -> Dict[str, Dict[str, float]]:
        sums_by_run_id = {}
        for stat in self._data:
            if stat.run_id not in sums_by_run_id:
                sums_by_run_id[stat.run_id] = {
                    "total_time": 0,
                    "parsed_elements": 0,
                    "saved_elements": 0
                }
            sums_by_run_id[stat.run_id]["total_time"] += stat.total_time
            sums_by_run_id[stat.run_id]["parsed_elements"] += stat.parsed_elements
            sums_by_run_id[stat.run_id]["saved_elements"] += stat.saved_elements
        return sums_by_run_id

    def get_last_run(self) -> ParserStatistic:
        return max(self._data, key=lambda stat: stat.end_date)
