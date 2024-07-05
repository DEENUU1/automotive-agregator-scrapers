import logging
from bson.objectid import ObjectId

logger = logging.getLogger(__name__)


class PyObjectId(ObjectId):
    """Custom BSON ObjectId type for Pydantic."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, field):
        """Validate ObjectId."""
        if not ObjectId.is_valid(value):
            raise ValueError('Invalid ObjectId')
        return ObjectId(value)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate