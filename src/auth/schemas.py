from datetime import datetime
from typing import Optional, List
import uuid

from pydantic import BaseModel, Field

from src.db.models import Book


class CreateUserPayload(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=6)
    email: str = Field(max_length=120)
    first_name: Optional[str] = Field(max_length=120, default=None)
    last_name: Optional[str] = Field(max_length=120, default=None)


class UserLoginPayload(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=6)


class UserSchema(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    updated_at: datetime
    created_at: datetime
    books: List[Book]
