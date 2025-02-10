from typing import Optional

from pydantic import BaseModel, Field


class CreateUserPayload(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=6)
    email: str = Field(max_length=120)
    first_name: Optional[str] = Field(max_length=120, default=None)
    last_name: Optional[str] = Field(max_length=120, default=None)


class UserLoginPayload(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=6)
