from pydantic import BaseModel
from typing import Optional, List


class Price(BaseModel):
    value: float
    currency: str


class Location(BaseModel):
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None


class Offer(BaseModel):
    title: str
    offer_url: str
    description: Optional[str] = None
    mileage: Optional[int] = None
    fuel_type: Optional[str] = None
    gearbox: Optional[str] = None
    production_year: Optional[int] = None
    location: Optional[Location] = None
    publication_time: Optional[str] = None
    price: Optional[Price] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    engine_size: Optional[int] = None
    engine_power: Optional[int] = None
    car_body: Optional[str] = None
    color: Optional[str] = None
    condition: Optional[str] = None
    drive: Optional[str] = None
    vin: Optional[str] = None
