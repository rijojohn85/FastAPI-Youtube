from typing import List

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()
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
books:List[Book] = [
    Book(
    id=1,
        title="Think Python",
        author= "Allen B. Downey",
        publisher= "O'Reilly Media",
        published_date= "2021-01-01",
        page_count= 1234,
        language= "English",
    ),
    Book(
        id= 2,
        title= "Django By Example",
        author= "Antonio Mele",
        publisher= "Packt Publishing Ltd",
        published_date= "2022-01-19",
        page_count= 1023,
        language= "English",
    ),
    Book(
        id= 3,
        title= "The web socket handbook",
        author= "Alex Diaconu",
        publisher= "Xinyu Wang",
        published_date= "2021-01-01",
        page_count= 3677,
        language= "English",
    ),
    Book(
        id= 4,
        title= "Head first Javascript",
        author= "Hellen Smith",
        publisher= "Oreilly Media",
        published_date= "2021-01-01",
        page_count= 540,
        language= "English",
    ),
    Book(
        id= 5,
        title= "Algorithms and Data Structures In Python",
        author= "Kent Lee",
        publisher= "Springer, Inc",
        published_date= "2021-01-01",
        page_count= 9282,
        language= "English",
    ),
    Book(
        id= 6,
        title= "Head First HTML5 Programming",
        author= "Eric T Freeman",
        publisher= "O'Reilly Media",
        published_date= "2011-21-01",
        page_count= 3006,
        language= "English",
    ),
]
#end point to get all books
@app.get("/books", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books():
    return books

#end point for creating a new book
@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book_payload: CreateBookPayload):
    new_book = Book(id=len(books)+1,**book_payload.model_dump())
    books.append(new_book)
    return new_book

#end point for getting book by id
@app.get("/books/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int):
    if book := next((book for book in books if book.id == book_id), None):
        return book
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

#end point for updating book by id
@app.patch("/books/{book_id}", response_model=Book, status_code=status.HTTP_202_ACCEPTED)
async def update_book_by_id(book_id: int, book_payload: UpdateBookPayload):
    if book := next((book for book in books if book.id == book_id), None):
        [setattr(book, k, v) for k, v in book_payload.model_dump().items()]
        return book
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")



#end point for deleting book by id
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(book_id: int):
    if book := next((book for book in books if book.id == book_id), None):
        books.remove(book)
        return
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")