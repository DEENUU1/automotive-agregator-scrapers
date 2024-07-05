from pydantic import BaseModel, BaseConfig, Field
from models.pyobject_id import PyObjectId
from bson import ObjectId
from typing import Optional


class Raw(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    category: Optional[str] = None
    raw_text: Optional[str] = None
    raw_json: Optional[dict] = None
    created_at: Optional[str] = None

    class Config(BaseConfig):
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
