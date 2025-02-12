from pydantic import BaseModel
from typing import Optional
import uuid


class ReviewPayloadSchema(BaseModel):
    rating: int
    review_text: str
    book_uid: Optional[uuid.UUID]


class ReviewCreateSchema(ReviewPayloadSchema):
    user_uid: Optional[uuid.UUID]


class ReviewResponseSchema(ReviewCreateSchema):
    uid: uuid.UUID
