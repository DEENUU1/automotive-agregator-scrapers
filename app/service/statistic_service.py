from bson import ObjectId
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
