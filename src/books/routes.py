from typing import List
from src.books.service import BookService
from src.utils import logger

from fastapi import HTTPException, APIRouter, Depends
from starlette import status

from src.books.schemas import Book, CreateBookPayload, UpdateBookPayload
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.dependencies import AccessTokenBearer

books_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()


@books_router.get("/", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details: AccessTokenBearer = Depends(access_token_bearer),
):
    logger.debug(token_details)
    books = await book_service.get_all_books(session)
    return books


@books_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_payload: CreateBookPayload,
    session: AsyncSession = Depends(get_session),
    token_details: AccessTokenBearer = Depends(access_token_bearer),
):
    try:
        new_book = await book_service.create_book(
            book_payload=book_payload, session=session
        )
    except HTTPException as err:
        raise err
    except Exception as err:
        logger.error(err)
        raise err
    return new_book


@books_router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book_by_id(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    token_details: AccessTokenBearer = Depends(access_token_bearer),
):
    if len(book_id) != 36:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid book ID"
        )
    try:
        book = await book_service.get_book_by_id(book_id=book_id, session=session)
    except HTTPException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return book


@books_router.patch(
    "/{book_id}", response_model=Book, status_code=status.HTTP_202_ACCEPTED
)
async def update_book_by_id(
    book_id: str,
    book_payload: UpdateBookPayload,
    session: AsyncSession = Depends(get_session),
    token_details: AccessTokenBearer = Depends(access_token_bearer),
):
    updated_book = await book_service.update_book(
        book_id=book_id, book_payload=book_payload, session=session
    )
    if updated_book is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    return updated_book


@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    token_details: AccessTokenBearer = Depends(access_token_bearer),
):
    delete_status = await book_service.delete_book(book_id=book_id, session=session)
    if not delete_status["success"]:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
