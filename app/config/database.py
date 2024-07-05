import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from config.config import settings

logger = logging.getLogger(__name__)


async def client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)


async def get_db() -> AsyncIOMotorDatabase:
    db_client = await client()
    return db_client[settings.MONGO_DATABASE_NAME]


async def get_collection(collection_name: str) -> AsyncIOMotorCollection | None:
    try:
        db = await get_db()
        return db[collection_name]
    except KeyError:
        raise KeyError("Invalid collection name")
    except Exception as e:
        logger.error(f"Error retrieving collection: {e}")
        return None
