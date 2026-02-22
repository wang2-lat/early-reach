from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class Platform(str, Enum):
    PRODUCT_HUNT = "ProductHunt"
    REDDIT = "Reddit"
    TWITTER = "Twitter"
    HACKER_NEWS = "HackerNews"
    INDIE_HACKERS = "IndieHackers"


class Product(BaseModel):
    name: str
    description: str
    url: Optional[str] = ""
    created_at: datetime = Field(default_factory=datetime.now)


class Launch(BaseModel):
    platform: Platform
    url: Optional[str] = ""
    notes: Optional[str] = ""
    launched_at: datetime


class Feedback(BaseModel):
    source: str
    content: str
    platform: Optional[Platform] = None
    rating: Optional[int] = None
    created_at: datetime
