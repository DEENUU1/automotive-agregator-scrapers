from pydantic import BaseModel
from typing import Optional


class Offer(BaseModel):
    title: str
    offer_url: str
    description: Optional[str] = None
    mileage: Optional[str] = None
    fuel_type: Optional[str] = None
    gearbox: Optional[str] = None
    production_year: Optional[str] = None
    location: Optional[str] = None
    publication_time: Optional[str] = None
    price: Optional[str] = None
    image_url: Optional[str] = None
