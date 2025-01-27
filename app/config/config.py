from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
from starlette.templating import Jinja2Templates

load_dotenv()


class Settings(BaseSettings):
    # App
    TITLE: str | None = "Media expert price comparison"
    DEBUG: bool | None = os.getenv("DEBUG") == "True"
    TEMPLATES: Jinja2Templates = Jinja2Templates(directory="templates")

    # Celery
    CELERY_BROKER: str | None = os.getenv("CELERY_BROKER")
    CELERY_BACKEND: str | None = os.getenv("CELERY_BACKEND")

    # Mongodb
    MONGO_CONNECTION_STRING: str | None= os.getenv("MONGO_CONNECTION_STRING")
    MONGO_DATABASE_NAME: str | None= os.getenv("MONGO_DATABASE_NAME")
    MONGO_RAW_COLLECTION: str | None= os.getenv("MONGO_RAW_COLLECTION")
    MONGO_SCRAPER_STATS_COLLECTION: str | None = os.getenv("MONGO_SCRAPER_STATS_COLLECTION")
    MONGO_PARSER_STATS_COLLECTION: str | None = os.getenv("MONGO_PARSER_STATS_COLLECTION")

    # API URL
    API_URL: str | None = os.getenv("API_URL")


settings = Settings()
