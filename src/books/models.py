from pydantic import BaseModel


class CreateBookPayload(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class Book(CreateBookPayload):
    id:int


class UpdateBookPayload(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
