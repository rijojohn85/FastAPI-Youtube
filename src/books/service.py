import uuid
from fastapi import HTTPException, status
from typing import Dict, List
from sqlalchemy import Sequence
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from datetime import datetime


from src.db.models import Book
from src.books.schemas import CreateBookPayload, UpdateBookPayload


class BookService:
    async def get_all_books(self, session: AsyncSession) -> Sequence[Book]:
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()  # type: ignore

    async def get_book_by_id(self, book_id: str, session: AsyncSession) -> Book:
        statement = select(Book).where(Book.uid == book_id)
        try:
            result = await session.exec(statement)
        except Exception as e:
            raise Exception(str(e))
        book = result.first()
        if book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )
        return book

    async def get_book_by_uid(
        self, session: AsyncSession, user_uid: uuid.UUID
    ) -> List[Book]:
        """Get Book By User

        Args:
            session: DB session injected through dependency
            user_uid: User id to search for
        Returns:
            List of books created by user_uid
        """
        statement = select(Book).where(Book.user_uid == user_uid)
        try:
            result = await session.exec(statement=statement)
        except Exception as e:
            raise e
        books = result.all()
        return books  # type: ignore

    async def create_book(
        self,
        book_payload: CreateBookPayload,
        session: AsyncSession,
        user_uid: uuid.UUID,
    ) -> Book:
        """Create a book object and store it in the DB

        Args:
            book_payload: book create payload
            session: DB session
            user_uid: user_uid for user creating book

        Returns:
            Book: newly created and stored book object.
        """
        new_book = Book(**book_payload.model_dump())
        new_book.user_uid = user_uid
        try:
            session.add(new_book)
            await session.commit()
            await session.refresh(new_book)
        except Exception as e:
            raise e
        return new_book

    async def update_book(
        self, book_id: str, book_payload: UpdateBookPayload, session: AsyncSession
    ) -> Book:
        try:
            book_to_update = await self.get_book_by_id(book_id, session)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise Exception(str(e))

        for k, v in book_payload.model_dump().items():
            setattr(book_to_update, k, v)
        setattr(book_to_update, "updated_at", datetime.now())
        try:
            await session.commit()
            await session.refresh(book_to_update)
        except Exception as e:
            await session.rollback()
            raise e
        return book_to_update

    async def delete_book(self, book_id: str, session: AsyncSession) -> Dict:
        book_to_delete = await self.get_book_by_id(book_id, session)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return {"success": True}
        else:
            return {"success": False}
