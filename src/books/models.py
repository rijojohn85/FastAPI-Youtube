from datetime import datetime, date

from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid


class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    publisher: str = Field(min_length=1, max_length=100)
    published_date: date
    page_count: int = Field(gt=0)
    language: str
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now,
        )
    )

    def __repr__(self):
        return f"<Book {self.title}>"
