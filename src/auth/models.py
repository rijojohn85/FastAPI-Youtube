from sqlmodel import SQLModel, Field, Column, String, Boolean
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        ),
    )
    username: str = Field(sa_column=Column(String(100), unique=True))
    password_hash: bytes = Field(
        exclude=True
    )  # exclude while returning the data to user
    email: str = Field(sa_column=Column(String(120), unique=True))
    first_name: str = Field(sa_column=Column(String(120), nullable=True))
    last_name: str = Field(sa_column=Column(String(120), nullable=True))
    is_verified: bool = Field(sa_column=Column(Boolean, default=False))
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
        return f"<User {self.username}>"
