from typing import List

from fastapi import HTTPException, APIRouter
from starlette import status

from src.books.book_data import books
from src.books.models import Book, CreateBookPayload, UpdateBookPayload

books_router = APIRouter()

@books_router.get("", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books():
    return books


@books_router.post("", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book_payload: CreateBookPayload):
    new_book = Book(id=len(books) + 1, **book_payload.model_dump())
    books.append(new_book)
    return new_book


@books_router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int):
    if book := next((book for book in books if book.id == book_id), None):
        return book
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")


@books_router.patch("/{book_id}", response_model=Book, status_code=status.HTTP_202_ACCEPTED)
async def update_book_by_id(book_id: int, book_payload: UpdateBookPayload):
    if book := next((book for book in books if book.id == book_id), None):
        [setattr(book, k, v) for k, v in book_payload.model_dump().items()]
        return book
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")


@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(book_id: int):
    if book := next((book for book in books if book.id == book_id), None):
        books.remove(book)
        return
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
