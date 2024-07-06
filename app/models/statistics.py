from pydantic import BaseModel, BaseConfig, Field
from models.pyobject_id import PyObjectId
from bson import ObjectId


class ScraperStatistic(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    run_date: str
    end_date: str
    total_time: float
    visited_pages: int
    scraper_name: str
    run_id: str

    class Config(BaseConfig):
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True


class ParserStatistic(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    run_date: str
    end_date: str
    total_time: float
    parsed_elements: int
    saved_elements: int
    parser_name: str
    run_id: str

    class Config(BaseConfig):
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
