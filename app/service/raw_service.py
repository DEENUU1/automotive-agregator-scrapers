import os

from bson import ObjectId
from pydantic import ValidationError

from config.database import get_collection
from models.raw import Raw
from typing import List, Union, Dict
import logging
from config.config import settings

logger = logging.getLogger(__name__)

COLLECTION_NAME = settings.MONGO_RAW_COLLECTION


async def get_raw_list() -> List[Raw]:
    collection = await get_collection(COLLECTION_NAME)
    cursor = collection.find()
    documents = await cursor.to_list(length=None)
    return [Raw(**doc) for doc in documents]


async def create_raw_object(data: Dict) -> Union[Raw, None]:
    try:
        document = Raw(**data)
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return None

    collection = await get_collection(COLLECTION_NAME)
    result = await collection.insert_one(document.dict(by_alias=True))
    if result.inserted_id:
        created_document = await collection.find_one({"_id": result.inserted_id})
        return Raw(**created_document)
    return None


async def delete_raw_by_id(document_id: str) -> bool:
    collection = await get_collection(COLLECTION_NAME)
    result = await collection.delete_one({"_id": ObjectId(document_id)})
    return result.deleted_count > 0
