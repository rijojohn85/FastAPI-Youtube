from typing import Optional, List
import uuid
from datetime import datetime, date

from pydantic import BaseModel

from src.db.models import Reviews


class UpdateBookPayload(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str


class CreateBookPayload(UpdateBookPayload):
    published_date: date


class Book(CreateBookPayload):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime
    user_uid: Optional[uuid.UUID]
    reviews: List[Reviews]
